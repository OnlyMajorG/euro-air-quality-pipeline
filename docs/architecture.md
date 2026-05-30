# Architecture

The project uses a notebook-only implementation model. Each implementation step is documented and executed in one ordered Jupyter notebook. Supporting Markdown files explain architecture, source assumptions, cluster limitations, and decisions.

## Pipeline Architecture

1. EEA historical files are loaded as the file/batch source.
2. Wikipedia city pages are fetched and parsed as the web scraping source.
3. Open-Meteo Air Quality API responses are converted into events.
4. Open-Meteo events are written to a group-specific Kafka topic.
5. Spark Structured Streaming reads Kafka events and writes Parquet.
6. Silver and Gold Parquet datasets support visual analysis and storytelling.

## Notebook-Only Implementation

Implementation logic lives in notebooks `00` through `08`. The repository intentionally does not use a `src/` package or `tests/` folder as the primary implementation and QA layer because the course deliverable is a public GitHub repository of notebooks.

## Execution Modes

- `local_project`: standard mode, `SPARK_MASTER_URL=local[*]`, reliable Parquet output under `data/`.
- `fh_cluster_connectivity`: cluster smoke-test mode only.
- `fh_cluster_shared_storage`: optional only after a real shared storage path is confirmed.
