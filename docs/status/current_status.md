# Current Project Status

Last updated: 2026-05-30

## Status

Current phase: **Phase 2 in progress**

Decision: **Phase 2.1 and Phase 2.2 completed; Phase 2 gate not yet reviewed**

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
| 2026-05-30 | README still described Phase 1 as next work after Phase 1 QA had passed. | README now states Phase 1 complete and Phase 2 ready to start. |
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

## Next Allowed Work

The next allowed work remains within Phase 2 city mapping and reference model:

- Document EEA station-to-city mapping rules.
- Carry forward Open-Meteo field mapping.
- Define how Wikipedia metadata joins to cities.
- Extend validation tests as mapping rules become more specific.

## Explicitly Not Implemented

- EEA ingestion.
- Wikipedia scraping.
- Open-Meteo API client behavior.
- Kafka producer behavior.
- Spark Structured Streaming behavior.
- Bronze/Silver/Gold transformations.
- Analysis results and final visualizations.
