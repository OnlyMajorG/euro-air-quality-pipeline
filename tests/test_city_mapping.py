"""Tests for Phase 2 city reference builder and Phase 3 EEA station mapping."""

from pathlib import Path

import pandas as pd
import pytest

from src.city_mapping.build_city_reference import (
    CITY_REFERENCE_COLUMNS,
    CITY_REFERENCE_DTYPES,
    REQUIRED_COLUMNS,
    build_city_reference,
    validate_city_reference,
    write_city_reference,
)
from src.city_mapping.build_station_mapping import (
    REQUIRED_MAPPING_COLUMNS,
    STATION_MAPPING_COLUMNS,
    VALID_MAPPING_STATUSES,
    build_station_mapping,
    validate_station_mapping,
    write_station_mapping,
)


# ---------------------------------------------------------------------------
# Phase 2 — City Reference Tests
# ---------------------------------------------------------------------------


def test_city_reference_has_required_columns() -> None:
    df = build_city_reference()

    assert list(df.columns) == CITY_REFERENCE_COLUMNS


def test_city_reference_has_minimum_phase2_city_count() -> None:
    df = build_city_reference()

    assert len(df) == 8


def test_city_reference_required_join_keys_are_not_null() -> None:
    df = build_city_reference()

    assert not df[REQUIRED_COLUMNS].isna().any().any()


def test_city_reference_has_documented_dtypes() -> None:
    df = build_city_reference()

    assert str(df["population"].dtype) == CITY_REFERENCE_DTYPES["population"]
    assert str(df["area_km2"].dtype) == CITY_REFERENCE_DTYPES["area_km2"]
    assert str(df["latitude"].dtype) == CITY_REFERENCE_DTYPES["latitude"]


def test_city_ids_are_unique_and_stable() -> None:
    df = build_city_reference()

    assert df["city_id"].is_unique
    assert set(df["city_id"]) == {
        "vienna_at",
        "berlin_de",
        "paris_fr",
        "madrid_es",
        "rome_it",
        "amsterdam_nl",
        "warsaw_pl",
        "prague_cz",
    }


def test_coordinates_are_valid() -> None:
    df = build_city_reference()

    assert df["latitude"].between(-90, 90).all()
    assert df["longitude"].between(-180, 180).all()


def test_country_codes_are_iso_alpha2_uppercase() -> None:
    df = build_city_reference()

    assert df["country_code"].str.fullmatch(r"[A-Z]{2}").all()


def test_normalized_names_match_city_ids() -> None:
    df = build_city_reference()

    expected_city_ids = df["city_name_normalized"] + "_" + df["country_code"].str.lower()
    assert (df["city_id"] == expected_city_ids).all()


def test_validate_city_reference_rejects_missing_required_column() -> None:
    df = build_city_reference().drop(columns=["city_id"])

    with pytest.raises(ValueError, match="Missing city reference columns"):
        validate_city_reference(df)


def test_validate_city_reference_rejects_null_required_join_key() -> None:
    df = build_city_reference()
    df.loc[0, "city_id"] = pd.NA

    with pytest.raises(ValueError, match="Required city reference columns"):
        validate_city_reference(df)


def test_validate_city_reference_rejects_duplicate_city_id() -> None:
    df = build_city_reference()
    df.loc[1, "city_id"] = df.loc[0, "city_id"]

    with pytest.raises(ValueError, match="unique"):
        validate_city_reference(df)


def test_validate_city_reference_rejects_invalid_country_code() -> None:
    df = build_city_reference()
    df.loc[0, "country_code"] = "AUT"

    with pytest.raises(ValueError, match="Invalid country_code"):
        validate_city_reference(df)


def test_validate_city_reference_rejects_invalid_normalized_name() -> None:
    df = build_city_reference()
    df.loc[0, "city_name_normalized"] = "Vienna City"

    with pytest.raises(ValueError, match="Invalid city_name_normalized"):
        validate_city_reference(df)


def test_validate_city_reference_rejects_inconsistent_normalized_name() -> None:
    df = build_city_reference()
    df.loc[0, "city_name_normalized"] = "wien"

    with pytest.raises(ValueError, match="Invalid city_id"):
        validate_city_reference(df)


def test_validate_city_reference_rejects_invalid_latitude() -> None:
    df = build_city_reference()
    df.loc[0, "latitude"] = 100.0

    with pytest.raises(ValueError, match="latitude"):
        validate_city_reference(df)


def test_validate_city_reference_rejects_invalid_longitude() -> None:
    df = build_city_reference()
    df.loc[0, "longitude"] = 200.0

    with pytest.raises(ValueError, match="longitude"):
        validate_city_reference(df)


def test_write_city_reference_writes_csv_and_parquet(tmp_path: Path) -> None:
    csv_path, parquet_path = write_city_reference(tmp_path)

    assert csv_path.exists()
    assert parquet_path.exists()

    csv_df = pd.read_csv(csv_path)
    parquet_df = pd.read_parquet(parquet_path)

    assert len(csv_df) == 8
    assert len(parquet_df) == 8
    assert list(parquet_df.columns) == CITY_REFERENCE_COLUMNS


# ---------------------------------------------------------------------------
# Phase 3 — EEA Station-To-City Mapping Tests (Issue 3.3)
# ---------------------------------------------------------------------------


def test_station_mapping_has_required_columns() -> None:
    df = build_station_mapping()

    for col in REQUIRED_MAPPING_COLUMNS:
        assert col in df.columns, f"Required column missing: {col}"


def test_station_mapping_has_all_documented_columns() -> None:
    df = build_station_mapping()

    assert list(df.columns) == STATION_MAPPING_COLUMNS


def test_station_mapping_city_ids_are_subset_of_city_reference() -> None:
    """Every mapped station must reference an existing city_id."""
    mapping_df = build_station_mapping()
    city_ref_df = build_city_reference()

    unknown = set(mapping_df["city_id"]) - set(city_ref_df["city_id"])
    assert not unknown, f"station mapping references unknown city_id values: {unknown}"


def test_station_mapping_all_8_starter_cities_are_represented() -> None:
    """Every starter city must have at least one mapping entry."""
    mapping_df = build_station_mapping()
    city_ref_df = build_city_reference()

    mapped_cities = set(mapping_df["city_id"])
    all_cities = set(city_ref_df["city_id"])
    missing = all_cities - mapped_cities
    assert not missing, f"No station mapping entry for cities: {missing}"


def test_station_mapping_statuses_are_valid() -> None:
    df = build_station_mapping()

    invalid = set(df["mapping_status"]) - VALID_MAPPING_STATUSES
    assert not invalid, f"Invalid mapping_status values: {invalid}"


def test_station_mapping_required_fields_are_not_null() -> None:
    df = build_station_mapping()

    non_nullable = [
        "city_id",
        "eea_station_id",
        "mapping_status",
        "mapping_notes",
        "representativeness_notes",
        "pollutants_available",
    ]
    for col in non_nullable:
        assert not df[col].isna().any(), f"Required mapping column has null values: {col}"


def test_station_mapping_pilot_cities_have_selected_station() -> None:
    """Vienna and Berlin must each have at least one 'selected' station
    because Phase 1 identified confirmed candidate stations for both."""
    df = build_station_mapping()

    for city_id in ("vienna_at", "berlin_de"):
        selected = df[(df["city_id"] == city_id) & (df["mapping_status"] == "selected")]
        assert len(selected) >= 1, f"No selected station found for {city_id}"


def test_station_mapping_distances_are_computed_for_known_stations() -> None:
    """Stations with known coordinates must have a non-null distance."""
    df = build_station_mapping()

    known = df[df["station_latitude"].notna() & df["station_longitude"].notna()]
    assert known["distance_km_to_city_center"].notna().all(), (
        "Some stations with known coordinates are missing distance_km_to_city_center"
    )


def test_station_mapping_distances_are_plausible_for_pilot_cities() -> None:
    """Vienna and Berlin pilot stations should be within 20 km of city centre."""
    df = build_station_mapping()

    for station_id in ("AT90TAB", "DEBE068"):
        row = df[df["eea_station_id"] == station_id]
        assert len(row) == 1, f"Expected exactly one row for station {station_id}"
        dist = row["distance_km_to_city_center"].iloc[0]
        assert dist is not None and dist < 20.0, (
            f"Station {station_id} distance {dist} km is implausible (expected < 20 km)"
        )


def test_validate_station_mapping_rejects_unknown_city_id() -> None:
    mapping_df = build_station_mapping().copy()
    mapping_df.loc[0, "city_id"] = "nonexistent_xx"
    city_ref_df = build_city_reference()

    with pytest.raises(ValueError, match="city_id values not in city_reference"):
        validate_station_mapping(mapping_df, city_ref_df)


def test_validate_station_mapping_rejects_invalid_status() -> None:
    mapping_df = build_station_mapping().copy()
    mapping_df.loc[0, "mapping_status"] = "approved"
    city_ref_df = build_city_reference()

    with pytest.raises(ValueError, match="Invalid mapping_status"):
        validate_station_mapping(mapping_df, city_ref_df)


def test_write_station_mapping_writes_csv_and_parquet(tmp_path: Path) -> None:
    csv_path, parquet_path = write_station_mapping(tmp_path)

    assert csv_path.exists()
    assert parquet_path.exists()

    parquet_df = pd.read_parquet(parquet_path)
    assert len(parquet_df) >= 8
    assert "city_id" in parquet_df.columns
    assert "eea_station_id" in parquet_df.columns
    assert "mapping_status" in parquet_df.columns
