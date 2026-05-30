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
