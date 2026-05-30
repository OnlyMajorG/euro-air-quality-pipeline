# Current Project Status

Last updated: 2026-05-30

## Status

Current phase: **Phase 2 in progress**

Decision: **Phase 2 in progress through Issue 2.7; Phase 2 gate not yet reviewed**

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

## Next Allowed Work

The next allowed work remains within Phase 2 city mapping and reference model:

- Extend validation tests as EEA, Wikipedia, and Open-Meteo mapping rules
  become more specific.
- Prepare the Phase 2 QA/gate decision after remaining Phase 2 issue work is
  complete.

## Explicitly Not Implemented

- EEA ingestion.
- Wikipedia scraping.
- Open-Meteo API client behavior.
- Kafka producer behavior.
- Spark Structured Streaming behavior.
- Bronze/Silver/Gold transformations.
- Analysis results and final visualizations.
