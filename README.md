# euro-air-quality-pipeline

## Executive summary
This repository initializes a reproducible Big Data Engineering project focused on European air quality. It defines the Phase 0 structure, documentation, and placeholders needed to implement a multi-source pipeline in later phases.

## Research question
> Which air quality patterns can be identified across selected European cities when historical air quality data, current API data and urban context metadata are combined in a reproducible Big Data Engineering pipeline?

## Core scope
- Initialize a clean, reproducible repository for a university Big Data Engineering project.
- Prepare structure for three data sources: EEA files, Wikipedia scraping, Open-Meteo API.
- Prepare placeholders for Kafka-centric streaming with Spark Structured Streaming.
- Define Bronze/Silver/Gold storage design using Parquet.
- Provide notebook and presentation scaffolding for documentation and storytelling.

## Non-goals / out of scope
- Full pipeline implementation.
- Kafka producer implementation.
- Spark job implementation.
- Real dataset downloads.
- PostgreSQL, dashboards, Airflow, dbt, cloud deployment, CI/CD, and additional infrastructure.

## Data sources
| Source | Type | Planned use |
|---|---|---|
| EEA historical air quality data | File/batch source | Historical baseline ingestion |
| Wikipedia city pages | Web scraping source | City metadata enrichment |
| Open-Meteo Air Quality API | REST API source | Near-real-time air quality events |

## Technology stack
| Technology | Purpose |
|---|---|
| Python | Core implementation language |
| Pandas | Batch transformations and analysis |
| BeautifulSoup | Wikipedia parsing/scraping |
| Kafka | Streaming event broker |
| Spark Structured Streaming | Stream processing from Kafka |
| Parquet | Primary analytics storage format |
| Jupyter Notebooks | Documentation, exploration, and demos |
| Docker Compose | Local multi-service baseline orchestration |

## Planned architecture
The planned pipeline combines batch and API sources into a common layered lakehouse pattern:
1. Ingest EEA files (batch), Wikipedia metadata (scraping), and Open-Meteo API data (REST).
2. Publish Open-Meteo events to Kafka.
3. Process streams/batches into Parquet Bronze, then curated Silver, then analytics-ready Gold.
4. Use notebooks for analysis, validation, and storytelling.

See `docs/architecture.md` and `docs/diagrams/architecture.mmd` for placeholders.

## Bronze / Silver / Gold data layers
- **Bronze**: raw, minimally transformed data, source-aligned.
- **Silver**: cleaned, standardized, and join-ready datasets.
- **Gold**: analytics-focused, business-question-ready tables.

## Repository structure
- `docs/`: architecture, data model, source documentation, ADRs, diagrams.
- `notebooks/`: ordered project notebooks from scope to visualization.
- `src/`: Python modules for config, ingestion, mapping, Kafka, Spark, and analysis.
- `tests/`: placeholder tests for key pipeline domains.
- `data/`: Bronze/Silver/Gold/checkpoints folder scaffolding.
- `presentation/`: final storyline and figures.

## Planned notebook order
1. `00_project_scope_and_sources.ipynb`
2. `01_city_mapping.ipynb`
3. `02_eea_batch_ingestion.ipynb`
4. `03_wikipedia_scraping.ipynb`
5. `04_kafka_producer_demo.ipynb`
6. `05_spark_streaming_processing.ipynb`
7. `06_analysis_and_visualization.ipynb`

## BDENG requirement mapping checklist
- [x] At least 3 different data sources
- [x] One file or database source
- [x] One web scraping source
- [x] One REST API source
- [x] Kafka producer and topic (planned structure)
- [x] Spark reads from Kafka (planned structure)
- [x] ETL/ELT result storage (Bronze/Silver/Gold Parquet structure)
- [x] Data flow visualization
- [x] Jupyter documentation
- [x] Final storytelling and visualization

## Setup (Phase 0 placeholders)
```bash
git clone <repo-url>
cd euro-air-quality-pipeline
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
```

## Current project status
**Phase 0 - Repository initialization**

## Limitations and assumptions
- Files currently provide structure and placeholders, not production logic.
- Service definitions are intentionally minimal and not production-ready.
- Data schemas and transformations will be finalized in later phases.

## License
License to be defined (`LICENSE` file placeholder planned).
