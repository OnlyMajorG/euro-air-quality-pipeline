# Data Sources

## Phase 1 Pilot Scope

Phase 1 is a source spike and feasibility check. It uses a deliberately small
pilot scope so each data source can be inspected manually before the project
commits to the Phase 2 city reference model.

This section is **not** the final city reference model. It does not create
`city_reference.parquet`, does not define EEA station matching, and does not
implement ingestion logic.

### Pilot Cities

| city_name | country_code | latitude | longitude | reason |
| --- | --- | ---: | ---: | --- |
| Vienna | AT | 48.2082 | 16.3738 | Likely coverage across Open-Meteo, Wikipedia, and EEA; central European capital with expected monitoring availability. |
| Berlin | DE | 52.5200 | 13.4050 | Likely coverage across Open-Meteo, Wikipedia, and EEA; large European capital with expected monitoring availability. |

### Target Pollutants

Phase 1 checks the planned core pollutants where each source supports them:

| pollutant | Open-Meteo check | EEA check | Wikipedia check | Notes |
| --- | --- | --- | --- | --- |
| PM2.5 | Check API field availability. | Check historical availability for pilot cities or nearby stations. | Not expected as direct city metadata. | Use for air quality comparison if available. |
| PM10 | Check API field availability. | Check historical availability for pilot cities or nearby stations. | Not expected as direct city metadata. | Use for air quality comparison if available. |
| NO2 | Check API field availability. | Check historical availability for pilot cities or nearby stations. | Not expected as direct city metadata. | Open-Meteo may expose this as `nitrogen_dioxide`; field name must be verified. |

If a pollutant is unavailable or named differently in a source, Phase 1 must
record that as a source-specific constraint. It must not silently replace the
approved pollutant scope or expand to additional pollutants.

### Source Spike Usage

The same two pilot cities must be used consistently across the Phase 1 checks:

| Source | Phase 1 use | Expected evidence |
| --- | --- | --- |
| Open-Meteo Air Quality API | Verify API reachability, field names, timestamps, units, and missing-value behavior for Vienna and Berlin. | Notebook notes and/or tiny JSON evidence if allowed by data hygiene rules. |
| EEA historical air quality data | Verify historical availability for Vienna and Berlin or clearly document station/city constraints. | Documentation of access path, fields, pollutant availability, and mapping risk. |
| Wikipedia city pages | Verify raw HTML availability and metadata candidates for Vienna and Berlin. | Notebook notes and/or tiny HTML evidence if allowed by data hygiene rules. |

### Phase 1 Boundaries

Allowed:

- Document source feasibility.
- Inspect two pilot cities.
- Check PM2.5, PM10, and NO2 availability.
- Record source-specific constraints.

Not allowed in this issue:

- Final city reference model.
- `city_reference.parquet`.
- Station-radius matching.
- Production schemas.
- Kafka producer logic.
- Spark processing logic.
- Full ingestion jobs.

## Open-Meteo Phase 1 Feasibility

Status: **usable**

Open-Meteo Air Quality API access was tested for the two Phase 1 pilot cities
with a deliberately small one-day hourly request. This was a source feasibility
check only. It did not create a reusable API client, Kafka event schema,
producer, scheduler, or streaming path.

### Request Scope

| city_name | country_code | latitude | longitude | request scope | evidence |
| --- | --- | ---: | ---: | --- | --- |
| Vienna | AT | 48.2082 | 16.3738 | `forecast_days=1`, hourly `pm10,pm2_5,nitrogen_dioxide`, `timezone=UTC` | `data/bronze/open_meteo_raw/sample_open_meteo_vienna_at.json` |
| Berlin | DE | 52.5200 | 13.4050 | `forecast_days=1`, hourly `pm10,pm2_5,nitrogen_dioxide`, `timezone=UTC` | `data/bronze/open_meteo_raw/sample_open_meteo_berlin_de.json` |

The evidence JSON files are intentionally small local source-spike samples.
They are stored under `data/bronze/open_meteo_raw/` and protected by the
repository data ignore rules.

### Observed Response Structure

| Area | Observed result |
| --- | --- |
| Top-level fields | `latitude`, `longitude`, `elevation`, `timezone`, `timezone_abbreviation`, `utc_offset_seconds`, `hourly_units`, `hourly` |
| Hourly fields | `time`, `pm10`, `pm2_5`, `nitrogen_dioxide` |
| Timestamp format | `hourly.time` values are ISO-8601-like hourly strings. Requests used `timezone=UTC`; response `utc_offset_seconds` was `0`. |
| Units | `hourly_units` reports pollutant units as micrograms per cubic meter (`ug/m3` equivalent). |
| Sample size | 24 hourly records per pilot city. |
| Missing values in sample | No missing values were observed for `pm10`, `pm2_5`, or `nitrogen_dioxide` in the two saved samples. |

### Pollutant Mapping

| Approved pollutant | Open-Meteo field observed | Phase 1 decision |
| --- | --- | --- |
| PM2.5 | `pm2_5` | Usable; field name differs from display label. |
| PM10 | `pm10` | Usable. |
| NO2 | `nitrogen_dioxide` | Usable with field-name mapping; do not expect an `no2` field. |

### Risks And Constraints

- Open-Meteo uses API field names rather than presentation labels. Future code
  must map NO2 to `nitrogen_dioxide` and PM2.5 to `pm2_5`.
- The Phase 1 sample proves short-window reachability only. It is not evidence
  for long-term availability or historical completeness.
- Future ingestion must handle missing values even though the two source-spike
  samples did not contain missing pollutant values.
- Open-Meteo current or forecast data must not be treated as directly
  equivalent to historical EEA measurements without clear context fields.

### Phase 1 Decision

Open-Meteo is **usable** for the planned REST API source and later Kafka path,
subject to explicit field mapping and missing-value handling in later phases.

## EEA Phase 1 Feasibility

Status: **usable with constraints**

EEA historical air quality data availability was checked through the EEA
station metadata and download service for the two Phase 1 pilot cities. This
was a metadata-level feasibility check only. It did not download full EEA time
series data, create an EEA ingestion job, run Spark, define station-radius
matching, or write Bronze/Silver/Gold outputs.

### Access Path

| Access path | Purpose | Phase 1 observation |
| --- | --- | --- |
| EEA station spatial service | Find monitoring stations and pollutant-specific availability near pilot cities. | ArcGIS REST layer `AirQualityDownloadServiceEUMonitoringStations/MapServer/0` is queryable and returns station metadata, coordinates, pollutant labels, year ranges, and Parquet download links in station popup metadata. |
| EEA Air Quality Download Service | Download selected air quality measurement time series. | EEA metadata describes country/city/pollutant filtering and zipped Parquet outputs for selected time series. |
| Station-level Parquet links | Download pollutant-specific validated E1a time series for individual stations. | Station metadata includes pollutant-specific Parquet links, but Phase 1 did not download those files. |

Relevant public service references:

- Station metadata REST service: `https://air.discomap.eea.europa.eu/arcgis/rest/services/AirQuality/AirQualityDownloadServiceEUMonitoringStations/MapServer`
- Station data viewer: `https://discomap.eea.europa.eu/App/AQViewer/index.html?fqn=Airquality_Dissem.b2g.AirQualityStatistics`
- Download web app referenced by station metadata: `https://eeadmz1-downloads-webapp.azurewebsites.net`

### Metadata Query Scope

The metadata query used the Phase 1 pilot city coordinates and a small bounding
box around each city. Returned station metadata was inspected for target
pollutants PM2.5, PM10, and NO2.

| city | metadata result | target pollutant evidence | key risk | decision |
| --- | --- | --- | --- | --- |
| Vienna | 37 nearby station records with at least one target pollutant in the inspected bounding box. | `Taborstraße` (`AT90TAB`) reports NO2, PM2.5, and PM10 for 2013-2024; `AKH` (`AT90AKC`) reports PM2.5, PM10, and NO2; `Stephansplatz` (`AT9STEF`) reports NO2. | Need a documented rule for selecting stations and avoiding arbitrary city-center bias. | usable with constraints |
| Berlin | 68 nearby station records with at least one target pollutant in the inspected bounding box. | `Berlin Mitte` (`DEBE068`) reports NO2 and PM10 for 2013-2024 and PM2.5 for 2020-2024; several nearby Berlin stations report NO2. | PM2.5 availability may have shorter history at some stations; station class and representativeness need review. | usable with constraints |

### Observed Or Expected Fields

| Field category | Observed or expected fields | Notes |
| --- | --- | --- |
| Station identity | `AirQualityStation`, `AirQualityStationEoICode`, `AQStationName`, `Country`, `CountryCode` | Observed in EEA station metadata. |
| Geometry | longitude, latitude | Returned by the ArcGIS REST query with `outSR=4326`. |
| Pollutant | PM2.5, PM10, NO2 labels in popup metadata and pollutant-specific Parquet links | Observed in station popup metadata. |
| Unit | `ug/m3` equivalent in popup metadata | Observed for PM2.5, PM10, and NO2 links. |
| Time coverage | pollutant-specific year ranges such as 2013-2024 or 2020-2024 | Observed in station popup metadata. |
| Measurement timestamp | expected measurement timestamp or period field in downloaded time series | Must be verified during the EEA ingestion phase before transformation logic is written. |
| Measurement value | expected numeric concentration value | Must be verified from a tiny controlled sample in the EEA ingestion phase. |
| Validity or quality flags | expected in EEA time series or metadata | Must be checked before using values analytically. |

### Timestamp Handling

The station metadata exposes pollutant-specific year coverage. The EEA
download documentation describes date filtering over measurement time ranges.
Phase 1 did not inspect full time series rows, so the exact timestamp column
name and timezone semantics must be verified before Phase 3 ingestion logic.

Future EEA processing must preserve:

- original measurement timestamp or period,
- source station identifier,
- pollutant,
- unit,
- measured value,
- quality or validity indicators where available,
- processing timestamp.

### Station-To-City Mapping Risk

EEA data is station-based, not city-based. Vienna and Berlin both have multiple
nearby stations with different pollutants, year ranges, station classes, and
representativeness. Phase 2 must define a transparent station selection rule
before any city-level EEA aggregation is created.

The project must not silently choose the nearest station without documenting:

- station distance to the city reference coordinate,
- pollutant availability,
- time coverage,
- station class or representativeness if available,
- fallback behavior when PM2.5, PM10, or NO2 is missing.

### Phase 1 Decision

EEA is **usable with constraints** for the planned file/batch historical source.
The main constraint is not basic availability; it is the station-to-city mapping
and pollutant/time-coverage selection rule required in Phase 2.
