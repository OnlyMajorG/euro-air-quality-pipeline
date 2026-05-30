# Phase Gate Register

## Phase 0 - Repository Initialization

| Item | Status | Evidence |
| --- | --- | --- |
| Repository skeleton exists | Done | README, docs, notebooks, src, tests, data, presentation folders exist. |
| Scope documented | Done | README and ADR-001. |
| Storage direction documented | Done | ADR-002 and data folder scaffold. |
| City reference need documented | Done | ADR-003. |
| QA report exists | Done | `docs/qa/phase0_qa_report.md`. |
| Notebooks structurally valid | Done | All seven notebooks pass `json.loads` validation. |

Phase 0 gate decision: **Approved for Phase 1**.

## Phase 1 - Data Source Spike And Feasibility Testing

Status: **Done**

Gate decision: **Approved for Phase 2**

| Item | Status | Evidence |
| --- | --- | --- |
| Pilot cities defined | Done | `docs/data_sources.md` and notebook 00. |
| Target pollutants defined | Done | PM2.5, PM10, NO2 in `docs/data_sources.md`. |
| Open-Meteo feasibility checked | Done | Open-Meteo section and ignored JSON samples. |
| EEA feasibility checked | Done | EEA section with station metadata findings. |
| Wikipedia feasibility checked | Done | Wikipedia section and ignored HTML samples. |
| Sample data hygiene documented | Done | `Phase 1 Sample Data Hygiene Policy`. |
| Source feasibility matrix created | Done | `Phase 1 Source Feasibility Matrix`. |
| Phase 1 QA report exists | Done | `docs/qa/phase1_qa_report.md`. |
| FH Spark cluster connectivity documented | Done | `docs/qa/cluster_connectivity_check.md`. |
| Execution/storage strategy accepted | Done | `docs/decisions/ADR-004-execution-environment-and-storage-strategy.md`. |

## Phase 2 - City Mapping And Reference Model

Status: **Done**

Gate decision: **Approved for Phase 3**

| Item | Status | Evidence |
| --- | --- | --- |
| Starter city scope defined | Done | `docs/data_model.md` and notebook 01 document exactly 8 starter cities. |
| Canonical city reference schema designed | Done | `docs/data_model.md` documents fields, types, nullability, identifier rules, and validation constraints. |
| ADR-003 reviewed | Done | `docs/decisions/ADR-003-city-reference-model.md` confirms the decision remains unchanged. |
| Deterministic city reference builder | Done | `src/city_mapping/build_city_reference.py` builds local records and writes ignored CSV/Parquet only when explicitly called. |
| Station-to-city mapping rules | Done | `docs/data_model.md` and notebook 01 document EEA candidate selection, required mapping fields, fallback behavior, and `city_id` join rules. |
| Wikipedia metadata join rules | Done | `docs/data_model.md` and notebook 01 document planned fields, null handling, ambiguity handling, contextual-only status, and `city_id` joins. |
| Open-Meteo coordinate and field mapping rules | Done | `docs/data_model.md` and notebook 01 document coordinate usage, PM2.5/PM10/NO2 field mapping, UTC assumption, and Phase 5 handoff. |
| City reference validation tests | Done | `tests/test_city_mapping.py` validates schema, join keys, identifiers, country codes, normalized names, coordinates, duplicate rejection, minimum city count, and CSV/Parquet write/read. |
| Notebook 01 Phase 2 documentation | Done | `notebooks/01_city_mapping.ipynb` documents city scope, schema, source mapping rules, validation, DoD, and local readback. |
| Phase 2 QA report exists | Done | `docs/qa/phase2_qa_report.md`. |

Phase 3 allowed focus:

- EEA batch ingestion planning and implementation.
- Controlled EEA sample or metadata inspection.
- EEA schema and timestamp/unit validation.
- Joining EEA outputs through `city_id`.

Not allowed yet:

- Full EEA ingestion.
- Production Wikipedia scraping.
- Kafka producer implementation.
- Spark Structured Streaming implementation.
- Gold-layer analytics.

## Phase 3 - EEA Batch Ingestion

Status: **In progress**

| Item | Status | Evidence |
| --- | --- | --- |
| EEA source access path documented | Done | `docs/data_sources.md` contains `Phase 3 EEA Source Access` section. |
| Raw-data policy defined | Done | `docs/data_sources.md` documents that large raw EEA files must not be committed; `data/bronze/eea/` is git-ignored. |
| File naming convention documented | Done | Pattern `eea_<station_id>_<pollutant_key>_<year_start>_<year_end>.<ext>` documented in `docs/data_sources.md` and notebook 02. |
| Git-ignore verification confirmed | Done | `git check-ignore -v data/bronze/eea/sample_test.csv` returns the `.gitignore` rule as expected. |
| Notebook 02 updated | Done | `notebooks/02_eea_batch_ingestion.ipynb` contains Phase 3 scope and Issues 3.1-3.6 summaries with 0 code outputs. |
| EEA input schema defined | Done | `docs/data_model.md` contains `Phase 3 EEA Batch Ingestion Data Model`. |
| Station-to-city mapping table | Done with constraints | `src/city_mapping/build_station_mapping.py`; placeholders remain for six non-pilot cities. |
| EEA loader implementation | Done | `src/ingestion/eea_loader.py` reads controlled local CSV/Parquet files and has pytest coverage. |
| Data quality validation | Done | `src/ingestion/eea_loader.py` exposes `validate_eea_rows`; `tests/test_eea_loader.py`, `docs/data_sources.md`, and notebook 02 document and verify behavior. |
| Silver Parquet output | Done | `write_eea_city_daily_parquet()` and `build_eea_city_daily_parquet()` write/read local ignored Parquet output with pytest coverage. |
| Notebook 02 complete | Pending | Issue 3.7 |
| Phase 3 QA report | Pending | Issue 3.8 |

Allowed focus:

- Document EEA source access policy and schema contracts.
- Implement EEA loader for controlled local files.
- Build city/day/pollutant Silver Parquet from EEA data.
- Keep historical EEA data strictly separated from Open-Meteo live data.

Not allowed yet:

- Wikipedia production scraping.
- Open-Meteo API client implementation.
- Kafka producer implementation.
- Spark Structured Streaming.
- Gold-layer analytics.
- Cluster Spark Parquet persistence unless shared storage is confirmed.
