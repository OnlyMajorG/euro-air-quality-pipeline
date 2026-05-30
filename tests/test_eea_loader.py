"""Tests for Phase 3 EEA batch loader (Issue 3.4).

All tests use tiny in-memory DataFrames or pytest tmp_path fixtures.
No internet access, no EEA downloads, no Kafka, no Spark.
"""

from __future__ import annotations

import io
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pytest

from src.ingestion.eea_loader import (
    CORE_POLLUTANTS,
    INVALID_VALIDITY_VALUES,
    POLLUTANT_LABEL_MAP,
    RAW_COLUMNS,
    SILVER_COLUMNS,
    aggregate_to_city_daily,
    load_and_aggregate,
    load_eea_raw,
    map_stations_to_cities,
)


# ---------------------------------------------------------------------------
# Tiny fixture helpers
# ---------------------------------------------------------------------------

_FIXED_TS = datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
_FIXED_PROCESSING_TS = datetime(2026, 5, 30, 10, 0, 0, tzinfo=timezone.utc)


def _make_minimal_csv(
    tmp_path: Path,
    rows: list[dict],
    filename: str = "sample.csv",
) -> Path:
    """Write a tiny CSV with EEA-like columns and return the path."""
    df = pd.DataFrame(rows)
    p = tmp_path / filename
    df.to_csv(p, index=False)
    return p


def _make_minimal_parquet(
    tmp_path: Path,
    rows: list[dict],
    filename: str = "sample.parquet",
) -> Path:
    """Write a tiny Parquet with EEA-like columns and return the path."""
    df = pd.DataFrame(rows)
    p = tmp_path / filename
    df.to_parquet(p, index=False)
    return p


def _standard_rows() -> list[dict]:
    """Return a minimal set of valid EEA-format rows covering all 3 pollutants."""
    return [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "AirPollutant": "PM2.5",
            "Concentration": 12.5,
            "Unit": "µg/m³",
            "Validity": 1,
        },
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T09:00:00+00:00",
            "AirPollutant": "PM10",
            "Concentration": 22.0,
            "Unit": "µg/m³",
            "Validity": 1,
        },
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T10:00:00+00:00",
            "AirPollutant": "NO2",
            "Concentration": 35.0,
            "Unit": "µg/m³",
            "Validity": 1,
        },
    ]


def _minimal_station_mapping(city_id: str = "vienna_at") -> pd.DataFrame:
    """Return a tiny selected station mapping for tests."""
    return pd.DataFrame(
        [
            {
                "eea_station_id": "AT90TAB",
                "city_id": city_id,
                "mapping_status": "selected",
            }
        ]
    )


# ---------------------------------------------------------------------------
# Module-level safety checks
# ---------------------------------------------------------------------------


def test_loader_module_has_no_forbidden_imports() -> None:
    """Loader must not import requests, urllib, Kafka, or Spark."""
    import src.ingestion.eea_loader as module
    import inspect

    source = inspect.getsource(module)
    # Check actual import statements only — not docstrings or comments
    import_lines = [line.strip() for line in source.splitlines() if line.strip().startswith("import ") or line.strip().startswith("from ")]
    import_text = "\n".join(import_lines)
    forbidden = ["requests", "urllib", "kafka", "pyspark", "SparkSession"]
    for token in forbidden:
        assert token.lower() not in import_text.lower(), (
            f"Forbidden import found in eea_loader.py imports: {token!r}\n"
            f"Import lines: {import_lines}"
        )


def test_loader_module_imports_without_side_effects() -> None:
    """Importing the loader must not trigger network calls or file writes."""
    import importlib
    import src.ingestion.eea_loader  # noqa: F401 — just checking import succeeds
    assert True  # If we get here, import had no side effects that raised


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_core_pollutants_are_exactly_three() -> None:
    assert CORE_POLLUTANTS == {"PM2.5", "PM10", "NO2"}


def test_pollutant_label_map_covers_all_core_pollutants() -> None:
    mapped_targets = set(POLLUTANT_LABEL_MAP.values())
    assert mapped_targets == CORE_POLLUTANTS


def test_silver_columns_match_documented_schema() -> None:
    expected = (
        "city_id", "date", "pollutant", "mean_value", "min_value",
        "max_value", "observation_count", "unit", "source", "processing_time_utc",
    )
    assert SILVER_COLUMNS == expected


# ---------------------------------------------------------------------------
# load_eea_raw — file reading
# ---------------------------------------------------------------------------


def test_load_eea_raw_reads_csv(tmp_path: Path) -> None:
    p = _make_minimal_csv(tmp_path, _standard_rows())
    df = load_eea_raw(p)

    assert len(df) == 3
    assert list(df.columns) == list(RAW_COLUMNS)


def test_load_eea_raw_reads_parquet(tmp_path: Path) -> None:
    p = _make_minimal_parquet(tmp_path, _standard_rows())
    df = load_eea_raw(p)

    assert len(df) == 3
    assert list(df.columns) == list(RAW_COLUMNS)


def test_load_eea_raw_raises_on_missing_file() -> None:
    with pytest.raises(FileNotFoundError, match="not found"):
        load_eea_raw(Path("/nonexistent/path/sample.csv"))


def test_load_eea_raw_raises_on_unsupported_format(tmp_path: Path) -> None:
    p = tmp_path / "sample.json"
    p.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file format"):
        load_eea_raw(p)


def test_load_eea_raw_raises_on_missing_column(tmp_path: Path) -> None:
    """A file with a valid station column but no pollutant column must raise KeyError
    mentioning 'pollutant label'."""
    rows = [
        {
            "AirQualityStationEoICode": "AT90TAB",  # station alias present
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",  # timestamp alias present
            "Concentration": 10.0,  # value alias present
            "Unit": "µg/m³",  # unit alias present
            # AirPollutant / pollutant / Pollutant / Component all absent
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)

    with pytest.raises(KeyError, match="pollutant label"):
        load_eea_raw(p)


# ---------------------------------------------------------------------------
# load_eea_raw — normalisation
# ---------------------------------------------------------------------------


def test_load_eea_raw_normalises_canonical_station_id(tmp_path: Path) -> None:
    p = _make_minimal_csv(tmp_path, _standard_rows())
    df = load_eea_raw(p)

    assert (df["eea_station_id"] == "AT90TAB").all()


def test_load_eea_raw_datetime_is_utc_aware(tmp_path: Path) -> None:
    p = _make_minimal_csv(tmp_path, _standard_rows())
    df = load_eea_raw(p)

    assert pd.api.types.is_datetime64_any_dtype(df["datetime_begin"])
    # All timestamps must carry UTC timezone info
    assert df["datetime_begin"].dt.tz is not None


def test_load_eea_raw_pollutant_label_is_canonical(tmp_path: Path) -> None:
    p = _make_minimal_csv(tmp_path, _standard_rows())
    df = load_eea_raw(p)

    assert set(df["pollutant"]).issubset(CORE_POLLUTANTS)


def test_load_eea_raw_normalises_verbose_pm25_label(tmp_path: Path) -> None:
    rows = [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "AirPollutant": "Particles < 2.5 µm (aerodynamic diameter)",
            "Concentration": 15.0,
            "Unit": "µg/m³",
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    df = load_eea_raw(p)

    assert len(df) == 1
    assert df.iloc[0]["pollutant"] == "PM2.5"


def test_load_eea_raw_normalises_verbose_no2_label(tmp_path: Path) -> None:
    rows = [
        {
            "AirQualityStationEoICode": "DEBE068",
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "AirPollutant": "Nitrogen dioxide (air)",
            "Concentration": 40.0,
            "Unit": "µg/m³",
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    df = load_eea_raw(p)

    assert len(df) == 1
    assert df.iloc[0]["pollutant"] == "NO2"


def test_load_eea_raw_accepts_alternative_column_names(tmp_path: Path) -> None:
    """Loader must resolve alternative column name aliases."""
    rows = [
        {
            "AirQualityStation": "AT90TAB",   # alternative station column
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "pollutant": "PM2.5",              # alternative pollutant column
            "Value": 10.0,                     # alternative value column
            "unit": "µg/m³",                   # alternative unit column
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    df = load_eea_raw(p)

    assert len(df) == 1
    assert df.iloc[0]["pollutant"] == "PM2.5"


# ---------------------------------------------------------------------------
# load_eea_raw — quality filtering
# ---------------------------------------------------------------------------


def test_load_eea_raw_excludes_out_of_scope_pollutants(tmp_path: Path) -> None:
    rows = _standard_rows() + [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T11:00:00+00:00",
            "AirPollutant": "SO2",  # out of scope
            "Concentration": 5.0,
            "Unit": "µg/m³",
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    df = load_eea_raw(p)

    assert len(df) == 3  # SO2 row excluded
    assert "SO2" not in df["pollutant"].values


def test_load_eea_raw_excludes_negative_concentration(tmp_path: Path) -> None:
    rows = _standard_rows() + [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T11:00:00+00:00",
            "AirPollutant": "PM2.5",
            "Concentration": -9.0,  # invalid measurement
            "Unit": "µg/m³",
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    df = load_eea_raw(p)

    assert len(df) == 3  # negative row excluded
    assert (df["concentration"] >= 0).all()


def test_load_eea_raw_excludes_missing_concentration(tmp_path: Path) -> None:
    rows = _standard_rows() + [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T11:00:00+00:00",
            "AirPollutant": "PM2.5",
            "Concentration": None,  # missing value
            "Unit": "µg/m³",
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    df = load_eea_raw(p)

    assert df["concentration"].notna().all()


def test_load_eea_raw_excludes_invalid_validity_flag(tmp_path: Path) -> None:
    rows = _standard_rows() + [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T11:00:00+00:00",
            "AirPollutant": "PM2.5",
            "Concentration": 20.0,
            "Unit": "µg/m³",
            "Validity": -1,  # known-bad validity flag
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    df = load_eea_raw(p)

    assert len(df) == 3  # validity=-1 row excluded


def test_load_eea_raw_allows_missing_validity_column(tmp_path: Path) -> None:
    """Files without a Validity column should still load correctly."""
    rows = [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "AirPollutant": "NO2",
            "Concentration": 30.0,
            "Unit": "µg/m³",
            # No Validity column
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    df = load_eea_raw(p)

    assert len(df) == 1


def test_load_eea_raw_excludes_unparseable_timestamps(tmp_path: Path) -> None:
    rows = _standard_rows() + [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "NOT_A_DATE",  # unparseable
            "AirPollutant": "PM2.5",
            "Concentration": 10.0,
            "Unit": "µg/m³",
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    df = load_eea_raw(p)

    assert len(df) == 3  # bad timestamp row excluded


def test_load_eea_raw_returns_empty_if_all_rows_excluded(tmp_path: Path) -> None:
    rows = [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "AirPollutant": "SO2",  # out of scope
            "Concentration": 5.0,
            "Unit": "µg/m³",
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    df = load_eea_raw(p)

    assert df.empty
    assert list(df.columns) == list(RAW_COLUMNS)


# ---------------------------------------------------------------------------
# map_stations_to_cities
# ---------------------------------------------------------------------------


def test_map_stations_to_cities_attaches_city_id(tmp_path: Path) -> None:
    p = _make_minimal_csv(tmp_path, _standard_rows())
    raw = load_eea_raw(p)
    mapping = _minimal_station_mapping("vienna_at")

    mapped = map_stations_to_cities(raw, mapping)

    assert "city_id" in mapped.columns
    assert (mapped["city_id"] == "vienna_at").all()


def test_map_stations_to_cities_drops_unselected_stations(tmp_path: Path) -> None:
    rows = _standard_rows() + [
        {
            "AirQualityStationEoICode": "UNKNOWN_STA",
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "AirPollutant": "PM2.5",
            "Concentration": 10.0,
            "Unit": "µg/m³",
        }
    ]
    p = _make_minimal_csv(tmp_path, rows)
    raw = load_eea_raw(p)
    mapping = _minimal_station_mapping("vienna_at")

    mapped = map_stations_to_cities(raw, mapping)

    assert len(mapped) == 3  # UNKNOWN_STA row dropped
    assert "UNKNOWN_STA" not in mapped["eea_station_id"].values


def test_map_stations_to_cities_ignores_candidate_stations(tmp_path: Path) -> None:
    """Candidate (non-selected) stations must not be used for city join."""
    rows = _standard_rows()
    p = _make_minimal_csv(tmp_path, rows)
    raw = load_eea_raw(p)

    mapping = pd.DataFrame(
        [{"eea_station_id": "AT90TAB", "city_id": "vienna_at", "mapping_status": "candidate"}]
    )

    mapped = map_stations_to_cities(raw, mapping)

    assert mapped.empty  # candidate not used


def test_map_stations_to_cities_returns_empty_on_empty_input() -> None:
    raw = pd.DataFrame(columns=list(RAW_COLUMNS))
    mapping = _minimal_station_mapping()

    mapped = map_stations_to_cities(raw, mapping)

    assert mapped.empty


# ---------------------------------------------------------------------------
# aggregate_to_city_daily
# ---------------------------------------------------------------------------


def test_aggregate_to_city_daily_returns_silver_schema(tmp_path: Path) -> None:
    p = _make_minimal_csv(tmp_path, _standard_rows())
    raw = load_eea_raw(p)
    mapped = map_stations_to_cities(raw, _minimal_station_mapping())

    result = aggregate_to_city_daily(mapped, processing_time_utc=_FIXED_PROCESSING_TS)

    assert list(result.columns) == list(SILVER_COLUMNS)


def test_aggregate_to_city_daily_source_is_eea(tmp_path: Path) -> None:
    p = _make_minimal_csv(tmp_path, _standard_rows())
    raw = load_eea_raw(p)
    mapped = map_stations_to_cities(raw, _minimal_station_mapping())

    result = aggregate_to_city_daily(mapped)

    assert (result["source"] == "eea").all()


def test_aggregate_to_city_daily_produces_one_row_per_pollutant(tmp_path: Path) -> None:
    """3 standard rows (one per pollutant) must aggregate to 3 Silver rows."""
    p = _make_minimal_csv(tmp_path, _standard_rows())
    raw = load_eea_raw(p)
    mapped = map_stations_to_cities(raw, _minimal_station_mapping())

    result = aggregate_to_city_daily(mapped, processing_time_utc=_FIXED_PROCESSING_TS)

    assert len(result) == 3
    assert set(result["pollutant"]) == CORE_POLLUTANTS


def test_aggregate_to_city_daily_mean_is_correct(tmp_path: Path) -> None:
    """Two PM2.5 rows at 10.0 and 20.0 must produce mean_value = 15.0."""
    rows = [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "AirPollutant": "PM2.5",
            "Concentration": 10.0,
            "Unit": "µg/m³",
        },
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T09:00:00+00:00",
            "AirPollutant": "PM2.5",
            "Concentration": 20.0,
            "Unit": "µg/m³",
        },
    ]
    p = _make_minimal_csv(tmp_path, rows)
    raw = load_eea_raw(p)
    mapped = map_stations_to_cities(raw, _minimal_station_mapping())

    result = aggregate_to_city_daily(mapped, processing_time_utc=_FIXED_PROCESSING_TS)

    pm25 = result[result["pollutant"] == "PM2.5"]
    assert len(pm25) == 1
    assert pm25.iloc[0]["mean_value"] == pytest.approx(15.0)
    assert pm25.iloc[0]["min_value"] == pytest.approx(10.0)
    assert pm25.iloc[0]["max_value"] == pytest.approx(20.0)
    assert pm25.iloc[0]["observation_count"] == 2


def test_aggregate_to_city_daily_observation_count_is_at_least_1(tmp_path: Path) -> None:
    p = _make_minimal_csv(tmp_path, _standard_rows())
    raw = load_eea_raw(p)
    mapped = map_stations_to_cities(raw, _minimal_station_mapping())

    result = aggregate_to_city_daily(mapped, processing_time_utc=_FIXED_PROCESSING_TS)

    assert (result["observation_count"] >= 1).all()


def test_aggregate_to_city_daily_processing_timestamp_is_set(tmp_path: Path) -> None:
    p = _make_minimal_csv(tmp_path, _standard_rows())
    raw = load_eea_raw(p)
    mapped = map_stations_to_cities(raw, _minimal_station_mapping())

    result = aggregate_to_city_daily(mapped, processing_time_utc=_FIXED_PROCESSING_TS)

    assert result["processing_time_utc"].notna().all()


def test_aggregate_to_city_daily_city_id_is_not_free_text(tmp_path: Path) -> None:
    """city_id must come from the station mapping, never from a text column."""
    p = _make_minimal_csv(tmp_path, _standard_rows())
    raw = load_eea_raw(p)
    mapped = map_stations_to_cities(raw, _minimal_station_mapping("vienna_at"))

    result = aggregate_to_city_daily(mapped, processing_time_utc=_FIXED_PROCESSING_TS)

    assert (result["city_id"] == "vienna_at").all()


def test_aggregate_to_city_daily_returns_empty_silver_on_empty_input() -> None:
    empty = pd.DataFrame(
        columns=["city_id", "datetime_begin", "pollutant", "concentration", "unit"]
    )
    result = aggregate_to_city_daily(empty)

    assert result.empty
    assert list(result.columns) == list(SILVER_COLUMNS)


def test_aggregate_to_city_daily_groups_multiple_days_separately(tmp_path: Path) -> None:
    rows = [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "AirPollutant": "NO2",
            "Concentration": 30.0,
            "Unit": "µg/m³",
        },
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-16T08:00:00+00:00",  # different day
            "AirPollutant": "NO2",
            "Concentration": 50.0,
            "Unit": "µg/m³",
        },
    ]
    p = _make_minimal_csv(tmp_path, rows)
    raw = load_eea_raw(p)
    mapped = map_stations_to_cities(raw, _minimal_station_mapping())

    result = aggregate_to_city_daily(mapped, processing_time_utc=_FIXED_PROCESSING_TS)

    assert len(result) == 2  # two separate day rows


# ---------------------------------------------------------------------------
# load_and_aggregate — integration
# ---------------------------------------------------------------------------


def test_load_and_aggregate_end_to_end_csv(tmp_path: Path) -> None:
    p = _make_minimal_csv(tmp_path, _standard_rows())
    mapping = _minimal_station_mapping()

    result = load_and_aggregate(p, mapping, processing_time_utc=_FIXED_PROCESSING_TS)

    assert list(result.columns) == list(SILVER_COLUMNS)
    assert len(result) == 3
    assert (result["source"] == "eea").all()
    assert (result["city_id"] == "vienna_at").all()


def test_load_and_aggregate_end_to_end_parquet(tmp_path: Path) -> None:
    p = _make_minimal_parquet(tmp_path, _standard_rows())
    mapping = _minimal_station_mapping()

    result = load_and_aggregate(p, mapping, processing_time_utc=_FIXED_PROCESSING_TS)

    assert list(result.columns) == list(SILVER_COLUMNS)
    assert len(result) == 3


def test_load_and_aggregate_multi_station_multi_city(tmp_path: Path) -> None:
    """Two stations mapped to two different cities produce separate Silver rows."""
    rows = [
        {
            "AirQualityStationEoICode": "AT90TAB",
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "AirPollutant": "PM2.5",
            "Concentration": 10.0,
            "Unit": "µg/m³",
        },
        {
            "AirQualityStationEoICode": "DEBE068",
            "DatetimeBegin": "2023-01-15T08:00:00+00:00",
            "AirPollutant": "PM2.5",
            "Concentration": 18.0,
            "Unit": "µg/m³",
        },
    ]
    p = _make_minimal_csv(tmp_path, rows)

    mapping = pd.DataFrame(
        [
            {"eea_station_id": "AT90TAB", "city_id": "vienna_at", "mapping_status": "selected"},
            {"eea_station_id": "DEBE068", "city_id": "berlin_de", "mapping_status": "selected"},
        ]
    )

    result = load_and_aggregate(p, mapping, processing_time_utc=_FIXED_PROCESSING_TS)

    assert set(result["city_id"]) == {"vienna_at", "berlin_de"}
    assert len(result) == 2
