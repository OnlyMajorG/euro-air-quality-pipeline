# Data Sources

## Overview

| Source | Source type | Purpose | Notebook |
| --- | --- | --- | --- |
| EEA historical air quality data | File/batch | Historical PM2.5, PM10, NO2 observations | `03_eea_batch_ingestion.ipynb` |
| Wikipedia city pages | Web scraping | City context such as population, area, density | `04_wikipedia_web_scraping.ipynb` |
| Open-Meteo Air Quality API | REST API | Current air-quality events for Kafka path | `05_open_meteo_api_and_kafka_producer.ipynb` |

## EEA Historical Data

EEA data is the historical file/batch source. The notebook expects locally provided CSV or Parquet files and does not download large datasets automatically. Measurements are filtered to PM2.5, PM10, and NO2, normalized to a common schema, mapped to `city_id`, and aggregated to daily city/pollutant rows.

## Wikipedia

Wikipedia is used only for contextual city metadata. HTML parsing is fragile; missing or ambiguous values remain null and are explained in notes instead of being guessed.

## Open-Meteo

Open-Meteo is the REST API source and Kafka event source. API fields are mapped as PM2.5 -> `pm2_5`, PM10 -> `pm10`, and NO2 -> `nitrogen_dioxide`. Kafka output must use a group-specific FH topic such as `LIVE-bdeng_gXX_air_quality_live`.

Notebook `05_open_meteo_api_and_kafka_producer.ipynb` stores one raw Bronze JSON response per city, an ingestion manifest and a validated JSONL event batch under `data/bronze/open_meteo_raw/`. The internal event schema maps Open-Meteo `nitrogen_dioxide` to flat field `no2` for the Phase-6 Spark schema.

If the API is temporarily unreachable, the notebook can emit visibly labeled controlled fallback payloads. They are allowed for mechanics and reproducibility checks only, not for analytical conclusions.

By default, Phase 5 publishes the latest complete pollutant hour per city. `OPEN_METEO_MAX_HOURS_TO_SEND` can raise that bounded number for controlled replay tests.

## Sample Data Policy

Generated data under `data/` is local and ignored by Git. Tiny samples may be created during notebook execution, but large raw files, secrets, credentials, and uncontrolled generated data must not be committed.

Phase 3 persists `data_status=real_eea_file` or `data_status=controlled_sample_fallback` into Silver and Gold Parquet. Phase 7 therefore prevents a controlled EEA sample from being mistaken for empirical evidence.

## Phase 0 to 4 Implementation Notes

| Phase | Source or artifact | Notebook | Status | Notes |
| --- | --- | --- | --- | --- |
| Phase 1 | Open-Meteo source spike | `01_source_spike_and_cluster_check.ipynb` | implemented as guarded source check | Set `RUN_SOURCE_SPIKES=true` to create tiny JSON samples. |
| Phase 1 | Wikipedia source spike | `01_source_spike_and_cluster_check.ipynb` | implemented as guarded source check | Set `RUN_SOURCE_SPIKES=true` to create tiny HTML samples. |
| Phase 1 | EEA feasibility | `01_source_spike_and_cluster_check.ipynb` | documented | EEA is treated as the file/batch source; full download is not automated. |
| Phase 2 | City reference | `02_city_reference_model.ipynb` | implemented | Writes `data/silver/city_reference.csv` and `.parquet` locally. |
| Phase 3 | EEA batch ingestion | `03_eea_batch_ingestion.ipynb` | implemented | Uses local EEA files if present; otherwise creates a controlled sample for reproducibility. |
| Phase 4 | Wikipedia scraping | `04_wikipedia_web_scraping.ipynb` | implemented | Fetches raw HTML when enabled and writes `data/silver/city_metadata.parquet`. |
| Phase 5 | Open-Meteo REST API | `05_open_meteo_api_and_kafka_producer.ipynb` | implemented with controlled fallback | Fetches cities, stores Bronze JSON and writes provenance-labeled local JSONL events. |
| Phase 5 | Kafka producer and consumer evidence | `05_open_meteo_api_and_kafka_producer.ipynb` | implemented with strict FH and local mock modes | Set `KAFKA_MODE=kafka` and `RUN_OPEN_METEO_KAFKA_PRODUCER=true` for the FH evidence run. |
| Phase 6 | Spark Kafka processing | `06_spark_structured_streaming_kafka_to_parquet.ipynb` | implemented with strict FH and Spark file-stream fallback modes | Final evidence requires `selected_source_mode=kafka`. |
| Phase 7 | Gold layer and data quality | `07_gold_layer_and_data_quality.ipynb` | implemented | Creates five Gold Parquets and records historical/live fallback provenance. |

## Gold Output Contracts

| Dataset | Context | Purpose |
| --- | --- | --- |
| `city_air_quality_daily_summary.parquet` | `eea_historical` | Historical daily city/pollutant values |
| `pollutant_ranking_by_city.parquet` | `eea_historical` | Pollutant-specific city rankings |
| `city_context_air_quality.parquet` | `eea_historical` | Ranking values joined with Wikipedia context |
| `live_air_quality_latest.parquet` | `open_meteo_live` | Separate latest API/Kafka snapshot |
| `data_quality_summary.parquet` | quality metadata | Row counts, duplicates, missing values, coverage and provenance |

## Open-Meteo Kafka Event Contract

| Column | Meaning |
| --- | --- |
| `event_id` | deterministic event identifier |
| `schema_version` | event contract version, currently `1.0` |
| `source` | `open_meteo` |
| `city_id` | stable city join key |
| `event_time_utc` | Open-Meteo hourly observation time |
| `ingestion_time_utc` | notebook ingestion timestamp |
| `data_status` | API/local/fallback provenance for downstream filtering |
| `pm2_5` | PM2.5 concentration |
| `pm10` | PM10 concentration |
| `no2` | NO2 concentration mapped from Open-Meteo `nitrogen_dioxide` |

## EEA Silver Output Contract

`data/silver/eea_city_daily.parquet` contains:

| Column | Meaning |
| --- | --- |
| `city_id` | stable city join key |
| `date` | daily aggregation date |
| `pollutant` | PM2.5, PM10 or NO2 |
| `mean_value` | daily mean concentration |
| `min_value` | daily minimum concentration |
| `max_value` | daily maximum concentration |
| `observation_count` | number of source measurements in the group |
| `unit` | source measurement unit |
| `source` | `eea` |
| `processing_time_utc` | notebook processing timestamp |
| `data_status` | `real_eea_file` or `controlled_sample_fallback` provenance marker |

## Wikipedia Silver Output Contract

`data/silver/city_metadata.parquet` contains one row per `city_id` where possible:

| Column | Meaning |
| --- | --- |
| `city_id` | stable city join key |
| `city_name` | display name |
| `country_code` | country code |
| `population` | parsed contextual population value, nullable |
| `area_km2` | parsed contextual area value, nullable |
| `population_density` | parsed or derived density, nullable |
| `source_url` | Wikipedia page URL |
| `metadata_source` | `wikipedia` |
| `processed_at_utc` | processing timestamp |
| `parse_status` | `success`, `partial`, or `failed` |
| `parse_notes` | parser notes and caveats |
