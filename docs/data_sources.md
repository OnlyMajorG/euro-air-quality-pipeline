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

Open-Meteo is the REST API source and Kafka event source. API fields are mapped as PM2.5 -> `pm2_5`, PM10 -> `pm10`, and NO2 -> `nitrogen_dioxide`. Kafka output must use a group-specific topic such as `bdeng_gXX_air_quality_live`.

## Sample Data Policy

Generated data under `data/` is local and ignored by Git. Tiny samples may be created during notebook execution, but large raw files, secrets, credentials, and uncontrolled generated data must not be committed.

## Phase 0 to 4 Implementation Notes

| Phase | Source or artifact | Notebook | Status | Notes |
| --- | --- | --- | --- | --- |
| Phase 1 | Open-Meteo source spike | `01_source_spike_and_cluster_check.ipynb` | implemented as guarded source check | Set `RUN_SOURCE_SPIKES=true` to create tiny JSON samples. |
| Phase 1 | Wikipedia source spike | `01_source_spike_and_cluster_check.ipynb` | implemented as guarded source check | Set `RUN_SOURCE_SPIKES=true` to create tiny HTML samples. |
| Phase 1 | EEA feasibility | `01_source_spike_and_cluster_check.ipynb` | documented | EEA is treated as the file/batch source; full download is not automated. |
| Phase 2 | City reference | `02_city_reference_model.ipynb` | implemented | Writes `data/silver/city_reference.csv` and `.parquet` locally. |
| Phase 3 | EEA batch ingestion | `03_eea_batch_ingestion.ipynb` | implemented | Uses local EEA files if present; otherwise creates a controlled sample for reproducibility. |
| Phase 4 | Wikipedia scraping | `04_wikipedia_web_scraping.ipynb` | implemented | Fetches raw HTML when enabled and writes `data/silver/city_metadata.parquet`. |

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
