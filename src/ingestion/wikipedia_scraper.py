"""Wikipedia city metadata scraper for Phase 4.

This module fetches and parses Wikipedia city pages to extract city metadata
(population, area, country) for use in the euro-air-quality-pipeline Silver
layer.

Design constraints:
- Side-effect free on import.
- Network calls happen only inside ``fetch_and_save_html``; never at module level.
- No Kafka, no Spark, no Open-Meteo logic.
- No EEA loader logic; this module is independent of Phase 3.
- All parsing failures are caught and recorded in ``metadata_notes`` so that
  callers always receive a structurally complete record.
- File writes happen only through explicit writer functions.

Schema contracts are defined in docs/data_model.md under
'Phase 4 Wikipedia City Metadata Schema'.
"""

from __future__ import annotations

import logging
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_HTML_DIR = Path("data/bronze/wikipedia_html")
DEFAULT_CITY_METADATA_PATH = Path("data/silver/city_metadata.parquet")
MIN_REQUEST_DELAY_SECONDS: float = 1.0
USER_AGENT = "euro-air-quality-pipeline/1.0"

# Silver output column order — must match docs/data_model.md Phase 4 schema
METADATA_COLUMNS: tuple[str, ...] = (
    "city_id",
    "city_name",
    "population",
    "area_km2",
    "population_density",
    "country",
    "wikipedia_url",
    "scraped_at",
    "metadata_notes",
    "source",
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _empty_record(city_id: str, wikipedia_url: str) -> dict:
    """Return a blank metadata record with all nullable fields set to None."""
    return {
        "city_id": city_id,
        "city_name": None,
        "population": None,
        "area_km2": None,
        "population_density": None,
        "country": None,
        "wikipedia_url": wikipedia_url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "metadata_notes": "",
        "source": "wikipedia",
    }


# Unit suffixes to strip before number parsing.
# Must match docs/data_model.md Phase 4 normalization rules.
_UNIT_SUFFIXES: tuple[str, ...] = (
    "/km\u00b2",  # /km² (with superscript)
    "/km2",
    "km\u00b2",   # km² (with superscript)
    "km2",
    "inhabitants",
    "people",
    "pop.",
    "sq\u00a0mi",  # sq\xc2\xa0mi (non-breaking space)
    "sq mi",
)


def normalize_number(raw: str) -> Optional[float]:
    """Strip non-numeric noise from a Wikipedia infobox value and return a float.

    Supported input formats:
    - Comma-separated thousands: ``"1,234,567"`` → ``1234567.0``
    - Period-separated thousands (European style): ``"1.234.567"`` → ``1234567.0``
    - Space-separated thousands: ``"1 234 567"`` → ``1234567.0``
    - Decimal values: ``"414.87"`` → ``414.87``
    - Mixed comma-thousands with decimal point: ``"1,234.56"`` → ``1234.56``
    - Citation markers (numeric or alpha): ``"1,234[1]"`` ``"1,234[a]"`` → ``1234.0``
    - Parenthetical qualifiers: ``"1,234 (estimate)"`` → ``1234.0``
    - Unit suffixes: ``"414.87 km2"`` ``"1,897,491 inhabitants"`` → stripped
    - Negative values are preserved: ``"-1.5"`` → ``-1.5``

    Returns ``None`` for:
    - Empty string or whitespace-only strings.
    - Strings that contain no digits after cleaning.
    - Strings that cannot be converted to float after all cleaning.

    No value is ever silently converted to ``0`` or an arbitrary default.

    Parameters
    ----------
    raw:
        Raw string value from a Wikipedia infobox cell.

    Returns
    -------
    float or None
        Parsed numeric value, or ``None`` if parsing is not possible.
    """
    if not raw or not raw.strip():
        return None

    # Step 1: Strip citation markers: [1], [a], [note 1], etc.
    cleaned = re.sub(r"\[.*?\]", "", raw)

    # Step 2: Strip parenthetical qualifiers: (estimate), (2020 census), etc.
    cleaned = re.sub(r"\(.*?\)", "", cleaned)

    # Step 3: Strip known unit suffixes (longest first to avoid partial matches)
    for suffix in _UNIT_SUFFIXES:
        cleaned = cleaned.replace(suffix, "")

    # Step 4: Strip remaining non-numeric characters except digits, dot, comma,
    # minus, and plus. Do this BEFORE deciding on separator style.
    cleaned = re.sub(r"[^\d.,\-]", " ", cleaned).strip()

    if not cleaned or not re.search(r"\d", cleaned):
        return None

    # Step 5: Collapse whitespace (space-separated thousands become one token
    # or multiple tokens; we join them without separator).
    # E.g. "1 234 567" after step 4 → "1 234 567" → after split/join → "1234567"
    tokens = cleaned.split()
    if len(tokens) > 1:
        # Space-separated thousands: join all tokens that are purely digit groups
        joined = "".join(tokens)
        # If all tokens are pure digits (no dots/commas), safe to join
        if all(re.match(r'^\d+$', t) for t in tokens):
            try:
                return float(joined)
            except ValueError:
                return None
        # Otherwise fall through with the first token that has digits
        cleaned = tokens[0]

    # Step 6: Detect period-as-thousands-separator vs decimal point.
    # Heuristic: if there are multiple dots and no comma, and all dot-separated
    # groups after the first are exactly 3 digits, treat dots as thousands separators.
    # Example: "1.234.567" → dots are grouping → remove them → 1234567
    # Example: "414.87" → single dot, 2-digit fraction → it is a decimal point
    dot_count = cleaned.count(".")
    comma_count = cleaned.count(",")

    if dot_count >= 2 and comma_count == 0:
        # Check if all segments after split on dot are 3 digits (thousands grouping)
        parts = cleaned.split(".")
        if all(len(p) == 3 and p.isdigit() for p in parts[1:]):
            # Period is a thousands separator: remove all dots
            cleaned = cleaned.replace(".", "")
    elif dot_count == 1 and comma_count >= 1:
        # Comma is thousands separator, dot is decimal point
        # E.g. "1,234.56" → remove commas → "1234.56"
        cleaned = cleaned.replace(",", "")
    elif dot_count == 0 and comma_count >= 1:
        # Comma is thousands separator only (no decimal part)
        # E.g. "1,234,567" → remove commas → "1234567"
        cleaned = cleaned.replace(",", "")
    elif dot_count == 1 and comma_count == 0:
        # Single dot: treat as decimal point, no change needed
        pass
    else:
        # Mixed or ambiguous: remove all commas, keep last dot as decimal
        cleaned = cleaned.replace(",", "")

    cleaned = cleaned.strip(". ")
    if not cleaned:
        return None

    try:
        return float(cleaned)
    except ValueError:
        return None


# Internal alias so existing code that calls _normalize_number keeps working
_normalize_number = normalize_number


def _get_infobox(soup: BeautifulSoup) -> Optional[object]:
    """Find the primary Wikipedia infobox table."""
    return soup.find("table", class_="infobox") or soup.find(
        "table", {"class": lambda c: c and "infobox" in c}
    )


def _parse_infobox_row(infobox, label_fragments: tuple[str, ...]) -> Optional[str]:
    """Find the first infobox row whose header text contains any of the label_fragments
    (case-insensitive) and return the cell text.
    Returns None if no matching row is found.
    """
    if infobox is None:
        return None
    for row in infobox.find_all("tr"):
        header = row.find("th")
        if header is None:
            continue
        header_text = header.get_text(separator=" ", strip=True).lower()
        if any(frag.lower() in header_text for frag in label_fragments):
            cell = row.find("td")
            if cell:
                return cell.get_text(separator=" ", strip=True)
    return None


def _parse_city_name(soup: BeautifulSoup, notes: list[str]) -> Optional[str]:
    """Extract city name from the Wikipedia page h1 title."""
    try:
        title_tag = soup.find("h1", id="firstHeading") or soup.find("h1")
        if title_tag:
            return title_tag.get_text(strip=True)
    except Exception as exc:  # noqa: BLE001
        notes.append(f"city_name parse error: {exc}")
    return None


def _parse_population(infobox, notes: list[str]) -> Optional[int]:
    """Extract and normalise population from the infobox."""
    try:
        pop_raw = _parse_infobox_row(infobox, ("population", "pop."))
        if pop_raw is not None:
            val = _normalize_number(pop_raw)
            if val is not None:
                return int(val)
            notes.append(f"population not parseable: {pop_raw!r}")
        else:
            notes.append("population row not found in infobox")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"population parse error: {exc}")
    return None


def _parse_area_km2(infobox, notes: list[str]) -> Optional[float]:
    """Extract and normalise area in km² from the infobox."""
    try:
        area_raw = _parse_infobox_row(infobox, ("area", "km"))
        if area_raw is not None:
            val = _normalize_number(area_raw)
            if val is not None:
                return val
            notes.append(f"area_km2 not parseable: {area_raw!r}")
        else:
            notes.append("area row not found in infobox")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"area_km2 parse error: {exc}")
    return None


def _parse_population_density(
    infobox,
    population: Optional[int],
    area_km2: Optional[float],
    notes: list[str],
) -> Optional[float]:
    """Derive or parse population density.

    Computes density from population / area_km2 when both are available.
    Falls back to parsing the density row directly from the infobox.
    Returns None if density cannot be determined.
    """
    try:
        if population is not None and area_km2 is not None and area_km2 > 0:
            return round(population / area_km2, 2)
        density_raw = _parse_infobox_row(infobox, ("density", "pop. density"))
        if density_raw is not None:
            val = _normalize_number(density_raw)
            if val is not None:
                return val
            notes.append(f"population_density not parseable: {density_raw!r}")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"population_density parse error: {exc}")
    return None


def _parse_country_name(infobox, notes: list[str]) -> Optional[str]:
    """Extract country name from the infobox."""
    try:
        country_raw = _parse_infobox_row(infobox, ("country", "nation", "state"))
        if country_raw is not None:
            return country_raw.split()[0] if country_raw else None
        notes.append("country row not found in infobox")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"country parse error: {exc}")
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def fetch_and_save_html(
    city_id: str,
    wikipedia_url: str,
    output_dir: Path = DEFAULT_HTML_DIR,
    delay_seconds: float = MIN_REQUEST_DELAY_SECONDS,
) -> Path:
    """Fetch a Wikipedia city page and save raw HTML locally.

    Parameters
    ----------
    city_id:
        Canonical city identifier used as the output filename stem.
    wikipedia_url:
        Full Wikipedia page URL, e.g. https://en.wikipedia.org/wiki/Vienna.
    output_dir:
        Directory for raw HTML files. Created if it does not exist.
    delay_seconds:
        Minimum pause before the request to respect Wikipedia's usage policy.

    Returns
    -------
    Path
        Path to the saved HTML file (<output_dir>/<city_id>.html).

    Raises
    ------
    requests.HTTPError
        If the Wikipedia page returns a non-2xx HTTP status.
    """
    time.sleep(delay_seconds)
    response = requests.get(
        wikipedia_url,
        headers={"User-Agent": USER_AGENT},
        timeout=15,
    )
    response.raise_for_status()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / f"{city_id}.html"
    html_path.write_text(response.text, encoding="utf-8")
    logger.info("Saved HTML for %s to %s", city_id, html_path)
    return html_path


def parse_city_metadata(
    city_id: str,
    wikipedia_url: str,
    html: str,
) -> dict:
    """Parse Wikipedia HTML and extract city metadata into a structured record.

    Always returns a complete record with all schema fields present.
    Parsing failures for individual fields are caught and recorded in
    ``metadata_notes`` rather than raising exceptions.

    Parameters
    ----------
    city_id:
        Canonical city identifier from city_reference.parquet.
    wikipedia_url:
        Source URL used for traceability.
    html:
        Raw Wikipedia page HTML string.

    Returns
    -------
    dict
        Record with keys matching METADATA_COLUMNS. ``city_id`` is always
        non-null. Nullable fields are None when not parseable.
    """
    record = _empty_record(city_id, wikipedia_url)
    notes: list[str] = []

    if not html or not html.strip():
        record["metadata_notes"] = "empty html"
        return record

    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception as exc:  # noqa: BLE001
        record["metadata_notes"] = f"html parse error: {exc}"
        return record

    record["city_name"] = _parse_city_name(soup, notes)

    infobox = _get_infobox(soup)
    if infobox is None:
        notes.append("infobox not found")

    record["population"] = _parse_population(infobox, notes)
    record["area_km2"] = _parse_area_km2(infobox, notes)
    record["population_density"] = _parse_population_density(
        infobox, record["population"], record["area_km2"], notes
    )
    record["country"] = _parse_country_name(infobox, notes)

    record["metadata_notes"] = "; ".join(notes) if notes else "ok"
    return record


def parse_city_metadata_from_file(
    city_id: str,
    wikipedia_url: str,
    html_path: Path,
) -> dict:
    """Parse metadata from a locally saved HTML file.

    Convenience wrapper around :func:`parse_city_metadata` for use with
    cached HTML files. Returns an empty record with an error note if the
    file does not exist.
    """
    html_path = Path(html_path)
    if not html_path.exists():
        record = _empty_record(city_id, wikipedia_url)
        record["metadata_notes"] = f"html file not found: {html_path}"
        return record
    html = html_path.read_text(encoding="utf-8")
    return parse_city_metadata(city_id, wikipedia_url, html)
