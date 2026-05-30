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


def _normalize_number(raw: str) -> Optional[float]:
    """Strip non-numeric noise from a Wikipedia infobox value string.

    Handles: comma/period thousands separators, citation markers [1],
    parenthetical qualifiers, unit suffixes, and whitespace.
    Returns None when the value cannot be parsed.
    """
    if not raw or not raw.strip():
        return None
    cleaned = re.sub(r"\[.*?\]", "", raw)          # strip citations [1]
    cleaned = re.sub(r"\(.*?\)", "", cleaned)        # strip parenthetical
    # Remove known unit suffixes
    for suffix in ("km2", "km²", "/km2", "/km²", "inhabitants", "people", "pop."):
        cleaned = cleaned.replace(suffix, "")
    cleaned = re.sub(r"[^\d.,\-]", "", cleaned)      # keep digits, separators, minus
    cleaned = cleaned.replace(",", "")               # remove thousands commas
    cleaned = cleaned.strip(". ")
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


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

    # --- city_name from page title ---
    try:
        title_tag = soup.find("h1", id="firstHeading") or soup.find("h1")
        if title_tag:
            record["city_name"] = title_tag.get_text(strip=True)
    except Exception as exc:  # noqa: BLE001
        notes.append(f"city_name parse error: {exc}")

    # --- infobox ---
    infobox = _get_infobox(soup)
    if infobox is None:
        notes.append("infobox not found")

    # --- population ---
    try:
        pop_raw = _parse_infobox_row(infobox, ("population", "pop."))
        if pop_raw is not None:
            val = _normalize_number(pop_raw)
            if val is not None:
                record["population"] = int(val)
            else:
                notes.append(f"population not parseable: {pop_raw!r}")
        else:
            notes.append("population row not found in infobox")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"population parse error: {exc}")

    # --- area ---
    try:
        area_raw = _parse_infobox_row(infobox, ("area", "km"))
        if area_raw is not None:
            val = _normalize_number(area_raw)
            if val is not None:
                record["area_km2"] = val
            else:
                notes.append(f"area_km2 not parseable: {area_raw!r}")
        else:
            notes.append("area row not found in infobox")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"area_km2 parse error: {exc}")

    # --- population_density ---
    try:
        if record["population"] is not None and record["area_km2"] is not None and record["area_km2"] > 0:
            record["population_density"] = round(record["population"] / record["area_km2"], 2)
        else:
            # Try to parse directly from infobox
            density_raw = _parse_infobox_row(infobox, ("density", "pop. density"))
            if density_raw is not None:
                val = _normalize_number(density_raw)
                if val is not None:
                    record["population_density"] = val
                else:
                    notes.append(f"population_density not parseable: {density_raw!r}")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"population_density parse error: {exc}")

    # --- country ---
    try:
        country_raw = _parse_infobox_row(infobox, ("country", "nation", "state"))
        if country_raw is not None:
            record["country"] = country_raw.split()[0] if country_raw else None
        else:
            notes.append("country row not found in infobox")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"country parse error: {exc}")

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
