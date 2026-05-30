"""Tests for the Phase 2 city reference builder."""

from pathlib import Path

import pandas as pd

from src.city_mapping.build_city_reference import (
    CITY_REFERENCE_COLUMNS,
    CITY_REFERENCE_DTYPES,
    REQUIRED_COLUMNS,
    build_city_reference,
    validate_city_reference,
    write_city_reference,
)


def test_build_city_reference_has_documented_schema() -> None:
    df = build_city_reference()

    assert list(df.columns) == CITY_REFERENCE_COLUMNS
    assert len(df) == 8
    assert not df[REQUIRED_COLUMNS].isna().any().any()
    assert str(df["population"].dtype) == CITY_REFERENCE_DTYPES["population"]
    assert str(df["area_km2"].dtype) == CITY_REFERENCE_DTYPES["area_km2"]
    assert str(df["latitude"].dtype) == CITY_REFERENCE_DTYPES["latitude"]


def test_build_city_reference_has_stable_city_ids_and_coordinates() -> None:
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
    assert df["latitude"].between(-90, 90).all()
    assert df["longitude"].between(-180, 180).all()


def test_validate_city_reference_rejects_duplicate_city_id() -> None:
    df = build_city_reference()
    df.loc[1, "city_id"] = df.loc[0, "city_id"]

    try:
        validate_city_reference(df)
    except ValueError as exc:
        assert "unique" in str(exc)
    else:
        raise AssertionError("Expected duplicate city_id validation error")


def test_write_city_reference_writes_csv_and_parquet(tmp_path: Path) -> None:
    csv_path, parquet_path = write_city_reference(tmp_path)

    assert csv_path.exists()
    assert parquet_path.exists()

    csv_df = pd.read_csv(csv_path)
    parquet_df = pd.read_parquet(parquet_path)

    assert len(csv_df) == 8
    assert len(parquet_df) == 8
    assert list(parquet_df.columns) == CITY_REFERENCE_COLUMNS
