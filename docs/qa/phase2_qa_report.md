# Phase 2 QA Report

## Executive Summary

Overall status: **PASS**

Phase 2 created a coherent, tested, and documented city reference model. The
city reference builder is deterministic, local-only, side-effect free on import,
and can generate both `data/silver/city_reference.csv` and
`data/silver/city_reference.parquet`. The Parquet file can be read locally and
is stable enough to serve as input for later phases.

Final Decision: **Approved for Phase 3**

## Audit Scope

This audit covers only Phase 2: City Mapping and Reference Model.

The audit verifies that Phase 2 is ready to hand off to later EEA, Wikipedia,
and Open-Meteo implementation phases. It does not implement Phase 3 EEA
ingestion, a production Wikipedia scraper, Open-Meteo client behavior, Kafka,
Spark Structured Streaming, Gold tables, dashboards, or final analytics.

## Checks Performed

Commands and inspections performed:

- Reviewed `docs/data_model.md`.
- Reviewed `docs/decisions/ADR-003-city-reference-model.md`.
- Reviewed `notebooks/01_city_mapping.ipynb`.
- Reviewed `src/city_mapping/build_city_reference.py`.
- Reviewed `tests/test_city_mapping.py`.
- Ran `python -m src.city_mapping.build_city_reference`.
- Ran `python -m pytest`.
- Read back `data/silver/city_reference.csv`.
- Read back `data/silver/city_reference.parquet`.
- Validated notebook JSON and verified notebook output count is zero.
- Ran `docker compose config`.
- Ran `git diff -- src/ingestion src/kafka src/spark_jobs src/analysis`.
- Ran `git check-ignore -v` for generated CSV, Parquet, JSON, and HTML data
  artifacts.
- Searched for scope creep indicators in code, docs, tests, and notebooks.

## Requirement Checklist

| Area | Status | Evidence | Notes |
| ---- | ------ | -------- | ----- |
| P2-AC1: At least 8 cities defined | PASS | `city_reference.parquet` readback returned 8 rows. | Matches Phase 2 starter scope. |
| P2-AC2: Unique `city_id` values | PASS | `tests/test_city_mapping.py`; Parquet readback asserted uniqueness. | `city_id` is the stable join key. |
| P2-AC3: Coordinates present | PASS | `tests/test_city_mapping.py`; Parquet readback validated `latitude` and `longitude`. | Coordinates are WGS84 city reference coordinates. |
| P2-AC4: No null join keys | PASS | `tests/test_city_mapping.py`; Parquet readback checked required join fields. | Required fields are non-null. |
| P2-AC5: EEA mapping strategy documented | PASS | `docs/data_model.md` contains `EEA Station Mapping Strategy`. | Strategy covers distance, pollutant coverage, time coverage, representativeness, and `city_id` joins. |
| P2-AC6: `city_reference.parquet` readable | PASS | Local readback with pandas succeeded. | `city_reference.parquet` is a stable input for following phases. |
| Canonical schema | PASS | `docs/data_model.md`; `tests/test_city_mapping.py`. | Required/optional fields, types, nullability, and constraints are documented and tested. |
| ADR alignment | PASS | `docs/decisions/ADR-003-city-reference-model.md`. | ADR-003 reviewed during Phase 2; decision unchanged. |
| Notebook documentation | PASS | `notebooks/01_city_mapping.ipynb`. | Documents scope, schema, source mapping rules, validation, DoD, and readback. |
| Builder behavior | PASS | `src/city_mapping/build_city_reference.py`. | Deterministic local constants; no external calls; writes only when explicitly called. |
| Generated data hygiene | PASS | `.gitignore`; `git check-ignore -v`. | CSV/Parquet remain ignored local artifacts. |
| Test coverage | PASS | `python -m pytest`: 20 passed. | City mapping tests cover integrity and readback behavior. |
| Scope consistency | PASS | `git diff -- src/ingestion src/kafka src/spark_jobs src/analysis` was empty. | No future-phase implementation added. |

## Findings

### Critical

None.

### Major

None.

### Minor

None for Phase 2 gate readiness.

## Positive Observations

- The `city_id` join-key rule is consistently documented across the data model
  and notebook.
- EEA station mapping risk is handled as an explicit documented strategy before
  ingestion starts.
- Wikipedia metadata is correctly treated as contextual information, not
  official ground truth.
- Open-Meteo coordinate and pollutant field mapping is documented without
  prematurely implementing the client or event schema.
- Tests validate schema integrity, null handling, uniqueness, coordinate
  ranges, country-code format, normalized names, minimum city count, duplicate
  rejection, and CSV/Parquet readback.

## Scope Creep Assessment

Phase 2 remained within scope.

Confirmed not implemented in Phase 2:

- full EEA ingestion,
- production Wikipedia scraper,
- Open-Meteo client implementation,
- Kafka producer,
- Spark Structured Streaming,
- Gold tables,
- dashboard,
- machine learning,
- cloud deployment,
- PostgreSQL, Airflow, or dbt.

The only generated Phase 2 data artifacts are
`data/silver/city_reference.csv` and `data/silver/city_reference.parquet`, both
created by an explicit local builder command and ignored by Git.

## Data Engineering Readiness Assessment

Phase 2 is ready for Phase 3.

`city_reference.parquet` is a stable input for following phases because it:

- contains the agreed 8 starter cities,
- uses stable unique `city_id` values,
- contains non-null required join keys,
- contains fixed WGS84 city coordinates,
- documents source-specific mapping assumptions,
- can be regenerated deterministically,
- can be read back locally as Parquet,
- is protected by regression tests.

Phase 3 may begin as EEA Batch Ingestion only. Phase 3 should use the existing
`city_id` model and must not bypass the documented station-to-city mapping
strategy.

## Recommended Fixes

No blocking or required fixes before Phase 3.

Recommended follow-up tasks for Phase 3:

- Create a small, controlled EEA metadata/sample inspection workflow before any
  bulk data handling.
- Keep EEA raw data ignored or reproducibly referenced according to the data
  policy.
- Use `city_id` as the only downstream city join key.
- Record station selection decisions against the documented mapping fields.
- Keep Phase 3 separate from Wikipedia scraping, Open-Meteo client work, Kafka,
  Spark streaming, and Gold analytics.

## Final Decision

**Approved for Phase 3**

Phase 3 may start as EEA Batch Ingestion work. Phase 3 must not implement
Wikipedia scraping, Open-Meteo client behavior, Kafka producer logic, Spark
Structured Streaming, Gold tables, dashboards, or final analytics unless a
later phase or issue explicitly authorizes that work.
