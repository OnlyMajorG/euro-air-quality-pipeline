# euro-air-quality-pipeline

## Executive Summary

This repository contains a notebook-only Big Data Engineering project about European air quality patterns across selected cities. The project combines one file/batch source, one web scraping source, and one REST API source, then uses Kafka and Spark Structured Streaming to demonstrate a full data-flow from source acquisition to Parquet outputs and final storytelling.

The implementation deliverables are ordered Jupyter notebooks. Supporting documentation, Mermaid diagrams, data folders, and presentation notes remain in the repository, but `src/` and `tests/` are intentionally not used as the primary implementation and QA layers.

## Guiding Question

How do PM2.5, PM10, and NO2 air-quality patterns differ across selected European cities, and what context can city metadata add to the interpretation?

## Official Requirement Mapping

| Course requirement | Planned implementation |
| --- | --- |
| At least three data sources | EEA file/batch, Wikipedia web scraping, Open-Meteo REST API |
| File or database source | `03_eea_batch_ingestion.ipynb` |
| Web scraping source | `04_wikipedia_web_scraping.ipynb` |
| REST API source | `05_open_meteo_api_and_kafka_producer.ipynb` |
| Kafka producer and topic | `05_open_meteo_api_and_kafka_producer.ipynb` |
| Spark reads from Kafka | `06_spark_structured_streaming_kafka_to_parquet.ipynb` |
| Store transformed results | Silver and Gold Parquet files under `data/` |
| Visualize data flow | `docs/diagrams/` and `08_analysis_visualization_and_storytelling.ipynb` |
| Tell a coherent story | `08_analysis_visualization_and_storytelling.ipynb` and `presentation/` |
| Document each step in notebooks | Notebooks `00` through `08` |

## Notebook Execution Order

| Order | Notebook | Purpose |
| ---: | --- | --- |
| 00 | `notebooks/00_project_scope_and_requirements.ipynb` | Scope, requirements, non-goals, and full pipeline overview |
| 01 | `notebooks/01_source_spike_and_cluster_check.ipynb` | Source feasibility and FH cluster connectivity notes |
| 02 | `notebooks/02_city_reference_model.ipynb` | Stable city IDs and city reference Parquet |
| 03 | `notebooks/03_eea_batch_ingestion.ipynb` | Historical EEA batch normalization and daily Silver Parquet |
| 04 | `notebooks/04_wikipedia_web_scraping.ipynb` | Wikipedia HTML fetch, parsing, and city metadata Parquet |
| 05 | `notebooks/05_open_meteo_api_and_kafka_producer.ipynb` | Open-Meteo API events and Kafka producer |
| 06 | `notebooks/06_spark_structured_streaming_kafka_to_parquet.ipynb` | Spark Structured Streaming from Kafka to Parquet |
| 07 | `notebooks/07_gold_layer_and_data_quality.ipynb` | Gold tables and cross-table quality checks |
| 08 | `notebooks/08_analysis_visualization_and_storytelling.ipynb` | Visualizations, figures, interpretation, and final story |

## Current Implementation Status

| Phase | Status | Evidence |
| --- | --- | --- |
| Phase 0: Notebook-only refactor | Complete | Target structure, ADRs, README, `.env` templates, `.gitignore`, archive notes |
| Phase 1: Source spike and cluster check | Implemented as guarded notebook | `01_source_spike_and_cluster_check.ipynb` contains Open-Meteo, Wikipedia, EEA and cluster checks |
| Phase 2: City reference model | Implemented | `02_city_reference_model.ipynb` builds, validates and writes `city_reference.csv` and `city_reference.parquet` |
| Phase 3: EEA batch ingestion | Implemented with local-file path and controlled fallback sample | `03_eea_batch_ingestion.ipynb` loads file data, normalizes, maps, aggregates and writes `eea_city_daily.parquet` |
| Phase 4: Wikipedia web scraping | Implemented as notebook workflow | `04_wikipedia_web_scraping.ipynb` fetches raw HTML when enabled, parses metadata and writes `city_metadata.parquet` |
| Phase 5 onward | Planned | Notebooks `05` to `08` contain the planned continuation and must be completed in later phases |

Generated data files are intentionally ignored by Git. To reproduce Phase 2 to 4 outputs locally, run notebooks `02`, `03`, and `04` in order.

## Data Sources

| Source | Type | Role |
| --- | --- | --- |
| EEA historical air quality data | File/batch | Historical PM2.5, PM10, and NO2 measurements |
| Wikipedia city pages | Web scraping | Contextual city metadata such as population and area |
| Open-Meteo Air Quality API | REST API | Current or near-current air-quality observations for Kafka path |

## Technology Stack

Python, Jupyter Notebook, Pandas, Requests, BeautifulSoup, Kafka, Spark Structured Streaming, Parquet, Matplotlib, and Mermaid diagrams.

## Execution Modes

| Mode | Configuration | Use |
| --- | --- | --- |
| `local_project` | `SPARK_MASTER_URL=local[*]` | Standard reliable notebook execution and Parquet output |
| `fh_cluster_connectivity` | `CLUSTER_SPARK_MASTER_URL=spark://<fh-spark-master>:7077` | Spark connectivity and compute smoke test only |
| `fh_cluster_shared_storage` | confirmed shared path required | Optional future mode for cluster Parquet output |

The FH Spark cluster was tested successfully for basic Spark connectivity and compute. HDFS/shared storage was not confirmed. Therefore, the standard Parquet-producing pipeline uses Spark `local[*]` unless a lecturer or administrator confirms a shared storage path.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
jupyter notebook
```

Use a group-specific Kafka topic, for example `bdeng_g1_air_quality_live`. Do not hardcode credentials or use a generic shared topic.

## What Is Not Committed

Generated CSV, JSON, HTML, Parquet, and Spark checkpoint files under `data/` are ignored. `.gitkeep` files preserve the required folder structure. Secrets and local `.env` files are ignored; only safe examples are committed.

`project-resources/` is local course/reference material and is ignored by Git. It may exist on a developer machine for reference, but it is not part of the public repository deliverable.

## Limitations

This is a university project, not a production platform. The dataset may not be truly large, the analysis is exploratory rather than causal, Wikipedia metadata is fragile, and FH cluster storage is not assumed until proven.

## Presentation Notes

Final figures are saved to `presentation/figures/`. The storyline and presentation outline live in `presentation/final_storyline.md` and `presentation/presentation_outline.md`.

## Course Reference Material

The local folder `project-resources/bwi-big-data-engineering-main/` may contain course reference notebooks for pandas file loading, requests/JSON, BeautifulSoup web scraping, Parquet, Spark DataFrames, Kafka producer/consumer examples, and Spark streaming patterns. These files are reference material only, are ignored by Git, and must not be deleted by agents.
