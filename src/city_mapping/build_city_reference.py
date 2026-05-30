"""Build the Phase 2 city reference table from local constants.

This module is intentionally side-effect free on import. It does not call
external APIs, scrape websites, download EEA data, or depend on Kafka/Spark.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "silver"
CITY_REFERENCE_CSV = DEFAULT_OUTPUT_DIR / "city_reference.csv"
CITY_REFERENCE_PARQUET = DEFAULT_OUTPUT_DIR / "city_reference.parquet"

REQUIRED_COLUMNS = [
    "city_id",
    "city_name",
    "city_name_normalized",
    "country_code",
    "latitude",
    "longitude",
    "mapping_notes",
    "eea_station_selection_notes",
]

OPTIONAL_COLUMNS = [
    "population",
    "area_km2",
    "population_density",
    "wikipedia_page_title",
    "wikipedia_url",
    "wikipedia_metadata_notes",
    "open_meteo_coordinate_notes",
]

CITY_REFERENCE_COLUMNS = REQUIRED_COLUMNS + OPTIONAL_COLUMNS

CITY_REFERENCE_DTYPES = {
    "city_id": "string",
    "city_name": "string",
    "city_name_normalized": "string",
    "country_code": "string",
    "latitude": "float64",
    "longitude": "float64",
    "mapping_notes": "string",
    "eea_station_selection_notes": "string",
    "population": "Int64",
    "area_km2": "Float64",
    "population_density": "Float64",
    "wikipedia_page_title": "string",
    "wikipedia_url": "string",
    "wikipedia_metadata_notes": "string",
    "open_meteo_coordinate_notes": "string",
}

CITY_RECORDS: list[dict[str, Any]] = [
    {
        "city_id": "vienna_at",
        "city_name": "Vienna",
        "city_name_normalized": "vienna",
        "country_code": "AT",
        "latitude": 48.2082,
        "longitude": 16.3738,
        "population": None,
        "area_km2": None,
        "population_density": None,
        "mapping_notes": "Phase 1 pilot city with feasible Open-Meteo, EEA, and Wikipedia evidence.",
        "eea_station_selection_notes": "Select representative Vienna-area EEA stations in later Phase 2 mapping work.",
        "wikipedia_page_title": "Vienna",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Vienna",
        "wikipedia_metadata_notes": "Use page metadata only after parser rules are documented.",
        "open_meteo_coordinate_notes": "Use fixed city-center WGS84 coordinate for API feasibility and later alignment.",
    },
    {
        "city_id": "berlin_de",
        "city_name": "Berlin",
        "city_name_normalized": "berlin",
        "country_code": "DE",
        "latitude": 52.52,
        "longitude": 13.405,
        "population": None,
        "area_km2": None,
        "population_density": None,
        "mapping_notes": "Phase 1 pilot city with feasible Open-Meteo, EEA, and Wikipedia evidence.",
        "eea_station_selection_notes": "Select representative Berlin-area EEA stations in later Phase 2 mapping work.",
        "wikipedia_page_title": "Berlin",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Berlin",
        "wikipedia_metadata_notes": "Use page metadata only after parser rules are documented.",
        "open_meteo_coordinate_notes": "Use fixed city-center WGS84 coordinate for API feasibility and later alignment.",
    },
    {
        "city_id": "paris_fr",
        "city_name": "Paris",
        "city_name_normalized": "paris",
        "country_code": "FR",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "population": None,
        "area_km2": None,
        "population_density": None,
        "mapping_notes": "Controlled starter city chosen for major European capital coverage.",
        "eea_station_selection_notes": "Select representative Paris-area EEA stations in later Phase 2 mapping work.",
        "wikipedia_page_title": "Paris",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Paris",
        "wikipedia_metadata_notes": "Use page metadata only after parser rules are documented.",
        "open_meteo_coordinate_notes": "Use fixed city-center WGS84 coordinate for API feasibility and later alignment.",
    },
    {
        "city_id": "madrid_es",
        "city_name": "Madrid",
        "city_name_normalized": "madrid",
        "country_code": "ES",
        "latitude": 40.4168,
        "longitude": -3.7038,
        "population": None,
        "area_km2": None,
        "population_density": None,
        "mapping_notes": "Controlled starter city chosen for southern European comparison.",
        "eea_station_selection_notes": "Select representative Madrid-area EEA stations in later Phase 2 mapping work.",
        "wikipedia_page_title": "Madrid",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Madrid",
        "wikipedia_metadata_notes": "Use page metadata only after parser rules are documented.",
        "open_meteo_coordinate_notes": "Use fixed city-center WGS84 coordinate for API feasibility and later alignment.",
    },
    {
        "city_id": "rome_it",
        "city_name": "Rome",
        "city_name_normalized": "rome",
        "country_code": "IT",
        "latitude": 41.9028,
        "longitude": 12.4964,
        "population": None,
        "area_km2": None,
        "population_density": None,
        "mapping_notes": "Controlled starter city chosen for Mediterranean comparison.",
        "eea_station_selection_notes": "Select representative Rome-area EEA stations in later Phase 2 mapping work.",
        "wikipedia_page_title": "Rome",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Rome",
        "wikipedia_metadata_notes": "Use page metadata only after parser rules are documented.",
        "open_meteo_coordinate_notes": "Use fixed city-center WGS84 coordinate for API feasibility and later alignment.",
    },
    {
        "city_id": "amsterdam_nl",
        "city_name": "Amsterdam",
        "city_name_normalized": "amsterdam",
        "country_code": "NL",
        "latitude": 52.3676,
        "longitude": 4.9041,
        "population": None,
        "area_km2": None,
        "population_density": None,
        "mapping_notes": "Controlled starter city chosen for expected monitoring coverage and compact urban context.",
        "eea_station_selection_notes": "Select representative Amsterdam-area EEA stations in later Phase 2 mapping work.",
        "wikipedia_page_title": "Amsterdam",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Amsterdam",
        "wikipedia_metadata_notes": "Use page metadata only after parser rules are documented.",
        "open_meteo_coordinate_notes": "Use fixed city-center WGS84 coordinate for API feasibility and later alignment.",
    },
    {
        "city_id": "warsaw_pl",
        "city_name": "Warsaw",
        "city_name_normalized": "warsaw",
        "country_code": "PL",
        "latitude": 52.2297,
        "longitude": 21.0122,
        "population": None,
        "area_km2": None,
        "population_density": None,
        "mapping_notes": "Controlled starter city chosen for Central and Eastern European coverage.",
        "eea_station_selection_notes": "Select representative Warsaw-area EEA stations in later Phase 2 mapping work.",
        "wikipedia_page_title": "Warsaw",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Warsaw",
        "wikipedia_metadata_notes": "Use page metadata only after parser rules are documented.",
        "open_meteo_coordinate_notes": "Use fixed city-center WGS84 coordinate for API feasibility and later alignment.",
    },
    {
        "city_id": "prague_cz",
        "city_name": "Prague",
        "city_name_normalized": "prague",
        "country_code": "CZ",
        "latitude": 50.0755,
        "longitude": 14.4378,
        "population": None,
        "area_km2": None,
        "population_density": None,
        "mapping_notes": "Controlled starter city chosen for Central European coverage and manageable scope.",
        "eea_station_selection_notes": "Select representative Prague-area EEA stations in later Phase 2 mapping work.",
        "wikipedia_page_title": "Prague",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Prague",
        "wikipedia_metadata_notes": "Use page metadata only after parser rules are documented.",
        "open_meteo_coordinate_notes": "Use fixed city-center WGS84 coordinate for API feasibility and later alignment.",
    },
]


def build_city_reference() -> pd.DataFrame:
    """Return the deterministic Phase 2 city reference table."""
    df = pd.DataFrame.from_records(CITY_RECORDS, columns=CITY_REFERENCE_COLUMNS)
    df = df.astype(CITY_REFERENCE_DTYPES)
    validate_city_reference(df)
    return df


def validate_city_reference(df: pd.DataFrame) -> None:
    """Validate the documented Phase 2 city reference constraints."""
    missing_columns = [column for column in CITY_REFERENCE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing city reference columns: {missing_columns}")

    empty_required = [
        column
        for column in REQUIRED_COLUMNS
        if df[column].isna().any() or (df[column].astype(str).str.strip() == "").any()
    ]
    if empty_required:
        raise ValueError(f"Required city reference columns contain empty values: {empty_required}")

    if not df["city_id"].is_unique:
        raise ValueError("city_id values must be unique")

    invalid_country_codes = df.loc[~df["country_code"].str.fullmatch(r"[A-Z]{2}"), "country_code"].tolist()
    if invalid_country_codes:
        raise ValueError(f"Invalid country_code values: {invalid_country_codes}")

    invalid_normalized_names = df.loc[
        ~df["city_name_normalized"].str.fullmatch(r"[a-z0-9_]+"),
        "city_name_normalized",
    ].tolist()
    if invalid_normalized_names:
        raise ValueError(f"Invalid city_name_normalized values: {invalid_normalized_names}")

    expected_city_ids = df["city_name_normalized"] + "_" + df["country_code"].str.lower()
    invalid_city_ids = df.loc[df["city_id"] != expected_city_ids, "city_id"].tolist()
    if invalid_city_ids:
        raise ValueError(f"Invalid city_id values: {invalid_city_ids}")

    if not df["latitude"].between(-90, 90).all():
        raise ValueError("latitude values must be between -90 and 90")

    if not df["longitude"].between(-180, 180).all():
        raise ValueError("longitude values must be between -180 and 180")


def write_city_reference(output_dir: Path | str = DEFAULT_OUTPUT_DIR) -> tuple[Path, Path]:
    """Write city reference CSV and Parquet files when explicitly called."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    df = build_city_reference()
    csv_path = output_path / "city_reference.csv"
    parquet_path = output_path / "city_reference.parquet"

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    return csv_path, parquet_path


def main() -> None:
    """CLI entry point for generating local Phase 2 city reference artifacts."""
    parser = argparse.ArgumentParser(description="Build the local Phase 2 city reference table.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Project-relative or absolute output directory for CSV and Parquet files.",
    )
    args = parser.parse_args()

    csv_path, parquet_path = write_city_reference(args.output_dir)
    print(f"Wrote {csv_path}")
    print(f"Wrote {parquet_path}")


if __name__ == "__main__":
    main()
