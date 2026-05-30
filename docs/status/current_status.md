# Current Project Status

Last updated: 2026-05-30

## Status

Current phase: **Phase 0 cleanup complete; Phase 1 may start**

Decision: **Approved for Phase 1**

## Summary

The repository contains a clean Phase 0 skeleton for a university Big Data
Engineering project. It defines documentation placeholders, ADRs, diagram
placeholders, source package placeholders, placeholder tests, data folder
scaffolding, and a Phase 0 Docker Compose baseline.

No real pipeline implementation exists yet. That is intentional.

## Current Known Issues

| Severity | Issue | Source |
| --- | --- | --- |
| Minor | `pytest` is listed in requirements but is not installed in the active local interpreter used during QA. | `docs/qa/phase0_qa_report.md` |
| Minor | README BDENG checklist may read as completed capability rather than planned scaffolding. | `docs/qa/phase0_qa_report.md` |
| Minor | Docker Compose uses `latest` image tags. | `docs/qa/phase0_qa_report.md` |

## Resolved Issues

| Date | Issue | Evidence |
| --- | --- | --- |
| 2026-05-30 | All seven notebooks were invalid JSON because they contained extra literal text after the closing JSON object. | Notebook JSON validation now passes for all seven notebooks. |

## Next Allowed Work

The next allowed work is Phase 1 source spike and feasibility testing:

- Define two pilot cities and the target pollutant scope.
- Validate Open-Meteo API feasibility for pilot cities.
- Validate EEA data availability for pilot cities.
- Validate Wikipedia HTML feasibility for pilot cities.
- Document risks and a source feasibility matrix.

## Explicitly Not Implemented

- EEA ingestion.
- Wikipedia scraping.
- Open-Meteo API client behavior.
- Kafka producer behavior.
- Spark Structured Streaming behavior.
- Bronze/Silver/Gold transformations.
- Analysis results and final visualizations.
