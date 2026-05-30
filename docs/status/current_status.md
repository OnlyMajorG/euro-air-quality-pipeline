# Current Project Status

Last updated: 2026-05-30

## Status

Current phase: **Phase 1 complete; Phase 2 may start**

Decision: **Approved for Phase 2**

## Summary

The repository contains a clean Phase 0 skeleton for a university Big Data
Engineering project. It defines documentation placeholders, ADRs, diagram
placeholders, source package placeholders, placeholder tests, data folder
scaffolding, and a Phase 0 Docker Compose baseline.

No full pipeline implementation exists yet. That is intentional.

## Current Known Issues

| Severity | Issue | Source |
| --- | --- | --- |
| Minor | `pytest` is listed in requirements but is not installed in the active local interpreter used during QA. | `docs/qa/phase0_qa_report.md` |
| Minor | Docker Compose uses `latest` image tags. | `docs/qa/phase0_qa_report.md` |
| Minor | `pytest` could not be run during Phase 1 QA because it is not installed in the active interpreter. | `docs/qa/phase1_qa_report.md` |

## Resolved Issues

| Date | Issue | Evidence |
| --- | --- | --- |
| 2026-05-30 | All seven notebooks were invalid JSON because they contained extra literal text after the closing JSON object. | Notebook JSON validation now passes for all seven notebooks. |
| 2026-05-30 | README still described Phase 1 as next work after Phase 1 QA had passed. | README now states Phase 1 complete and Phase 2 ready to start. |

## Completed Phase 1 Work

- Defined Vienna and Berlin as pilot cities.
- Checked Open-Meteo API feasibility.
- Checked EEA metadata availability and station-based risk.
- Checked Wikipedia HTML/infobox feasibility.
- Documented sample data hygiene rules.
- Created the Phase 1 source feasibility matrix.
- Created the Phase 1 QA report.

## Next Allowed Work

The next allowed work is Phase 2 city mapping and reference model:

- Define stable `city_id` values.
- Decide the pilot-to-final city list.
- Document EEA station-to-city mapping rules.
- Carry forward Open-Meteo field mapping.
- Define how Wikipedia metadata joins to cities.

## Explicitly Not Implemented

- EEA ingestion.
- Wikipedia scraping.
- Open-Meteo API client behavior.
- Kafka producer behavior.
- Spark Structured Streaming behavior.
- Bronze/Silver/Gold transformations.
- Analysis results and final visualizations.
