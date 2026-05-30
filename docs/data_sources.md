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
