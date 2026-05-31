# Architecture

The project uses a notebook-only implementation model. Each implementation step is documented and executed in one ordered Jupyter notebook. Supporting Markdown files explain architecture, source assumptions, cluster limitations, and decisions.

## Pipeline Architecture

1. EEA historical files are loaded as the file/batch source.
2. Wikipedia city pages are fetched and parsed as the web scraping source.
3. Open-Meteo Air Quality API responses are converted into events.
4. Open-Meteo raw JSON and validated JSONL event batches are stored locally as Bronze evidence.
5. When a reachable broker is configured, Open-Meteo events are written to a group-specific Kafka topic and verified with a bounded consumer smoke test.
6. Spark Structured Streaming reads Kafka events and writes Parquet.
7. Silver and Gold Parquet datasets support visual analysis and storytelling.

## Phase 5 Event Contract

Notebook `05_open_meteo_api_and_kafka_producer.ipynb` emits flat JSON events with `event_id`, `schema_version`, `source`, `city_id`, `event_time_utc`, `ingestion_time_utc`, `data_status`, `pm2_5`, `pm10`, and `no2`. The flat schema is the explicit input contract for Spark Structured Streaming in Phase 6. `data_status` allows downstream exclusion of controlled fallback records.

## Kafka Execution Modes

- `KAFKA_MODE=kafka`: strict FH evidence mode. Broker errors fail the notebook.
- `KAFKA_MODE=auto`: try Kafka and use the mock only when `ALLOW_KAFKA_MOCK_FALLBACK=true`.
- `KAFKA_MODE=mock`: local JSONL mock broker for reproducible offline producer/consumer mechanics.

## Notebook-Only Implementation

Implementation logic lives in notebooks `00` through `08`. The repository intentionally does not use a `src/` package or `tests/` folder as the primary implementation and QA layer because the course deliverable is a public GitHub repository of notebooks.

## Execution Modes

- `local_project`: standard mode, `SPARK_MASTER_URL=local[*]`, reliable Parquet output under `data/`.
- `fh_cluster_connectivity`: cluster smoke-test mode only.
- `fh_cluster_shared_storage`: optional only after a real shared storage path is confirmed.
