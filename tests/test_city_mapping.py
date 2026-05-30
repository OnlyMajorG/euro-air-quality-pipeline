"""Tests for the Phase 2 city reference builder."""

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
