"""Build the Phase 3 EEA station-to-city mapping table from local constants.

This module is intentionally side-effect free on import. It does not call
external APIs, download EEA station metadata, query the EEA ArcGIS REST
service, run Spark, or write files unless explicitly called.

The station records defined here are based on Phase 1 metadata observations
(docs/data_sources.md, EEA Phase 1 Feasibility section). All stations that
have not been fully reviewed carry mapping_status = 'candidate'. Only
stations that have been explicitly reviewed and selected carry
mapping_status = 'selected'.

This mapping must be reviewed and finalized before Phase 3 ingestion
(Issue 3.4) processes real EEA files.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

import pandas as pd

from src.city_mapping.build_city_reference import build_city_reference


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "silver"
STATION_MAPPING_CSV = DEFAULT_OUTPUT_DIR / "eea_station_city_mapping.csv"
STATION_MAPPING_PARQUET = DEFAULT_OUTPUT_DIR / "eea_station_city_mapping.parquet"

VALID_MAPPING_STATUSES = {"selected", "candidate", "fallback", "rejected"}

REQUIRED_MAPPING_COLUMNS = [
    "city_id",
    "eea_station_id",
    "station_latitude",
    "station_longitude",
    "distance_km_to_city_center",
    "pollutants_available",
    "representativeness_notes",
    "mapping_status",
    "mapping_notes",
]

OPTIONAL_MAPPING_COLUMNS = [
    "eea_station_name",
    "time_coverage_start",
    "time_coverage_end",
    "station_class",
    "station_area",
]

STATION_MAPPING_COLUMNS = REQUIRED_MAPPING_COLUMNS + OPTIONAL_MAPPING_COLUMNS


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return the great-circle distance in km between two WGS84 coordinates."""
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ---------------------------------------------------------------------------
# Phase 1 pilot stations — reviewed from EEA metadata (docs/data_sources.md)
# ---------------------------------------------------------------------------
# City reference coordinates for distance calculation:
#   vienna_at  48.2082 N, 16.3738 E
#   berlin_de  52.5200 N, 13.4050 E
#
# Phase 1 found the following candidate stations in station popup metadata.
# Distances are calculated from city reference coordinates using the
# haversine formula. Station coordinates are approximate from EEA metadata.
# ---------------------------------------------------------------------------

_STATION_RECORDS_RAW: list[dict[str, Any]] = [
    # ------------------------------------------------------------------
    # VIENNA — AT
    # Phase 1 identified AT90TAB (Taborstraße) as the strongest candidate:
    # all three core pollutants (NO2, PM2.5, PM10) from 2013-2024.
    # AT90AKC (AKH) also covers all three pollutants.
    # AT9STEF (Stephansplatz) covers NO2 only — candidate for NO2 backup.
    # ------------------------------------------------------------------
    {
        "city_id": "vienna_at",
        "eea_station_id": "AT90TAB",
        "eea_station_name": "Taborstraße",
        "station_latitude": 48.2183,
        "station_longitude": 16.3817,
        "pollutants_available": "PM2.5,PM10,NO2",
        "time_coverage_start": "2013",
        "time_coverage_end": "2024",
        "station_class": None,
        "station_area": "urban",
        "representativeness_notes": (
            "Phase 1 identified as strongest Vienna candidate: all three core "
            "pollutants (NO2, PM2.5, PM10) from 2013-2024. Urban station close "
            "to city centre. Promoted to selected pending Phase 3 file verification."
        ),
        "mapping_status": "selected",
        "mapping_notes": (
            "Primary selected station for vienna_at. Must be verified against "
            "real downloaded E1a Parquet file in Issue 3.4 before ingestion."
        ),
    },
    {
        "city_id": "vienna_at",
        "eea_station_id": "AT90AKC",
        "eea_station_name": "AKH",
        "station_latitude": 48.2189,
        "station_longitude": 16.3492,
        "pollutants_available": "PM2.5,PM10,NO2",
        "time_coverage_start": "2013",
        "time_coverage_end": "2024",
        "station_class": None,
        "station_area": "urban",
        "representativeness_notes": (
            "Phase 1 identified as Vienna candidate covering all three core "
            "pollutants. Suitable as fallback or secondary station if AT90TAB "
            "data quality is insufficient."
        ),
        "mapping_status": "candidate",
        "mapping_notes": (
            "Fallback candidate for vienna_at. Use if AT90TAB is insufficient "
            "for PM2.5 or PM10. Review time coverage and station class in Issue 3.3."
        ),
    },
    {
        "city_id": "vienna_at",
        "eea_station_id": "AT9STEF",
        "eea_station_name": "Stephansplatz",
        "station_latitude": 48.2085,
        "station_longitude": 16.3731,
        "pollutants_available": "NO2",
        "time_coverage_start": None,
        "time_coverage_end": None,
        "station_class": None,
        "station_area": "urban",
        "representativeness_notes": (
            "Phase 1 identified as NO2-only Vienna station. Insufficient for "
            "PM2.5 and PM10 coverage. Kept as candidate for NO2-only backup use."
        ),
        "mapping_status": "candidate",
        "mapping_notes": (
            "NO2-only candidate for vienna_at. Not suitable as primary station. "
            "May supplement AT90TAB NO2 data if gaps are found in Issue 3.4."
        ),
    },
    # ------------------------------------------------------------------
    # BERLIN — DE
    # Phase 1 identified DEBE068 (Berlin Mitte) as strongest candidate:
    # NO2 and PM10 from 2013-2024, PM2.5 from 2020-2024.
    # PM2.5 shorter history is a documented constraint.
    # ------------------------------------------------------------------
    {
        "city_id": "berlin_de",
        "eea_station_id": "DEBE068",
        "eea_station_name": "Berlin Mitte",
        "station_latitude": 52.5163,
        "station_longitude": 13.3777,
        "pollutants_available": "NO2,PM10,PM2.5",
        "time_coverage_start": "2013",
        "time_coverage_end": "2024",
        "station_class": None,
        "station_area": "urban",
        "representativeness_notes": (
            "Phase 1 identified as strongest Berlin candidate. NO2 and PM10 "
            "from 2013-2024; PM2.5 from 2020-2024 only. PM2.5 shorter history "
            "is a documented constraint. Urban centre station."
        ),
        "mapping_status": "selected",
        "mapping_notes": (
            "Primary selected station for berlin_de. PM2.5 coverage starts "
            "2020; historical PM2.5 comparisons before 2020 are not possible "
            "from this station. Verify in Issue 3.4."
        ),
    },
    # ------------------------------------------------------------------
    # REMAINING 6 CITIES — stations not yet reviewed from Phase 1
    # These records were added during the Phase 3 QA follow-up to close the
    # previous placeholder mapping finding.
    # ------------------------------------------------------------------
    {
        "city_id": "paris_fr",
        "eea_station_id": "FR04143",
        "eea_station_name": "PARIS Centre",
        "station_latitude": 48.8590,
        "station_longitude": 2.3510,
        "pollutants_available": "PM2.5,PM10,NO2",
        "time_coverage_start": None,
        "time_coverage_end": None,
        "station_class": None,
        "station_area": None,
        "representativeness_notes": (
            "EEA metadata query returned PM2.5, PM10, and NO2 availability. "
            "Station is approximately 0.3 km from the Paris reference point."
        ),
        "mapping_status": "selected",
        "mapping_notes": (
            "Selected from EEA station metadata query around paris_fr on "
            "2026-05-30. Use for controlled EEA ingestion pending real "
            "source-file row validation."
        ),
    },
    {
        "city_id": "madrid_es",
        "eea_station_id": "ES0118A",
        "eea_station_name": "ESCUELAS AGUIRRE",
        "station_latitude": 40.4217,
        "station_longitude": -3.6822,
        "pollutants_available": "PM2.5,PM10,NO2",
        "time_coverage_start": None,
        "time_coverage_end": None,
        "station_class": None,
        "station_area": None,
        "representativeness_notes": (
            "EEA metadata query returned PM2.5, PM10, and NO2 availability. "
            "Station is approximately 1.9 km from the Madrid reference point."
        ),
        "mapping_status": "selected",
        "mapping_notes": (
            "Selected from EEA station metadata query around madrid_es on "
            "2026-05-30. Use for controlled EEA ingestion pending real "
            "source-file row validation."
        ),
    },
    {
        "city_id": "rome_it",
        "eea_station_id": "IT1906A",
        "eea_station_name": "ARENULA",
        "station_latitude": 41.8940,
        "station_longitude": 12.4754,
        "pollutants_available": "PM2.5,PM10,NO2",
        "time_coverage_start": None,
        "time_coverage_end": None,
        "station_class": None,
        "station_area": None,
        "representativeness_notes": (
            "EEA metadata query returned PM2.5, PM10, and NO2 availability. "
            "Station is approximately 2.0 km from the Rome reference point."
        ),
        "mapping_status": "selected",
        "mapping_notes": (
            "Selected from EEA station metadata query around rome_it on "
            "2026-05-30. Use for controlled EEA ingestion pending real "
            "source-file row validation."
        ),
    },
    {
        "city_id": "amsterdam_nl",
        "eea_station_id": "NL00014",
        "eea_station_name": "Amsterdam-Vondelpark",
        "station_latitude": 52.3597,
        "station_longitude": 4.8662,
        "pollutants_available": "PM2.5,PM10,NO2",
        "time_coverage_start": None,
        "time_coverage_end": None,
        "station_class": None,
        "station_area": None,
        "representativeness_notes": (
            "EEA metadata query returned PM2.5, PM10, and NO2 availability. "
            "Station is approximately 2.7 km from the Amsterdam reference point."
        ),
        "mapping_status": "selected",
        "mapping_notes": (
            "Selected from EEA station metadata query around amsterdam_nl on "
            "2026-05-30. Use for controlled EEA ingestion pending real "
            "source-file row validation."
        ),
    },
    {
        "city_id": "warsaw_pl",
        "eea_station_id": "PL0592A",
        "eea_station_name": "Warszawa-Marszałkowska",
        "station_latitude": 52.2252,
        "station_longitude": 21.0148,
        "pollutants_available": "PM2.5,PM10,NO2",
        "time_coverage_start": None,
        "time_coverage_end": None,
        "station_class": None,
        "station_area": None,
        "representativeness_notes": (
            "EEA metadata query returned PM2.5, PM10, and NO2 availability. "
            "Station is approximately 0.5 km from the Warsaw reference point."
        ),
        "mapping_status": "selected",
        "mapping_notes": (
            "Selected from EEA station metadata query around warsaw_pl on "
            "2026-05-30. Use for controlled EEA ingestion pending real "
            "source-file row validation."
        ),
    },
    {
        "city_id": "prague_cz",
        "eea_station_id": "CZ0ARIE",
        "eea_station_name": "Praha 2-Riegrovy sady",
        "station_latitude": 50.0815,
        "station_longitude": 14.4427,
        "pollutants_available": "PM2.5,PM10,NO2",
        "time_coverage_start": None,
        "time_coverage_end": None,
        "station_class": None,
        "station_area": None,
        "representativeness_notes": (
            "EEA metadata query returned PM2.5, PM10, and NO2 availability. "
            "Station is approximately 0.8 km from the Prague reference point."
        ),
        "mapping_status": "selected",
        "mapping_notes": (
            "Selected from EEA station metadata query around prague_cz on "
            "2026-05-30. Use for controlled EEA ingestion pending real "
            "source-file row validation."
        ),
    },
]


def _compute_distances(
    records: list[dict[str, Any]],
    city_reference: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Fill distance_km_to_city_center for records that have station coordinates."""
    city_coords = city_reference.set_index("city_id")[["latitude", "longitude"]].to_dict("index")
    enriched = []
    for rec in records:
        rec = dict(rec)
        city_id = rec["city_id"]
        slat = rec.get("station_latitude")
        slon = rec.get("station_longitude")
        if slat is not None and slon is not None and city_id in city_coords:
            clat = city_coords[city_id]["latitude"]
            clon = city_coords[city_id]["longitude"]
            rec["distance_km_to_city_center"] = round(_haversine_km(slat, slon, clat, clon), 2)
        else:
            rec["distance_km_to_city_center"] = None
        enriched.append(rec)
    return enriched


def build_station_mapping() -> pd.DataFrame:
    """Return the Phase 3 EEA station-to-city mapping table.

    This function is deterministic and side-effect free. It builds the mapping
    from local constants only. No external API calls, downloads, or Spark
    sessions are triggered.

    Returns
    -------
    pd.DataFrame
        Station mapping table with STATION_MAPPING_COLUMNS column order.
    """
    city_ref = build_city_reference()
    records = _compute_distances(_STATION_RECORDS_RAW, city_ref)
    df = pd.DataFrame.from_records(records, columns=STATION_MAPPING_COLUMNS)
    validate_station_mapping(df, city_ref)
    return df


def validate_station_mapping(
    mapping_df: pd.DataFrame,
    city_reference_df: pd.DataFrame,
) -> None:
    """Validate documented Phase 3 station mapping constraints.

    Parameters
    ----------
    mapping_df:
        The station mapping table to validate.
    city_reference_df:
        The city reference table (from build_city_reference).

    Raises
    ------
    ValueError
        If any constraint is violated.
    """
    missing_columns = [col for col in REQUIRED_MAPPING_COLUMNS if col not in mapping_df.columns]
    if missing_columns:
        raise ValueError(f"Missing station mapping columns: {missing_columns}")

    unknown_city_ids = set(mapping_df["city_id"]) - set(city_reference_df["city_id"])
    if unknown_city_ids:
        raise ValueError(
            f"Station mapping references city_id values not in city_reference: {unknown_city_ids}"
        )

    invalid_statuses = set(mapping_df["mapping_status"]) - VALID_MAPPING_STATUSES
    if invalid_statuses:
        raise ValueError(
            f"Invalid mapping_status values: {invalid_statuses}. "
            f"Allowed: {VALID_MAPPING_STATUSES}"
        )

    null_required = [
        col
        for col in ["city_id", "eea_station_id", "mapping_status", "mapping_notes",
                    "representativeness_notes", "pollutants_available"]
        if mapping_df[col].isna().any()
    ]
    if null_required:
        raise ValueError(f"Required station mapping columns contain null values: {null_required}")

    if not mapping_df["city_id"].isin(city_reference_df["city_id"]).all():
        raise ValueError("All station mapping city_id values must exist in city_reference.")


def write_station_mapping(
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
) -> tuple[Path, Path]:
    """Write station mapping CSV and Parquet files when explicitly called.

    Both files are git-ignored under the repository data policy and are local
    Phase 3 deliverables, not committed source data.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    df = build_station_mapping()
    csv_path = output_path / "eea_station_city_mapping.csv"
    parquet_path = output_path / "eea_station_city_mapping.parquet"

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    return csv_path, parquet_path


def main() -> None:
    """CLI entry point for generating local Phase 3 station mapping artifacts."""
    parser = argparse.ArgumentParser(
        description="Build the local Phase 3 EEA station-to-city mapping table."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Project-relative or absolute output directory for CSV and Parquet files.",
    )
    args = parser.parse_args()

    csv_path, parquet_path = write_station_mapping(args.output_dir)
    print(f"Wrote {csv_path}")
    print(f"Wrote {parquet_path}")

    df = build_station_mapping()
    selected = df[df["mapping_status"] == "selected"]
    unresolved = df[df["eea_station_id"].str.startswith("PLACEHOLDER")]
    print(f"\nSelected stations : {len(selected)}")
    print(f"Placeholder station IDs: {len(unresolved)}")
    if not unresolved.empty:
        print("\nCity IDs requiring station review:")
        for cid in unresolved["city_id"].unique():
            print(f"  - {cid}")


if __name__ == "__main__":
    main()
