# Current Project Status

Last updated: 2026-05-30

## Status

Current phase: **Phase 3 in progress**

Decision: **Phase 2 complete (PASS); Phase 3 started — Issue 3.1 complete**

## Summary

The repository contains a clean Phase 0 skeleton for a university Big Data
Engineering project. It defines documentation placeholders, ADRs, diagram
placeholders, source package placeholders, placeholder tests, data folder
scaffolding, and a Phase 0 Docker Compose baseline.

No full pipeline implementation exists yet. That is intentional.

## Current Known Issues

| Severity | Issue | Source |
| --- | --- | --- |
| Minor | Docker Compose uses `latest` image tags. | `docs/qa/phase0_qa_report.md` |

## Resolved Issues

| Date | Issue | Evidence |
| --- | --- | --- |
| 2026-05-30 | All seven notebooks were invalid JSON because they contained extra literal text after the closing JSON object. | Notebook JSON validation now passes for all seven notebooks. |
| 2026-05-30 | README lagged behind the active phase after Phase 1 QA and later Phase 2 work. | README now states Phase 2 in progress and lists completed Phase 2 city reference work through Issue 2.7. |
| 2026-05-30 | `pytest` and `pyarrow` were missing from the active local interpreter. | Installed locally and verified `tests/test_city_mapping.py` passes. |

## Completed Phase 1 Work

- Defined Vienna and Berlin as pilot cities.
- Checked Open-Meteo API feasibility.
- Checked EEA metadata availability and station-based risk.
- Checked Wikipedia HTML/infobox feasibility.
- Documented sample data hygiene rules.
- Created the Phase 1 source feasibility matrix.
- Created the Phase 1 QA report.

## Completed Phase 2 Work

- Defined exactly 8 starter cities for the city reference model.
- Designed the canonical city reference schema.
- Reviewed ADR-003 and confirmed that the city reference model decision remains
  unchanged.
- Implemented a deterministic local city reference builder that writes ignored
  CSV and Parquet artifacts only when explicitly called.
- Added city reference integrity tests for schema, join keys, uniqueness,
  country codes, normalized names, coordinates, city count, and Parquet
  readback.
- Documented the EEA station-to-city mapping strategy, including distance,
  pollutant coverage, time coverage, representativeness, fallback behavior, and
  the `city_id` join rule.
- Documented Wikipedia metadata join, null-handling, ambiguity-handling, and
  contextual-only rules.
- Documented Open-Meteo coordinate, pollutant field, UTC timezone, and Phase 5
  handoff rules.
- Updated notebook 01 as the readable Phase 2 city mapping documentation trail,
  including deliverables, schema, source mapping rules, validation checks, and
  a local Parquet readback example.
- Created the Phase 2 QA report and gate decision.

## Completed Phase 3 Work

- Created `agents/soul.md` — the AI agent operating contract for this repository.
- Issue 3.1: Documented EEA batch source access path, raw-data policy, file
  naming convention, git-ignore verification, and reproducibility contract.
- Updated `docs/data_sources.md` with `Phase 3 EEA Source Access` section.
- Updated `notebooks/02_eea_batch_ingestion.ipynb` with Phase 3 scope and
  Issue 3.1 summary.

## Next Allowed Work

Phase 3 issues in order:

- Issue 3.2: Define EEA input schema and Silver output schema.
- Issue 3.3: Prepare EEA station-to-city mapping table.
- Issue 3.4: Implement EEA loader for controlled local files.
- Issue 3.5: Add EEA data quality validation rules.
- Issue 3.6: Build EEA city daily Silver Parquet.
- Issue 3.7: Update notebook 02 with full Phase 3 documentation.
- Issue 3.8: Phase 3 QA report and gate decision.

## Explicitly Not Implemented

- EEA loader or ingestion implementation.
- EEA bulk data download.
- Wikipedia scraping.
- Open-Meteo API client behavior.
- Kafka producer behavior.
- Spark Structured Streaming behavior.
- Silver/Gold transformations beyond city reference.
- Analysis results and final visualizations.
