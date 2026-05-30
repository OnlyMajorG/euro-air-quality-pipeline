# Current Project Status

Last updated: 2026-05-30

## Status

Current phase: **Phase 0 - Repository initialization**

Decision: **Approved for Phase 1 after notebook JSON fixes**

## Summary

The repository contains a clean Phase 0 skeleton for a university Big Data
Engineering project. It defines documentation placeholders, ADRs, diagram
placeholders, source package placeholders, placeholder tests, data folder
scaffolding, and a Phase 0 Docker Compose baseline.

No real pipeline implementation exists yet. That is intentional.

## Current Known Issues

| Severity | Issue | Source |
| --- | --- | --- |
| Major | All seven notebooks are invalid JSON because they contain extra literal text after the closing JSON object. | `docs/qa/phase0_qa_report.md` |
| Minor | `pytest` is listed in requirements but is not installed in the active local interpreter used during QA. | `docs/qa/phase0_qa_report.md` |
| Minor | README BDENG checklist may read as completed capability rather than planned scaffolding. | `docs/qa/phase0_qa_report.md` |
| Minor | Docker Compose uses `latest` image tags. | `docs/qa/phase0_qa_report.md` |

## Next Allowed Work

The next allowed work is still Phase 0 cleanup:

- Fix invalid notebook JSON.
- Prepare the local Python environment and run placeholder tests.
- Clarify README wording around planned versus implemented requirements.

Phase 1 may begin only after the notebook issue is fixed.

## Explicitly Not Implemented

- EEA ingestion.
- Wikipedia scraping.
- Open-Meteo API client behavior.
- Kafka producer behavior.
- Spark Structured Streaming behavior.
- Bronze/Silver/Gold transformations.
- Analysis results and final visualizations.
