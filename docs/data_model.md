# Data Model

## Phase 2 City Reference Scope

Phase 2 defines the controlled starter city list for the city reference model.
This is city-reference work only. It does not implement EEA ingestion,
Wikipedia scraping, Open-Meteo API calls, Kafka, Spark, Gold tables, or final
analytics.

The list starts with exactly 8 European cities. Vienna and Berlin are included
because they were the Phase 1 pilot cities and all three planned source
categories were feasible for them.

| city_id_candidate | city_name | country_code | latitude | longitude | selection_rationale |
| --- | --- | --- | ---: | ---: | --- |
| vienna_at | Vienna | AT | 48.2082 | 16.3738 | Phase 1 pilot city; Open-Meteo, EEA metadata, and Wikipedia feasibility confirmed. |
| berlin_de | Berlin | DE | 52.5200 | 13.4050 | Phase 1 pilot city; Open-Meteo, EEA metadata, and Wikipedia feasibility confirmed. |
| paris_fr | Paris | FR | 48.8566 | 2.3522 | Major European capital with expected air-quality monitoring and rich city metadata. |
| madrid_es | Madrid | ES | 40.4168 | -3.7038 | Major European capital; useful southern European comparison city. |
| rome_it | Rome | IT | 41.9028 | 12.4964 | Major European capital; useful Mediterranean comparison city. |
| amsterdam_nl | Amsterdam | NL | 52.3676 | 4.9041 | Major European city with expected monitoring coverage and compact urban context. |
| warsaw_pl | Warsaw | PL | 52.2297 | 21.0122 | Major Central/Eastern European capital for regional diversity. |
| prague_cz | Prague | CZ | 50.0755 | 14.4378 | Central European capital with expected source coverage and manageable scope. |

## Canonical City Reference Schema

The city reference table is the controlled join surface for later phases. It
does not prove that downstream EEA, Wikipedia, Open-Meteo, Kafka, Spark, or
analytics outputs already exist. It only defines the stable city-level fields
that later source-specific work must map to.

### Identifier Convention

`city_id` is the stable technical identifier for joins. It uses lowercase
ASCII text in the pattern `<normalized_city_name>_<country_code_lower>`.
Spaces and punctuation are replaced or removed during normalization. The
country code suffix uses ISO 3166-1 alpha-2 in lowercase form.

Examples:

- `vienna_at`
- `berlin_de`
- `amsterdam_nl`

Once a `city_id` is used by downstream data, it should not be renamed without a
documented migration note. Downstream jobs should join on `city_id`, not on free
text city names.

### Schema

| field | type | required | nullability | rule |
| --- | --- | --- | --- | --- |
| city_id | string | yes | non-null | Unique stable key using lowercase `<normalized_city_name>_<country_code_lower>`. |
| city_name | string | yes | non-null | Human-readable display name, for example `Vienna`. |
| city_name_normalized | string | yes | non-null | Lowercase normalized city name used to derive `city_id`. |
| country_code | string | yes | non-null | ISO 3166-1 alpha-2 country code in uppercase, for example `AT`. |
| latitude | float | yes | non-null | WGS84 city coordinate used for Open-Meteo feasibility and later source alignment; must be between -90 and 90. |
| longitude | float | yes | non-null | WGS84 city coordinate used for Open-Meteo feasibility and later source alignment; must be between -180 and 180. |
| population | integer | no | nullable | Future contextual metadata, expected from Wikipedia or another documented reference source. |
| area_km2 | float | no | nullable | Future contextual metadata, expected from Wikipedia or another documented reference source. |
| population_density | float | no | nullable | Future contextual or derived metadata; may stay null if population or area is unavailable. |
| mapping_notes | string | yes | non-null | Short explanation of why the city belongs in the controlled starter scope and how source alignment should be interpreted. |
| eea_station_selection_notes | string | yes | non-null | Notes for future EEA station-to-city matching; this is not an implemented station mapping. |
| wikipedia_page_title | string | no | nullable | Planned Wikipedia page title used for metadata linkage. |
| wikipedia_url | string | no | nullable | Planned Wikipedia page URL used for traceability. |
| wikipedia_metadata_notes | string | no | nullable | Notes about expected Wikipedia metadata fields, ambiguity, or fallback handling. |
| open_meteo_coordinate_notes | string | no | nullable | Notes about coordinate assumptions for future Open-Meteo API checks. |

### Constraints And Validation Rules

- `city_id` must be unique across the city reference table.
- Required fields must not be null or empty.
- `country_code` must be exactly two uppercase letters.
- `latitude` and `longitude` must be numeric and within WGS84 ranges.
- Optional metadata fields may be null during Phase 2 and must not block city
  reference creation.
- EEA station mapping remains a documented mapping decision until later
  ingestion phases; Phase 2 must not download or process full EEA datasets.
- Wikipedia fields are linkage metadata only in Phase 2; production scraping
  and parser implementation remain out of scope.
- The schema is intentionally small enough to support focused tests in
  `tests/test_city_mapping.py`.

### Phase 2.3 Local Builder

`src/city_mapping/build_city_reference.py` implements the first deterministic
city reference builder from local constants. The module is side-effect free on
import. It writes the following local Silver artifacts only when explicitly
called:

- `data/silver/city_reference.csv`
- `data/silver/city_reference.parquet`

Both generated files are ignored by `.gitignore` under the repository data
policy. They are local Phase 2 deliverables, not committed source data.

## EEA Station Mapping Strategy

EEA measurements are station-based, while the project analysis is city-based.
Phase 2 therefore documents how future EEA station records should be associated
with the canonical `city_id`. This is a mapping strategy only; it does not
download EEA data, implement station-radius matching, run Spark, or aggregate
measurements.

For each city, candidate EEA stations must be reviewed by:

1. distance to the city reference coordinate,
2. pollutant coverage for PM2.5, PM10, and NO2,
3. time coverage overlap with the planned analysis period,
4. station class, station area, or representativeness where available,
5. country and city context consistency.

Downstream EEA processing must join through `city_id`. Free-text city names,
station names, or manually typed labels must not be used as downstream city
join keys.

### Required Station Mapping Fields

| field | type | required | purpose |
| --- | --- | --- | --- |
| city_id | string | yes | Canonical city join key from the city reference table. |
| eea_station_id | string | yes | Stable EEA station identifier from future EEA metadata. |
| eea_station_name | string | no | Human-readable station name for review only. |
| station_latitude | float | yes | Station WGS84 latitude used for distance review. |
| station_longitude | float | yes | Station WGS84 longitude used for distance review. |
| distance_km_to_city_center | float | yes | Distance from station to city reference coordinate. |
| pollutants_available | string/list | yes | Target pollutant coverage observed for PM2.5, PM10, and NO2. |
| time_coverage_start | date/string | no | Earliest observed or documented measurement date. |
| time_coverage_end | date/string | no | Latest observed or documented measurement date. |
| station_class | string | no | Station class where EEA metadata provides it. |
| station_area | string | no | Urban/suburban/rural or equivalent area context where available. |
| representativeness_notes | string | yes | Reviewer note explaining whether the station is appropriate for the city. |
| mapping_status | string | yes | One of `selected`, `candidate`, `fallback`, or `rejected`. |
| mapping_notes | string | yes | Transparent rationale for the station-to-city decision. |

### Fallback Rules

- If no nearby station covers all target pollutants, select the best documented
  candidate per pollutant and mark the mapping as constrained.
- If pollutant coverage is partial, preserve the city in the reference model
  but document unavailable pollutants before Phase 3 ingestion.
- If time coverage is too short for the planned analysis period, keep the
  station as `candidate` or `fallback` until reviewed.
- If station representativeness is unclear, do not promote the station to
  `selected` without a manual note.
- The station mapping must be reviewed before Phase 3 ingestion starts.

```mermaid
flowchart LR
    city["city_reference.city_id"]
    candidates["EEA station metadata candidates"]
    review["Review distance, pollutant coverage, time coverage, representativeness"]
    mapping["station_city_mapping"]
    ingestion["Phase 3 EEA ingestion"]

    city --> review
    candidates --> review
    review --> mapping
    mapping --> ingestion
```

## Phase 3.3 EEA Station-To-City Mapping Table

Phase 3 Issue 3.3 implements the station-to-city mapping structure as a
controlled local table built from Python constants. The builder is in
\src/city_mapping/build_station_mapping.py\. No external API calls, no EEA
bulk downloads, and no Spark sessions are triggered by building or validating
the mapping.

### Implemented Mapping Builder

\src/city_mapping/build_station_mapping.py\ provides:

- \uild_station_mapping()\ — deterministic, side-effect-free builder that
  returns a DataFrame with all columns in \STATION_MAPPING_COLUMNS\ order.
- \alidate_station_mapping(mapping_df, city_reference_df)\ — validates that
  all \city_id\ values exist in \city_reference.parquet\, all \mapping_status  values are from the allowed set, and required fields are non-null.
- \write_station_mapping(output_dir)\ — writes local CSV and Parquet files
  when explicitly called; both are git-ignored under repository data policy.
- \_haversine_km(lat1, lon1, lat2, lon2)\ — computes great-circle distance
  used to fill \distance_km_to_city_center\ for stations with known coordinates.

**Output paths (local, git-ignored):**

- \data/silver/eea_station_city_mapping.csv- \data/silver/eea_station_city_mapping.parquet
### Current Mapping Status Per City

The Phase 3 QA follow-up resolved the previous placeholder mappings for the six
non-pilot cities by querying the official EEA ArcGIS station metadata layer on
2026-05-30. Each starter city now has at least one selected station whose popup
metadata indicates PM2.5, PM10, and NO2 availability.

| city_id | Selected station | Status | Constraint |
| --- | --- | --- | --- |
| `vienna_at` | `AT90TAB` Taborstrasse | selected | PM2.5, PM10, NO2 from 2013-2024. |
| `berlin_de` | `DEBE068` Berlin Mitte | selected | NO2+PM10 from 2013-2024; PM2.5 from 2020 only. |
| `paris_fr` | `FR04143` PARIS Centre | selected | Real source-file row validation still required before analysis. |
| `madrid_es` | `ES0118A` ESCUELAS AGUIRRE | selected | Real source-file row validation still required before analysis. |
| `rome_it` | `IT1906A` ARENULA | selected | Real source-file row validation still required before analysis. |
| `amsterdam_nl` | `NL00014` Amsterdam-Vondelpark | selected | Real source-file row validation still required before analysis. |
| `warsaw_pl` | `PL0592A` Warszawa-Marszalkowska | selected | Real source-file row validation still required before analysis. |
| `prague_cz` | `CZ0ARIE` Praha 2-Riegrovy sady | selected | Real source-file row validation still required before analysis. |

### Mapping QA Follow-Up

The previous unresolved mapping decision for Paris, Madrid, Rome, Amsterdam,
Warsaw, and Prague is closed. The project now tests that every starter city has
a selected station and that no station ID starts with `PLACEHOLDER`.

Remaining limitation: EEA measurement files still need to be downloaded locally
and row-validated before the EEA Silver output is treated as final analytical
input.

### Berlin PM2.5 Coverage Constraint

\DEBE068\ (Berlin Mitte) has PM2.5 measurements only from 2020 onwards. Any
Phase 3 ingestion or Silver aggregation for \erlin_de\ PM2.5 must document
this gap explicitly. Historical PM2.5 comparisons for Berlin before 2020 are
not possible from this station alone.

### Phase 3.3 Scope Boundary

**Included in this issue (3.3):**

- Station mapping structure implemented as a local Python builder.
- All 8 starter cities have selected station mappings.
- All 8 starter cities have at least one mapping entry.
- Validation ensures all \city_id\ values exist in \city_reference.parquet\.
- Tests cover structure, integrity, status values, distances, and Parquet roundtrip.

**Not included in this issue:**

- Bulk EEA station metadata download.
- EEA loader implementation (Issue 3.4).
- Silver Parquet output for air quality measurements (Issue 3.6).
- Kafka or Spark Structured Streaming.
- Gold tables.

## Wikipedia Metadata Join Rules

Wikipedia metadata is contextual city metadata, not official ground truth. Later
phases may use it to enrich the city reference model for documentation,
comparison, and analysis context, but EEA measurements and Open-Meteo API data
must not depend on Wikipedia values being complete.

Wikipedia metadata must attach to the city reference model through `city_id`.
Page titles, page URLs, translated names, and free-text city names are traceable
source attributes only; they are not downstream join keys.

### Planned Wikipedia Metadata Fields

| city reference field | source meaning | handling rule |
| --- | --- | --- |
| wikipedia_page_title | Expected English Wikipedia page title for the city. | Store as linkage metadata; do not use as join key. |
| wikipedia_url | Expected page URL for traceability. | Store as source trace; do not fetch during Phase 2. |
| population | Contextual population value where parseable. | Nullable integer; keep null when ambiguous or missing. |
| area_km2 | Contextual area value where parseable. | Nullable float; keep null when ambiguous or missing. |
| population_density | Contextual or derived density value. | Nullable float; derive only when population and area are reliable. |
| latitude | Canonical city coordinate. | Keep from the city reference model; do not overwrite from Wikipedia without review. |
| longitude | Canonical city coordinate. | Keep from the city reference model; do not overwrite from Wikipedia without review. |
| country_code | Canonical country context. | Keep from the city reference model; Wikipedia country text is a validation clue only. |
| wikipedia_metadata_notes | Parsing, ambiguity, missing-field, or fallback notes. | Required whenever a planned metadata value is null, ambiguous, conflicting, or manually reviewed. |

### Null And Ambiguity Handling

- If `population` or `area_km2` cannot be parsed confidently, keep the field
  null and populate `wikipedia_metadata_notes`.
- If Wikipedia contains multiple population, area, or coordinate values, do not
  choose one silently; document the ambiguity and keep the target field null
  until a later parser rule is approved.
- If a page is missing, redirected, disambiguated, or not clearly about the
  city, keep metadata fields null and document the issue.
- Do not infer values from unrelated pages, search snippets, dashboards, or
  other websites.
- Do not treat Wikipedia coordinates as a replacement for the canonical
  `latitude` and `longitude` defined in the city reference table.
- Production HTML parsing and metadata Parquet output remain out of scope for
  Phase 2 unless a later issue explicitly activates them.

## Open-Meteo Mapping Rules

Open-Meteo Air Quality requests are coordinate-based. Later Open-Meteo API
client and event schema work must use the canonical city reference `latitude`
and `longitude` for each `city_id`. Phase 2 records the mapping rules only; it
does not implement an API client, event schema, Kafka producer, scheduler, or
streaming job.

### Coordinate Usage

| city reference field | Open-Meteo usage | rule |
| --- | --- | --- |
| city_id | Internal city join key | Carry into future Open-Meteo events and downstream joins. |
| latitude | API request latitude | Use the fixed WGS84 coordinate from the city reference table. |
| longitude | API request longitude | Use the fixed WGS84 coordinate from the city reference table. |
| country_code | Context and validation | Preserve in future events for traceability; do not use as API coordinate input. |
| open_meteo_coordinate_notes | Coordinate review notes | Record assumptions, corrections, or later coordinate review decisions. |

Coordinates should be treated as city-level reference coordinates, not station
locations. If a later phase changes a coordinate, the change must be documented
because it can affect API responses and comparability.

### Pollutant Field Mapping

| project pollutant | Open-Meteo hourly field | planned internal meaning |
| --- | --- | --- |
| PM2.5 | `pm2_5` | Fine particulate matter. |
| PM10 | `pm10` | Particulate matter up to 10 micrometers. |
| NO2 | `nitrogen_dioxide` | Nitrogen dioxide. |

The Phase 1 source spike confirmed these Open-Meteo field names for the pilot
cities. Later Phase 5 work should map these fields into a stable internal event
schema before Kafka is introduced in Phase 6.

### Timezone Assumption

Open-Meteo requests should use `timezone=UTC` unless a later ADR changes this
decision. Future events should carry UTC timestamps explicitly, for example
`event_time_utc` and `ingestion_time_utc`, so Spark and Parquet outputs can be
compared consistently across cities.

### Phase 5 Handoff

Phase 5 may implement the Open-Meteo client and event schema using these rules.
Phase 2 must stop at documentation and city reference support. No API calls,
production client behavior, event schema implementation, Kafka producer, or
Spark streaming logic belongs in this issue.

## Phase 2 Scope Boundary

Allowed in Phase 2:

- define stable city identifiers,
- document the city reference scope,
- design the city reference schema,
- prepare EEA station mapping rules,
- prepare Wikipedia metadata join rules,
- prepare Open-Meteo coordinate and field mapping rules,
- add city reference validation tests.

Not allowed in Phase 2:

- EEA data download or ingestion,
- production Wikipedia scraping,
- Open-Meteo production client behavior,
- Kafka producer implementation,
- Spark Structured Streaming,
- Bronze/Silver/Gold transformations beyond the local city reference outputs
  planned for later Phase 2 issues,
- final analytics or visualizations.

## Phase 3 EEA Batch Ingestion Data Model

This section documents the EEA input field expectations and the normalized
Silver output schema for Phase 3. As of Issue 3.6, the pandas/pyarrow-based EEA
loader, validation path, aggregation, and explicit local Silver Parquet writer
are implemented. The section still does not represent Spark streaming, Gold
tables, Open-Meteo merging, or any dataset download.

### Phase 3 Execution Mode

Parquet-producing Phase 3 work must use the reliable project execution mode:

```text
SPARK_MASTER_URL=local[*]
```

or a local pandas/pyarrow path in the project environment. The FH Spark cluster
must not be used for final Phase 3 Parquet persistence unless a confirmed shared
storage path is provided and tested. This follows ADR-004.

### EEA Input Field Expectations

EEA historical time series files (downloaded as station-level Parquet or CSV
from the EEA Air Quality Download Service) expose station-based measurement
records. Phase 3 must expect and handle the following source concepts:

| Source concept | Expected EEA field(s) | Notes |
| --- | --- | --- |
| Station identity | `AirQualityStation`, `AirQualityStationEoICode`, `AQStationName` | Used to join against the station-to-city mapping table; not used directly as a downstream join key. |
| Measurement timestamp | `DatetimeBegin`, `DatetimeEnd`, or equivalent period fields | Exact column name must be verified on first real file inspection; UTC normalisation required. |
| Pollutant label | `AirPollutant` or equivalent string | Source labels vary; must be mapped to internal canonical names (see pollutant normalisation table below). |
| Measured value | `Concentration` or equivalent numeric field | Must be non-negative after quality filtering; missing values must be handled explicitly. |
| Unit | `Unit` or equivalent | Expected to be `µg/m³` for PM2.5, PM10, and NO2; must be verified per file before processing. |
| Validity or quality flag | `Validity`, `AggType`, or equivalent flag field | Rows with known-bad validity flags must be excluded before aggregation. |
| Station latitude | `Latitude` | Used only for station-to-city distance review; not carried into Silver output. |
| Station longitude | `Longitude` | Used only for station-to-city distance review; not carried into Silver output. |

> **Important:** Exact EEA column names must be verified against a real
> controlled sample file during Issue 3.4 (EEA loader implementation). The
> field names above are based on Phase 1 station metadata observations and
> EEA documentation conventions. If the real file exposes different column
> names, the loader must map them to the internal concepts listed here without
> changing this schema contract.

### Pollutant Normalisation

Phase 3 processes exactly 3 core pollutants. Source pollutant labels from EEA
files must be normalised to these internal canonical names before any
aggregation or output:

| Internal canonical name | Accepted EEA source labels | Unit | Notes |
| --- | --- | --- | --- |
| `PM2.5` | `PM2.5`, `Particles < 2.5 µm (aerodynamic diameter)`, `PM2,5` | `µg/m³` | Fine particulate matter. |
| `PM10` | `PM10`, `Particles < 10 µm (aerodynamic diameter)` | `µg/m³` | Particulate matter up to 10 micrometers. |
| `NO2` | `NO2`, `Nitrogen dioxide (air)`, `Nitrogen dioxide` | `µg/m³` | Nitrogen dioxide. |

Any EEA source record whose pollutant label does not map to one of these three
canonical names must be silently excluded from Phase 3 processing. No other
pollutants are in scope.

### EEA Silver City Daily Schema

The normalized Silver output for Phase 3 is stored at:

```
data/silver/eea_city_daily.parquet
```

This file aggregates station-level measurements to city/day/pollutant rows
using the station-to-city mapping defined in Phase 2 and extended in Issue 3.3.
It is the stable input for Phase 8 Gold table construction and Phase 9
analysis.

| field | type | required | nullability | rule |
| --- | --- | --- | --- | --- |
| `city_id` | string | yes | non-null | Canonical city join key from `city_reference.parquet`. Must not be a free-text city name. |
| `date` | date | yes | non-null | UTC-normalised measurement date (daily granularity). Derived from `DatetimeBegin` or equivalent timestamp field. |
| `pollutant` | string | yes | non-null | One of `PM2.5`, `PM10`, `NO2` (canonical internal names only). |
| `mean_value` | float | yes | non-null | Daily mean concentration across all valid observations for the city/day/pollutant combination. |
| `min_value` | float | no | nullable | Daily minimum concentration. Null if only one observation is available. |
| `max_value` | float | no | nullable | Daily maximum concentration. Null if only one observation is available. |
| `observation_count` | integer | yes | non-null | Number of valid, non-negative observations used in the aggregation. Must be at least 1. |
| `unit` | string | yes | non-null | Measurement unit as normalised from the EEA source; expected to be `µg/m³`. |
| `source` | string | yes | non-null | Always `eea` for this Silver table. Used to distinguish historical EEA batch data from live Open-Meteo data. |
| `processing_time_utc` | timestamp | yes | non-null | UTC timestamp of when the row was generated by the Phase 3 loader. Provides technical traceability. |

#### Schema Constraints And Validation Rules

- `city_id` must exist in `data/silver/city_reference.parquet`; rows with
  unmapped station IDs must be excluded and logged.
- `date` must be a valid calendar date; rows with unparseable timestamps must
  be excluded and counted as data quality defects.
- `pollutant` must be exactly one of `PM2.5`, `PM10`, `NO2`; no other values
  are permitted.
- `mean_value` must be non-negative (≥ 0); negative values indicate invalid
  measurements and must be excluded before aggregation.
- `observation_count` must be ≥ 1; rows with zero valid observations must not
  be written.
- `unit` must be consistent within a city/day/pollutant group; mixed units
  within a group must trigger a data quality warning.
- `source` must always be the string literal `eea`.

#### Data Flow

```mermaid
flowchart LR
    raw["EEA station-level files\ndata/bronze/eea/"]
    filter["Filter: PM2.5, PM10, NO2 only"]
    valid["Validate: non-negative values,\nparseable timestamps, known units"]
    map["Map station_id -> city_id\nvia station-to-city mapping"]
    agg["Aggregate by city_id, date, pollutant\nmean, min, max, observation_count"]
    silver["data/silver/eea_city_daily.parquet"]

    raw --> filter --> valid --> map --> agg --> silver
```

### Historical vs. Live Data Separation

Historical EEA batch data and live Open-Meteo API data are **different data
contexts** and must never be silently merged into a single Silver or Gold
table without an explicit, documented decision.

| Attribute | Historical EEA | Live Open-Meteo |
| --- | --- | --- |
| Data type | Historical validated measurements | Current or forecast API data |
| Temporal coverage | Multi-year historical records (e.g. 2018–2024) | Current window (days to weeks) |
| Spatial basis | Station-based, mapped to `city_id` | Coordinate-based, mapped to `city_id` |
| Silver table | `data/silver/eea_city_daily.parquet` | `data/silver/open_meteo_city_hourly/` |
| `source` field value | `eea` | `open_meteo` |
| Phase | Phase 3 | Phase 5 + Phase 7 |

No Phase 3 code or transformation may read from, write to, or join with
Open-Meteo Silver or Gold tables. The `source = 'eea'` field in the Silver
schema makes this separation machine-checkable at all downstream layers.

### Phase 3.6 Silver Parquet Output Implementation

Issue 3.6 implements the reproducible write boundary for
`data/silver/eea_city_daily.parquet`.

Implemented functions in `src/ingestion/eea_loader.py`:

- `aggregate_to_city_daily(mapped_df)` groups normalized EEA rows by
  `city_id`, UTC `date`, `pollutant`, and `unit`.
- `write_eea_city_daily_parquet(silver_df, output_path)` validates the Silver
  schema and writes Parquet only when explicitly called.
- `build_eea_city_daily_parquet(input_path, station_mapping_df, output_path)`
  loads a caller-provided local EEA CSV/Parquet file, maps stations through the
  selected station mapping, aggregates to Silver, and writes the Parquet output.

The writer enforces:

- output columns must match `SILVER_COLUMNS`;
- `pollutant` must be limited to PM2.5, PM10, and NO2;
- `source` must be exactly `eea`;
- required join and measurement fields must be non-null;
- output is written only through an explicit function call.

The generated file is a local Phase 3 artifact and remains ignored by Git under
the repository data policy.

### Phase 3.2 Scope Boundary

**Included in this issue (3.2):**

- EEA input field expectations documented.
- Pollutant normalisation table defined.
- Silver output schema defined with all required fields, types, nullability, and validation rules.
- Historical vs. live data separation documented.

**Not included in this issue:**

- Full EEA data ingestion or download.
- Station-to-city mapping implementation (Issue 3.3).
- EEA loader implementation (Issue 3.4).
- Data quality validation implementation (Issue 3.5).
- Silver Parquet output (Issue 3.6).
- Open-Meteo event schema (Phase 5).
- Kafka or Spark Structured Streaming.
- Gold tables.

## Phase 4 Wikipedia City Metadata Schema

Wikipedia metadata is contextual city metadata, not official ground truth.
This schema is defined before implementation to enable testing and schema
validation. This section extends the Phase 2 Wikipedia Metadata Join Rules
(see above) with a concrete Silver output schema.

### Wikipedia City Metadata Schema

| field | type | required | nullability | rule |
| --- | --- | --- | --- | --- |
| `city_id` | string | yes | non-null | Join key from `city_reference.parquet`; must match exactly; must not be a free-text city name. |
| `city_name` | string | yes | non-null | Display name from the Wikipedia page title. |
| `population` | integer | no | nullable | Contextual value; null when not parseable; see `metadata_notes`. |
| `area_km2` | float | no | nullable | Contextual area in km²; null when not parseable; see `metadata_notes`. |
| `population_density` | float | no | nullable | Calculated when `population` and `area_km2` are both non-null; otherwise null. |
| `country` | string | no | nullable | Contextual country name from infobox; null when missing or ambiguous. |
| `wikipedia_url` | string | yes | non-null | Source URL of the scraped Wikipedia page; required for reproducibility. |
| `scraped_at` | string | yes | non-null | ISO 8601 UTC timestamp of the scraping run. |
| `metadata_notes` | string | yes | non-null | Documents parse failures, ambiguous values, or missing fields; `ok` when everything parsed. |
| `source` | string | yes | non-null | Always `wikipedia`. |

### city_id Join Contract

- `city_id` is the sole join key between `city_metadata.parquet` and
  `city_reference.parquet`.
- Every row must have a non-null `city_id` matching an entry in
  `city_reference.parquet`.
- Page titles, URLs, and free-text names are traceability fields only;
  they are never join keys.
- Wikipedia values are contextual and must not override `city_reference.parquet`
  coordinate or country code fields.

### Null And Missing Field Rules

- If a field cannot be parsed, set it to null and add a note in
  `metadata_notes`.
- Never guess or infer values from unrelated pages.
- A city with all nullable fields null is still a valid row if `city_id`,
  `city_name`, `wikipedia_url`, `scraped_at`, `metadata_notes`, and `source`
  are present.
- `population_density` is only computed when both `population` and `area_km2`
  are non-null.

### Silver Output Path

```
data/silver/city_metadata.parquet
```

Produced by Phase 4 Issue 4.6. Not yet implemented in this issue. Git-ignored.

### Contextual-Only Status

Wikipedia values must not be treated as official statistical ground truth,
analytical baselines, or pipeline dependencies. EEA measurements and
Open-Meteo data must not depend on Wikipedia values being complete.

### Phase 4.2 Scope Boundary

**Included in this issue (4.2):**

- Wikipedia City Metadata Schema defined with all fields, types, nullability,
  and validation rules.
- city_id join contract documented.
- Null and missing field rules documented.
- Silver output path declared.
- Contextual-only status documented.
- Schema cells added to notebook 03.

**Not included in this issue:**

- Python scraper code or HTML parsing implementation.
- Silver Parquet file generation (`city_metadata.parquet`).
- Open-Meteo, Kafka, or Spark work.
- Changes to `docs/data_sources.md` (updated in Issue 4.1).

## Later Data Model Work

Pending:

- Define Bronze schema detail per source as loaders are implemented.
- Define Silver canonical model for city and air quality joins (Phase 3 EEA
  schema is the first Silver definition; Phase 4 Wikipedia Silver schema is
  defined in this document; Open-Meteo Silver schema follows in Phase 5).
- Define Gold analytical tables for the project research question (Phase 8).
