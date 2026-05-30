"""EEA batch loader for Phase 3 controlled local files.

This module reads EEA historical air quality measurement files from caller-
provided local paths. It normalises source columns into canonical intermediate
fields and filters to the three core pollutants (PM2.5, PM10, NO2).

Design constraints:
- Side-effect free on import.
- No external network calls, no EEA downloads.
- No Kafka, no Spark, no Open-Meteo logic.
- No global file-system access; all paths are explicit caller arguments.
- File writes happen only through explicit writer functions.

The Silver aggregation (city/day/pollutant summary) is handled by a separate
function so callers can inspect and test raw records independently of the
aggregation step.

Schema contracts are defined in docs/data_model.md under
'Phase 3 EEA Batch Ingestion Data Model'.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import pandas as pd


logger = logging.getLogger(__name__)

DEFAULT_EEA_CITY_DAILY_PATH = Path("data/silver/eea_city_daily.parquet")

# ---------------------------------------------------------------------------
# Core pollutant constants — must match docs/data_model.md exactly
# ---------------------------------------------------------------------------

CORE_POLLUTANTS: frozenset[str] = frozenset({"PM2.5", "PM10", "NO2"})

# Maps every accepted EEA source label to the canonical internal name.
# Source: docs/data_model.md, Phase 3 EEA Batch Ingestion Data Model,
# Pollutant Normalisation section.
POLLUTANT_LABEL_MAP: dict[str, str] = {
    # PM2.5
    "PM2.5": "PM2.5",
    "PM2,5": "PM2.5",
    "Particles < 2.5 µm (aerodynamic diameter)": "PM2.5",
    "Particles < 2.5 um (aerodynamic diameter)": "PM2.5",
    # PM10
    "PM10": "PM10",
    "Particles < 10 µm (aerodynamic diameter)": "PM10",
    "Particles < 10 um (aerodynamic diameter)": "PM10",
    # NO2
    "NO2": "NO2",
    "Nitrogen dioxide": "NO2",
    "Nitrogen dioxide (air)": "NO2",
}

# ---------------------------------------------------------------------------
# Source column aliases
# EEA files may expose slightly different column names depending on the
# download format (CSV export vs Parquet). These aliases are checked in order;
# the first match wins. Column names must be verified against real files in
# Issue 3.4 and updated here if different names are found.
# ---------------------------------------------------------------------------

_STATION_ID_ALIASES: tuple[str, ...] = (
    "AirQualityStationEoICode",
    "AirQualityStation",
    "station_id",
)
_TIMESTAMP_ALIASES: tuple[str, ...] = (
    "DatetimeBegin",
    "datetime_begin",
    "Start",
    "date",
)
_POLLUTANT_ALIASES: tuple[str, ...] = (
    "AirPollutant",
    "pollutant",
    "Pollutant",
    "Component",
)
_VALUE_ALIASES: tuple[str, ...] = (
    "Concentration",
    "concentration",
    "Value",
    "value",
)
_UNIT_ALIASES: tuple[str, ...] = (
    "Unit",
    "unit",
)
_VALIDITY_ALIASES: tuple[str, ...] = (
    "Validity",
    "validity",
    "DataValid",
)

# Validity flag values that indicate an invalid or rejected measurement.
# Rows with these values are excluded before aggregation.
# EEA E1a validated files use integer codes; -1 and negative values signal
# invalid or missing data in many EEA export formats.
INVALID_VALIDITY_VALUES: frozenset[int] = frozenset({-1, -99, -999})

# Silver output column names — must match docs/data_model.md Silver schema
SILVER_COLUMNS: tuple[str, ...] = (
    "city_id",
    "date",
    "pollutant",
    "mean_value",
    "min_value",
    "max_value",
    "observation_count",
    "unit",
    "source",
    "processing_time_utc",
)

# Canonical intermediate record columns (before city join and aggregation)
RAW_COLUMNS: tuple[str, ...] = (
    "eea_station_id",
    "datetime_begin",
    "pollutant",
    "concentration",
    "unit",
)

REQUIRED_EEA_ROW_COLUMNS: tuple[str, ...] = (
    "city_id",
    "datetime_begin",
    "pollutant",
    "concentration",
    "unit",
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _find_column(df: pd.DataFrame, aliases: tuple[str, ...], label: str) -> str:
    """Return the first alias that exists as a column in *df*.

    Raises
    ------
    KeyError
        If none of the aliases is found, with a message listing what was
        expected and what columns the file actually has.
    """
    for alias in aliases:
        if alias in df.columns:
            return alias
    raise KeyError(
        f"Could not find expected {label} column. "
        f"Tried: {list(aliases)}. "
        f"File columns: {list(df.columns)}"
    )


def _normalise_pollutant(label: str) -> str | None:
    """Map a raw EEA pollutant label to the canonical internal name.

    Returns None for labels that are not in scope (silently excluded).
    """
    return POLLUTANT_LABEL_MAP.get(label.strip() if isinstance(label, str) else label)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_eea_raw(path: Path | str) -> pd.DataFrame:
    """Read a local EEA measurement file and return normalised raw records.

    Reads CSV or Parquet based on file extension. Normalises source column
    names to canonical intermediate field names. Filters to core pollutants
    (PM2.5, PM10, NO2). Excludes rows with known-bad validity flags or
    non-positive concentration values.

    Parameters
    ----------
    path:
        Absolute or relative path to a local EEA CSV or Parquet file.
        The file must exist and must not be an empty file.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: ``eea_station_id``, ``datetime_begin``,
        ``pollutant`` (canonical), ``concentration``, ``unit``.
        Rows that do not map to a core pollutant or that fail quality checks
        are excluded silently.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    ValueError
        If the file format is not recognised (not .csv or .parquet).
    KeyError
        If a required column cannot be found by any known alias.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"EEA file not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        raw = pd.read_csv(path, low_memory=False)
    elif suffix == ".parquet":
        raw = pd.read_parquet(path)
    else:
        raise ValueError(
            f"Unsupported file format: {suffix!r}. "
            "EEA loader accepts .csv and .parquet only."
        )

    logger.debug("Loaded %d raw rows from %s", len(raw), path)

    # Resolve column aliases
    station_col = _find_column(raw, _STATION_ID_ALIASES, "station identity")
    ts_col = _find_column(raw, _TIMESTAMP_ALIASES, "measurement timestamp")
    pollutant_col = _find_column(raw, _POLLUTANT_ALIASES, "pollutant label")
    value_col = _find_column(raw, _VALUE_ALIASES, "measured value")
    unit_col = _find_column(raw, _UNIT_ALIASES, "unit")

    # Resolve optional validity column
    validity_col: str | None = None
    for alias in _VALIDITY_ALIASES:
        if alias in raw.columns:
            validity_col = alias
            break

    # Build working DataFrame with only the columns we need
    working = pd.DataFrame(
        {
            "eea_station_id": raw[station_col].astype(str).str.strip(),
            "datetime_begin": pd.to_datetime(raw[ts_col], utc=True, errors="coerce"),
            "pollutant_raw": raw[pollutant_col].astype(str).str.strip(),
            "concentration": pd.to_numeric(raw[value_col], errors="coerce"),
            "unit": raw[unit_col].astype(str).str.strip(),
        }
    )

    if validity_col is not None:
        working["_validity"] = pd.to_numeric(raw[validity_col], errors="coerce")

    n_before = len(working)

    # Exclude rows with unparseable timestamps
    working = working[working["datetime_begin"].notna()].copy()
    n_after_ts = len(working)
    if n_before != n_after_ts:
        logger.warning(
            "Dropped %d rows with unparseable timestamps from %s",
            n_before - n_after_ts,
            path,
        )

    # Exclude rows with known-bad validity flags
    if "_validity" in working.columns:
        valid_mask = (
            working["_validity"].isna()
            | ~working["_validity"].isin(INVALID_VALIDITY_VALUES)
        )
        n_before_valid = len(working)
        working = working[valid_mask].copy()
        dropped_validity = n_before_valid - len(working)
        if dropped_validity:
            logger.debug(
                "Dropped %d rows with invalid validity flags from %s",
                dropped_validity,
                path,
            )
        working = working.drop(columns=["_validity"])

    # Exclude non-positive concentration values (instrument errors / missing)
    n_before_conc = len(working)
    working = working[working["concentration"].notna() & (working["concentration"] >= 0)].copy()
    if n_before_conc != len(working):
        logger.debug(
            "Dropped %d rows with negative or missing concentration from %s",
            n_before_conc - len(working),
            path,
        )

    # Normalise pollutant labels to canonical names
    working["pollutant"] = working["pollutant_raw"].map(_normalise_pollutant)
    working = working.drop(columns=["pollutant_raw"])

    # Filter to core pollutants only (silently exclude others)
    n_before_poll = len(working)
    working = working[working["pollutant"].isin(CORE_POLLUTANTS)].copy()
    excluded_pollutants = n_before_poll - len(working)
    if excluded_pollutants:
        logger.debug(
            "Excluded %d rows with non-core pollutants from %s",
            excluded_pollutants,
            path,
        )

    logger.debug(
        "Returning %d normalised rows from %s (started with %d raw rows)",
        len(working),
        path,
        n_before,
    )

    return working[list(RAW_COLUMNS)].reset_index(drop=True)


def map_stations_to_cities(
    raw_df: pd.DataFrame,
    station_mapping_df: pd.DataFrame,
) -> pd.DataFrame:
    """Join normalised raw records to city_id via the station mapping table.

    Only rows whose ``eea_station_id`` has at least one ``selected`` station
    mapping entry are used. Records for unresolved (placeholder) or rejected
    stations are excluded with a log warning.

    Parameters
    ----------
    raw_df:
        Output of :func:`load_eea_raw` with column ``eea_station_id``.
    station_mapping_df:
        Station mapping table from ``build_station_mapping()`` with at minimum
        columns ``eea_station_id``, ``city_id``, and ``mapping_status``.

    Returns
    -------
    pd.DataFrame
        ``raw_df`` with ``city_id`` column attached. Rows without a
        ``selected`` mapping are dropped.
    """
    # Only use selected stations to prevent unreviewed data entering Silver
    selected = station_mapping_df[
        station_mapping_df["mapping_status"] == "selected"
    ][["eea_station_id", "city_id"]].drop_duplicates()

    merged = raw_df.merge(selected, on="eea_station_id", how="left")

    unmatched_count = merged["city_id"].isna().sum()
    if unmatched_count:
        unmatched_ids = (
            raw_df.loc[merged["city_id"].isna(), "eea_station_id"].unique().tolist()
        )
        logger.warning(
            "Dropping %d rows with no selected station mapping. "
            "Unmatched station IDs: %s",
            unmatched_count,
            unmatched_ids,
        )

    return merged[merged["city_id"].notna()].reset_index(drop=True)


def validate_eea_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Validate normalised EEA rows before daily aggregation.

    The validator is intentionally strict about schema and required join fields:
    missing required columns or null required values raise ``ValueError``.
    Invalid measurement rows are rejected from the returned DataFrame so they
    cannot silently enter downstream aggregation.

    Required input columns are ``city_id``, ``datetime_begin``, ``pollutant``,
    ``concentration``, and ``unit``.
    """
    missing_columns = [col for col in REQUIRED_EEA_ROW_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required EEA row columns: {missing_columns}")

    null_required = [
        col
        for col in REQUIRED_EEA_ROW_COLUMNS
        if df[col].isna().any() or (df[col].astype(str).str.strip() == "").any()
    ]
    if null_required:
        raise ValueError(f"Required EEA row fields contain null or empty values: {null_required}")

    validated = df.copy()
    validated["datetime_begin"] = pd.to_datetime(
        validated["datetime_begin"],
        utc=True,
        errors="coerce",
    )
    invalid_dates = validated["datetime_begin"].isna()
    if invalid_dates.any():
        raise ValueError("EEA rows contain invalid or unparseable datetime_begin values")

    validated["concentration"] = pd.to_numeric(validated["concentration"], errors="coerce")
    invalid_measurements = validated["concentration"].isna() | (validated["concentration"] < 0)
    if invalid_measurements.any():
        logger.warning(
            "Rejected %d EEA rows with negative or invalid concentration values",
            int(invalid_measurements.sum()),
        )
        validated = validated[~invalid_measurements].copy()

    unsupported_pollutants = sorted(set(validated["pollutant"]) - CORE_POLLUTANTS)
    if unsupported_pollutants:
        logger.warning(
            "Rejected EEA rows with unsupported pollutant values: %s",
            unsupported_pollutants,
        )
        validated = validated[validated["pollutant"].isin(CORE_POLLUTANTS)].copy()

    return validated.reset_index(drop=True)


def aggregate_to_city_daily(
    mapped_df: pd.DataFrame,
    processing_time_utc: datetime | None = None,
) -> pd.DataFrame:
    """Aggregate station-level records to city/day/pollutant granularity.

    Computes mean, min, max, and observation_count per (city_id, date,
    pollutant, unit) group. Adds ``source = 'eea'`` and
    ``processing_time_utc`` for traceability.

    Parameters
    ----------
    mapped_df:
        Output of :func:`map_stations_to_cities`. Must have columns:
        ``city_id``, ``datetime_begin``, ``pollutant``,
        ``concentration``, ``unit``.
    processing_time_utc:
        UTC timestamp to stamp processed rows. Defaults to
        ``datetime.now(timezone.utc)`` if not provided.

    Returns
    -------
    pd.DataFrame
        Silver schema DataFrame with columns matching ``SILVER_COLUMNS``.
        Empty if ``mapped_df`` is empty.
    """
    if mapped_df.empty:
        return pd.DataFrame(columns=list(SILVER_COLUMNS))

    mapped_df = validate_eea_rows(mapped_df)
    if mapped_df.empty:
        return pd.DataFrame(columns=list(SILVER_COLUMNS))

    if processing_time_utc is None:
        processing_time_utc = datetime.now(timezone.utc)

    df = mapped_df.copy()
    df["date"] = df["datetime_begin"].dt.date

    grouped = (
        df.groupby(["city_id", "date", "pollutant", "unit"], as_index=False)
        .agg(
            mean_value=("concentration", "mean"),
            min_value=("concentration", "min"),
            max_value=("concentration", "max"),
            observation_count=("concentration", "count"),
        )
    )

    # Enforce schema constraints from docs/data_model.md
    grouped = grouped[grouped["observation_count"] >= 1].copy()
    grouped["date"] = pd.to_datetime(grouped["date"])
    grouped["source"] = "eea"
    grouped["processing_time_utc"] = pd.Timestamp(processing_time_utc)

    # Single-observation rows: min and max equal mean — keep as-is (not null)
    # because they are technically correct; marking as null is only relevant
    # when a deliberate nullable policy is chosen in a later review.

    return grouped[list(SILVER_COLUMNS)].reset_index(drop=True)


def load_and_aggregate(
    path: Path | str,
    station_mapping_df: pd.DataFrame,
    processing_time_utc: datetime | None = None,
) -> pd.DataFrame:
    """Convenience function: load, normalise, map, and aggregate in one call.

    Combines :func:`load_eea_raw`, :func:`map_stations_to_cities`, and
    :func:`aggregate_to_city_daily` into a single pipeline call for callers
    that do not need to inspect intermediate DataFrames.

    Parameters
    ----------
    path:
        Path to a local EEA CSV or Parquet file.
    station_mapping_df:
        Station mapping table from ``build_station_mapping()``.
    processing_time_utc:
        Optional fixed timestamp for the ``processing_time_utc`` column.

    Returns
    -------
    pd.DataFrame
        Silver schema DataFrame.
    """
    raw = load_eea_raw(path)
    mapped = map_stations_to_cities(raw, station_mapping_df)
    return aggregate_to_city_daily(mapped, processing_time_utc=processing_time_utc)


def write_eea_city_daily_parquet(
    silver_df: pd.DataFrame,
    output_path: Path | str = DEFAULT_EEA_CITY_DAILY_PATH,
) -> Path:
    """Write EEA city/day/pollutant Silver rows to Parquet explicitly.

    This function is the Phase 3.6 output boundary. It validates the Silver
    schema and pollutant/source constraints before writing. Importing this
    module never writes files; callers must invoke this function deliberately.
    """
    missing_columns = [col for col in SILVER_COLUMNS if col not in silver_df.columns]
    if missing_columns:
        raise ValueError(f"Missing EEA Silver output columns: {missing_columns}")

    output = silver_df[list(SILVER_COLUMNS)].copy()

    if not output.empty:
        unsupported_pollutants = sorted(set(output["pollutant"]) - CORE_POLLUTANTS)
        if unsupported_pollutants:
            raise ValueError(
                "EEA Silver output contains unsupported pollutants: "
                f"{unsupported_pollutants}"
            )

        invalid_sources = sorted(set(output["source"]) - {"eea"})
        if invalid_sources:
            raise ValueError(
                "EEA Silver output source must be 'eea' only; found: "
                f"{invalid_sources}"
            )

        required = [
            "city_id",
            "date",
            "pollutant",
            "mean_value",
            "observation_count",
            "unit",
            "source",
        ]
        null_required = [
            col
            for col in required
            if output[col].isna().any() or (output[col].astype(str).str.strip() == "").any()
        ]
        if null_required:
            raise ValueError(
                "EEA Silver output required fields contain null or empty values: "
                f"{null_required}"
            )

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    output.to_parquet(path, index=False)
    return path


def build_eea_city_daily_parquet(
    input_path: Path | str,
    station_mapping_df: pd.DataFrame,
    output_path: Path | str = DEFAULT_EEA_CITY_DAILY_PATH,
    processing_time_utc: datetime | None = None,
) -> pd.DataFrame:
    """Load local EEA rows, aggregate them, and explicitly write Silver Parquet.

    This convenience function is intended for controlled local Phase 3 runs
    using a caller-provided EEA CSV/Parquet sample and station mapping table.
    It performs no network calls and does not mix Open-Meteo data.
    """
    silver = load_and_aggregate(
        input_path,
        station_mapping_df,
        processing_time_utc=processing_time_utc,
    )
    write_eea_city_daily_parquet(silver, output_path)
    return silver
