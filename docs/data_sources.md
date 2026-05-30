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
