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

## Phase 2 - City Mapping And Reference Model

Status: **In progress**

| Item | Status | Evidence |
| --- | --- | --- |
| Starter city scope defined | Done | `docs/data_model.md` and notebook 01 document exactly 8 starter cities. |
| Canonical city reference schema designed | Done | `docs/data_model.md` documents fields, types, nullability, identifier rules, and validation constraints. |
| ADR-003 reviewed | Done | `docs/decisions/ADR-003-city-reference-model.md` confirms the decision remains unchanged. |
| Deterministic city reference builder | Done | `src/city_mapping/build_city_reference.py` builds local records and writes ignored CSV/Parquet only when explicitly called. |
| Station-to-city mapping rules | Pending | Planned Phase 2 work. |
| Source-specific city mapping rules | Pending | Planned Phase 2 work. |
| City reference validation tests | Done | `tests/test_city_mapping.py` validates schema, join keys, identifiers, country codes, normalized names, coordinates, duplicate rejection, minimum city count, and CSV/Parquet write/read. |

Allowed focus:

- Define stable city identifiers.
- Build the city reference model.
- Document station-to-city mapping rules.
- Add validation tests for city mapping.

Not allowed yet:

- Full EEA ingestion.
- Production Wikipedia scraping.
- Kafka producer implementation.
- Spark Structured Streaming implementation.
- Gold-layer analytics.
