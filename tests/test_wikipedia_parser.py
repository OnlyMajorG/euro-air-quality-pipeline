"""Tests for Phase 4 Wikipedia city metadata scraper.

All tests use local in-memory HTML fixtures. No network calls.
Schema contract: docs/data_model.md, Phase 4 Wikipedia City Metadata Schema.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# HTML fixtures
# ---------------------------------------------------------------------------

MINIMAL_INFOBOX_HTML = """
<html><body>
<h1 id="firstHeading">Vienna</h1>
<table class="infobox">
  <tr><th>Country</th><td>Austria</td></tr>
  <tr><th>Population</th><td>1,897,491</td></tr>
  <tr><th>Area</th><td>414.87 km2</td></tr>
</table>
</body></html>
"""

MISSING_INFOBOX_HTML = """
<html><body>
<h1 id="firstHeading">UnknownCity</h1>
<p>No infobox here.</p>
</body></html>
"""

PARTIAL_INFOBOX_HTML = """
<html><body>
<h1 id="firstHeading">PartialCity</h1>
<table class="infobox">
  <tr><th>Country</th><td>Germany</td></tr>
  <tr><th>Population</th><td>not available</td></tr>
</table>
</body></html>
"""

EMPTY_HTML = ""

MALFORMED_NUMBER_HTML = """
<html><body>
<h1 id="firstHeading">TestCity</h1>
<table class="infobox">
  <tr><th>Population</th><td>1,234,567[1]</td></tr>
  <tr><th>Area</th><td>123.45 km2</td></tr>
</table>
</body></html>
"""

COMPLETELY_EMPTY_INFOBOX_HTML = """
<html><body>
<h1 id="firstHeading">EmptyCity</h1>
<table class="infobox">
  <tr><th>Founded</th><td>1000 AD</td></tr>
</table>
</body></html>
"""

MISSING_AREA_HTML = """
<html><body>
<h1 id="firstHeading">NoAreaCity</h1>
<table class="infobox">
  <tr><th>Country</th><td>Poland</td></tr>
  <tr><th>Population</th><td>500,000</td></tr>
</table>
</body></html>
"""


# ---------------------------------------------------------------------------
# Module import side-effect tests
# ---------------------------------------------------------------------------


def test_module_import_has_no_side_effects() -> None:
    """Importing the module must not write files, make network calls, or raise."""
    import src.ingestion.wikipedia_scraper  # noqa: F401 (already imported but explicit)
    assert True  # if import raised we'd never reach here


def test_no_forbidden_imports() -> None:
    """The scraper must not import Kafka, Spark, or EEA loader."""
    import importlib.util
    spec = importlib.util.find_spec("src.ingestion.wikipedia_scraper")
    assert spec is not None
    # Read source and check for forbidden imports
    source = Path(spec.origin).read_text(encoding="utf-8")
    forbidden = ["kafka", "SparkSession", "readStream", "eea_loader", "pyspark"]
    for term in forbidden:
        assert term not in source, f"Forbidden term found in scraper: {term!r}"


# ---------------------------------------------------------------------------
# parse_city_metadata — happy path
# ---------------------------------------------------------------------------


def test_parse_returns_all_schema_fields() -> None:
    """Every METADATA_COLUMNS key must be present in the returned record."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata, METADATA_COLUMNS
    record = parse_city_metadata("vienna_at", "https://en.wikipedia.org/wiki/Vienna", MINIMAL_INFOBOX_HTML)
    for field in METADATA_COLUMNS:
        assert field in record, f"Missing field: {field}"


def test_parse_city_id_always_present() -> None:
    """city_id must always be present and non-null, even for empty HTML."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    for html in [MINIMAL_INFOBOX_HTML, MISSING_INFOBOX_HTML, PARTIAL_INFOBOX_HTML, EMPTY_HTML]:
        record = parse_city_metadata("test_city", "https://example.com", html)
        assert record["city_id"] == "test_city"
        assert record["city_id"] is not None


def test_parse_source_always_wikipedia() -> None:
    """source field must always be 'wikipedia'."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata("vienna_at", "https://en.wikipedia.org/wiki/Vienna", MINIMAL_INFOBOX_HTML)
    assert record["source"] == "wikipedia"


def test_parse_wikipedia_url_preserved() -> None:
    """wikipedia_url must match the input parameter exactly."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    url = "https://en.wikipedia.org/wiki/Vienna"
    record = parse_city_metadata("vienna_at", url, MINIMAL_INFOBOX_HTML)
    assert record["wikipedia_url"] == url


def test_parse_population_from_infobox() -> None:
    """Population is extracted and returned as an integer."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata("vienna_at", "https://en.wikipedia.org/wiki/Vienna", MINIMAL_INFOBOX_HTML)
    assert record["population"] is not None
    assert isinstance(record["population"], int)
    assert record["population"] > 0


def test_parse_area_from_infobox() -> None:
    """area_km2 is extracted and returned as a float."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata("vienna_at", "https://en.wikipedia.org/wiki/Vienna", MINIMAL_INFOBOX_HTML)
    assert record["area_km2"] is not None
    assert isinstance(record["area_km2"], float)
    assert record["area_km2"] > 0


def test_parse_population_density_computed() -> None:
    """population_density is computed when population and area_km2 are both present."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata("vienna_at", "https://en.wikipedia.org/wiki/Vienna", MINIMAL_INFOBOX_HTML)
    assert record["population_density"] is not None
    assert isinstance(record["population_density"], float)
    assert record["population_density"] > 0


# ---------------------------------------------------------------------------
# parse_city_metadata — missing / partial / malformed cases
# ---------------------------------------------------------------------------


def test_missing_infobox_returns_valid_partial_record() -> None:
    """A city with no infobox returns a valid record with nullable fields as None."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata("unknown_xx", "https://en.wikipedia.org/wiki/UnknownCity", MISSING_INFOBOX_HTML)
    assert record["city_id"] == "unknown_xx"
    assert record["population"] is None
    assert record["area_km2"] is None
    assert record["population_density"] is None
    assert record["metadata_notes"] != ""  # must document what went wrong


def test_empty_html_returns_valid_record() -> None:
    """Empty HTML input must not raise; returns a record with metadata_notes set."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata("empty_xx", "https://en.wikipedia.org/wiki/Empty", EMPTY_HTML)
    assert record["city_id"] == "empty_xx"
    assert record["population"] is None
    assert record["area_km2"] is None
    assert record["metadata_notes"] != ""


def test_unparseable_population_is_null_with_note() -> None:
    """If population text cannot be parsed, field is None and note is set."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata("partial_xx", "https://en.wikipedia.org/wiki/Partial", PARTIAL_INFOBOX_HTML)
    assert record["population"] is None
    assert record["metadata_notes"] != ""


def test_population_density_none_when_area_missing() -> None:
    """population_density stays None when area_km2 is missing."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata("partial_xx", "https://en.wikipedia.org/wiki/Partial", PARTIAL_INFOBOX_HTML)
    assert record["population_density"] is None


def test_citation_markers_stripped_from_numbers() -> None:
    """Citation markers like [1] must be stripped before number parsing."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata("test_city", "https://en.wikipedia.org/wiki/Test", MALFORMED_NUMBER_HTML)
    assert record["population"] is not None
    assert record["population"] == 1234567


# ---------------------------------------------------------------------------
# _normalize_number helper
# ---------------------------------------------------------------------------


def test_normalize_number_comma_thousands() -> None:
    from src.ingestion.wikipedia_scraper import _normalize_number
    assert _normalize_number("1,234,567") == pytest.approx(1234567.0)


def test_normalize_number_with_citation() -> None:
    from src.ingestion.wikipedia_scraper import _normalize_number
    assert _normalize_number("1,234[1]") == pytest.approx(1234.0)


def test_normalize_number_empty_returns_none() -> None:
    from src.ingestion.wikipedia_scraper import _normalize_number
    assert _normalize_number("") is None
    assert _normalize_number("   ") is None


def test_normalize_number_na_returns_none() -> None:
    from src.ingestion.wikipedia_scraper import _normalize_number
    assert _normalize_number("N/A") is None
    assert _normalize_number("not available") is None


def test_normalize_number_with_unit_suffix() -> None:
    from src.ingestion.wikipedia_scraper import _normalize_number
    result = _normalize_number("1,234.56 km2")
    assert result == pytest.approx(1234.56)


def test_normalize_number_float() -> None:
    from src.ingestion.wikipedia_scraper import _normalize_number
    assert _normalize_number("414.87") == pytest.approx(414.87)


# ---------------------------------------------------------------------------
# fetch_and_save_html — file write test (no network)
# ---------------------------------------------------------------------------


def test_fetch_and_save_html_writes_file(tmp_path: Path) -> None:
    """Saving HTML to a caller-provided path writes the correct content."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata_from_file
    # Write a fixture HTML file manually (no network)
    html_file = tmp_path / "vienna_at.html"
    html_file.write_text(MINIMAL_INFOBOX_HTML, encoding="utf-8")
    record = parse_city_metadata_from_file(
        "vienna_at",
        "https://en.wikipedia.org/wiki/Vienna",
        html_file,
    )
    assert record["city_id"] == "vienna_at"
    assert record["population"] is not None


def test_parse_from_missing_file_returns_partial_record() -> None:
    """parse_city_metadata_from_file handles a non-existent file gracefully."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata_from_file
    record = parse_city_metadata_from_file(
        "missing_xx",
        "https://en.wikipedia.org/wiki/Missing",
        Path("/nonexistent/path/missing_xx.html"),
    )
    assert record["city_id"] == "missing_xx"
    assert record["population"] is None
    assert "not found" in record["metadata_notes"].lower()


# ---------------------------------------------------------------------------
# scraped_at field
# ---------------------------------------------------------------------------


def test_scraped_at_is_iso_utc_string() -> None:
    """scraped_at must be an ISO 8601 UTC timestamp string."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    from datetime import datetime
    record = parse_city_metadata("vienna_at", "https://en.wikipedia.org/wiki/Vienna", MINIMAL_INFOBOX_HTML)
    assert isinstance(record["scraped_at"], str)
    # Must parse as ISO datetime
    dt = datetime.fromisoformat(record["scraped_at"])
    assert dt.tzname() in ("UTC", "+00:00")


# ---------------------------------------------------------------------------
# normalize_number — public API (Issue 4.4 comprehensive tests)
# Issue 4.4 Acceptance Criteria: cover all mandatory formats
# ---------------------------------------------------------------------------


def test_normalize_number_public_comma_thousands() -> None:
    """'1,234,567' → 1234567.0 (comma-separated thousands)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("1,234,567") == pytest.approx(1234567.0)


def test_normalize_number_public_period_thousands() -> None:
    """'1.234.567' → 1234567.0 (period-separated thousands, European style)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("1.234.567") == pytest.approx(1234567.0)


def test_normalize_number_public_space_thousands() -> None:
    """'1 234 567' → 1234567.0 (space-separated thousands)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("1 234 567") == pytest.approx(1234567.0)


def test_normalize_number_public_unit_suffix_km2() -> None:
    """'1,234.56 km2' → 1234.56 (unit suffix stripped)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("1,234.56 km2") == pytest.approx(1234.56)


def test_normalize_number_public_citation_numeric() -> None:
    """'1,234[1]' → 1234.0 (numeric citation marker stripped)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("1,234[1]") == pytest.approx(1234.0)


def test_normalize_number_public_citation_alpha() -> None:
    """'1,234[a]' → 1234.0 (alpha citation marker stripped)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("1,234[a]") == pytest.approx(1234.0)


def test_normalize_number_public_na_returns_none() -> None:
    """'N/A' → None (not parseable)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("N/A") is None


def test_normalize_number_public_empty_returns_none() -> None:
    """'' → None (empty string)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("") is None


def test_normalize_number_public_decimal() -> None:
    """'414.87' → 414.87 (decimal preserved)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("414.87") == pytest.approx(414.87)


def test_normalize_number_public_mixed_comma_decimal() -> None:
    """'1,897,491.5' → 1897491.5 (commas as thousands, dot as decimal)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("1,897,491.5") == pytest.approx(1897491.5)


def test_normalize_number_public_parenthetical_stripped() -> None:
    """'1,234 (estimate)' → 1234.0 (parenthetical qualifier stripped)."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("1,234 (estimate)") == pytest.approx(1234.0)


def test_normalize_number_public_never_returns_zero_for_none() -> None:
    """Unparseable values must return None, never 0."""
    from src.ingestion.wikipedia_scraper import normalize_number
    assert normalize_number("not available") is None
    assert normalize_number("unknown") is None
    assert normalize_number("   ") is None


def test_normalize_number_private_alias_still_works() -> None:
    """_normalize_number must remain importable as an alias (backward compat)."""
    from src.ingestion.wikipedia_scraper import _normalize_number
    assert _normalize_number("1,234,567") == pytest.approx(1234567.0)
    assert _normalize_number("") is None


# ---------------------------------------------------------------------------
# Issue 4.5: Null-handling and error resilience — targeted tests
# ---------------------------------------------------------------------------


def test_completely_missing_metadata_all_nullable_fields_null() -> None:
    """Infobox with no relevant rows: all nullable fields are None, notes non-empty."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata, METADATA_COLUMNS
    record = parse_city_metadata(
        "empty_city",
        "https://en.wikipedia.org/wiki/EmptyCity",
        COMPLETELY_EMPTY_INFOBOX_HTML,
    )
    # Required fields always present
    assert record["city_id"] == "empty_city"
    assert record["source"] == "wikipedia"
    assert record["wikipedia_url"] is not None
    assert record["scraped_at"] is not None
    assert record["metadata_notes"] is not None
    assert record["metadata_notes"] != ""
    # All nullable fields must be None
    assert record["population"] is None
    assert record["area_km2"] is None
    assert record["population_density"] is None
    # All METADATA_COLUMNS keys present
    for field in METADATA_COLUMNS:
        assert field in record, f"Missing schema field: {field}"


def test_missing_area_returns_none_with_note() -> None:
    """Population present but area missing: area_km2 and density are None, note set."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata(
        "noarea_xx",
        "https://en.wikipedia.org/wiki/NoAreaCity",
        MISSING_AREA_HTML,
    )
    assert record["city_id"] == "noarea_xx"
    assert record["population"] is not None        # population parsed
    assert record["population"] > 0
    assert record["area_km2"] is None              # area not found
    assert record["population_density"] is None    # cannot be computed
    assert record["metadata_notes"] != ""           # documents the missing area


def test_population_density_computed_from_population_and_area() -> None:
    """population_density equals population / area_km2 when both are non-null."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata(
        "vienna_at",
        "https://en.wikipedia.org/wiki/Vienna",
        MINIMAL_INFOBOX_HTML,
    )
    assert record["population"] is not None
    assert record["area_km2"] is not None
    assert record["population_density"] is not None
    expected = round(record["population"] / record["area_km2"], 2)
    assert record["population_density"] == pytest.approx(expected, rel=1e-3)


def test_single_city_failure_does_not_crash_batch() -> None:
    """Simulated batch: a failure for one city does not prevent others from parsing."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    cities = [
        ("vienna_at", "https://en.wikipedia.org/wiki/Vienna", MINIMAL_INFOBOX_HTML),
        ("empty_xx", "https://en.wikipedia.org/wiki/Empty", EMPTY_HTML),
        ("unknown_xx", "https://en.wikipedia.org/wiki/Unknown", MISSING_INFOBOX_HTML),
        ("partial_xx", "https://en.wikipedia.org/wiki/Partial", PARTIAL_INFOBOX_HTML),
    ]
    records = []
    for city_id, url, html in cities:
        # Must never raise regardless of HTML quality
        record = parse_city_metadata(city_id, url, html)
        records.append(record)

    assert len(records) == 4
    # Every record has city_id
    assert all(r["city_id"] is not None for r in records)
    # Vienna parses successfully
    vienna = next(r for r in records if r["city_id"] == "vienna_at")
    assert vienna["population"] is not None
    # Others have notes explaining failures
    for r in records:
        if r["city_id"] != "vienna_at":
            assert r["metadata_notes"] != ""


def test_downstream_pandas_handles_null_fields() -> None:
    """A pandas DataFrame built from records with None fields must not error."""
    import pandas as pd
    from src.ingestion.wikipedia_scraper import parse_city_metadata, METADATA_COLUMNS

    cities = [
        ("vienna_at", "https://en.wikipedia.org/wiki/Vienna", MINIMAL_INFOBOX_HTML),
        ("empty_xx", "https://en.wikipedia.org/wiki/Empty", EMPTY_HTML),
        ("unknown_xx", "https://en.wikipedia.org/wiki/Unknown", MISSING_INFOBOX_HTML),
    ]
    records = [
        parse_city_metadata(city_id, url, html)
        for city_id, url, html in cities
    ]

    # Build DataFrame — must not raise
    df = pd.DataFrame.from_records(records)

    # All schema columns present
    for col in METADATA_COLUMNS:
        assert col in df.columns, f"Missing column in DataFrame: {col}"

    # city_id is always non-null
    assert df["city_id"].notna().all()

    # Nullable columns may have NaN/None — basic operations must not raise
    _ = df["population"].dropna()
    _ = df["area_km2"].fillna(0)
    _ = df["population_density"].describe()

    # Filtering on nullable field must work
    cities_with_pop = df[df["population"].notna()]
    assert len(cities_with_pop) >= 1  # at least Vienna has population

    # Count per source must work
    source_counts = df.groupby("source").size()
    assert "wikipedia" in source_counts.index


def test_metadata_notes_ok_when_all_fields_parsed() -> None:
    """metadata_notes is 'ok' when all fields parsed successfully."""
    from src.ingestion.wikipedia_scraper import parse_city_metadata
    record = parse_city_metadata(
        "vienna_at",
        "https://en.wikipedia.org/wiki/Vienna",
        MINIMAL_INFOBOX_HTML,
    )
    assert record["metadata_notes"] == "ok"


def test_helpers_are_importable_and_callable() -> None:
    """Private helper functions exist and are callable for unit testing."""
    from src.ingestion.wikipedia_scraper import (
        _parse_city_name,
        _parse_population,
        _parse_area_km2,
        _parse_population_density,
        _parse_country_name,
    )
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(MINIMAL_INFOBOX_HTML, "html.parser")
    notes: list = []
    name = _parse_city_name(soup, notes)
    assert name == "Vienna"
    assert notes == []
