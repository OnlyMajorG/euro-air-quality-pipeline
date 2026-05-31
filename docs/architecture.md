# Architecture

The project uses a notebook-only implementation model. Each implementation step is documented and executed in one ordered Jupyter notebook. Supporting Markdown files explain architecture, source assumptions, cluster limitations, and decisions.

## Pipeline Architecture

1. EEA historical files are loaded as the file/batch source.
2. Wikipedia city pages are fetched and parsed as the web scraping source.
3. Open-Meteo Air Quality API responses are converted into events.
4. Open-Meteo raw JSON and validated JSONL event batches are stored locally as Bronze evidence.
5. When a reachable broker is configured, Open-Meteo events are written to a group-specific Kafka topic and verified with a bounded consumer smoke test.
6. Spark Structured Streaming reads Kafka events, validates the explicit schema, joins city context, and writes Parquet.
7. Phase 7 validates Silver contracts, creates historical Gold tables, keeps the live snapshot separate, and writes a cross-table quality report.
8. Gold Parquet datasets support visual analysis and storytelling.

## Phase 5 Event Contract

Notebook `05_open_meteo_api_and_kafka_producer.ipynb` emits flat JSON events with `event_id`, `schema_version`, `source`, `city_id`, `event_time_utc`, `ingestion_time_utc`, `data_status`, `pm2_5`, `pm10`, and `no2`. The flat schema is the explicit input contract for Spark Structured Streaming in Phase 6. `data_status` allows downstream exclusion of controlled fallback records.

## Kafka Execution Modes

- `KAFKA_MODE=kafka`: strict FH evidence mode. Broker errors fail the notebook.
- `KAFKA_MODE=auto`: try Kafka and use the mock only when `ALLOW_KAFKA_MOCK_FALLBACK=true`.
- `KAFKA_MODE=mock`: local JSONL mock broker for reproducible offline producer/consumer mechanics.

## Spark Kafka Execution Modes

- `SPARK_KAFKA_MODE=kafka`: strict FH evidence mode. Spark must initialize `readStream.format("kafka")`; broker or connector errors fail the notebook.
- `SPARK_KAFKA_MODE=auto`: try the configured Kafka broker and Spark Kafka connector first, then use the local Spark file-stream mock only when `ALLOW_SPARK_KAFKA_MOCK_FALLBACK=true`.
- `SPARK_KAFKA_MODE=mock`: local reproducibility mode. Spark Structured Streaming reads Phase-5 JSONL events via `readStream.text()`, then executes the same parsing, validation, joins, checkpoints and Parquet read-back.

The local Spark file-stream mock is a functional fallback, not proof that Spark read Kafka. The final FH evidence run must report `selected_source_mode=kafka`.

## Gold Layer Strategy

Notebook `07_gold_layer_and_data_quality.ipynb` writes driver-local Gold Parquet files for reproducibility. It checks configured Kafka and Spark endpoints and can execute a Spark-worker storage write/readback probe with `RUN_PHASE7_SPARK_STORAGE_PROBE=true`. Until that probe succeeds on FH JupyterHub, cluster shared storage is not claimed.

The live snapshot prefers Phase-6 Silver streaming Parquet. If it is absent locally, Phase-7 reconstruction from Phase-5 JSONL is allowed only as an explicit functional fallback with `live_input_mode=phase5_jsonl_mock_reconstruction`.

## Notebook-Only Implementation

Implementation logic lives in notebooks `00` through `08`. The repository intentionally does not use a `src/` package or `tests/` folder as the primary implementation and QA layer because the course deliverable is a public GitHub repository of notebooks.

## Execution Modes

- `local_project`: standard mode, `SPARK_MASTER_URL=local[*]`, reliable Parquet output under `data/`.
- `fh_cluster_connectivity`: cluster smoke-test mode only.
- `fh_cluster_shared_storage`: optional only after a real shared storage path is confirmed.
