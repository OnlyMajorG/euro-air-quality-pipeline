# Current Project Status

Last updated: 2026-05-30

## Status

Current phase: **Phase 4 approved, not started**

Decision: **Phase 3 complete after QA follow-up; approved for Phase 4**

## Summary

The repository contains a clean university Big Data Engineering project
skeleton, completed Phase 1 source feasibility documentation, completed Phase 2
city reference work, and completed Phase 3 EEA batch ingestion implementation
with selected EEA station mappings for all 8 starter cities.

The adapted execution strategy is now documented: Spark `local[*]` is the
default for Parquet-producing pipeline runs. The FH Spark cluster is documented
as connectivity and compute evidence only until a confirmed shared storage path
exists.

## Current Known Issues

| Severity | Issue | Source |
| --- | --- | --- |
| Major | FH Spark cluster storage is not confirmed for Parquet outputs. | `docs/qa/cluster_connectivity_check.md`, ADR-004 |
| Minor | Real EEA source files still need local row validation before Gold analysis. | `docs/qa/phase3_qa_report.md` |

## Resolved Issues

| Date | Issue | Evidence |
| --- | --- | --- |
| 2026-05-30 | All seven notebooks were invalid JSON because they contained extra literal text after the closing JSON object. | Notebook JSON validation now passes. |
| 2026-05-30 | README lagged behind the active phase. | README now states the latest approved phase and documents execution modes. |
| 2026-05-30 | `pytest` and `pyarrow` were missing from the active local interpreter. | Installed locally; tests pass. |
| 2026-05-30 | Phase 3 QA major/minor findings required follow-up. | Docker images pinned, all 8 EEA station mappings selected, Phase 4 pre-check added, QA report updated. |

## Completed Phase 1 Work

- Defined Vienna and Berlin as pilot cities.
- Checked Open-Meteo API feasibility.
- Checked EEA metadata availability and station-based risk.
- Checked Wikipedia HTML/infobox feasibility.
- Documented sample data hygiene rules.
- Created the Phase 1 source feasibility matrix.
- Created the Phase 1 QA report.
- Recorded FH Spark cluster connectivity evidence and storage limitation.
- Accepted ADR-004 for execution environment and storage strategy.

## Completed Phase 2 Work

- Defined exactly 8 starter cities for the city reference model.
- Designed the canonical city reference schema.
- Implemented a deterministic local city reference builder.
- Added city reference integrity tests.
- Documented EEA, Wikipedia, and Open-Meteo mapping rules.
- Updated notebook 01 as the Phase 2 documentation trail.
- Created the Phase 2 QA report.

## Completed Phase 3 Work

- Issue 3.1: EEA source access path and raw-data policy documented.
- Issue 3.2: EEA input schema and Silver output schema documented.
- Issue 3.3: EEA station-to-city mapping builder implemented from local constants.
- Issue 3.4: EEA loader for controlled local CSV/Parquet files implemented.
- Issue 3.5: EEA data quality validation rules implemented, tested, and documented.
- Issue 3.6: EEA city daily Silver Parquet writer implemented and tested.
- Issue 3.7: Notebook 02 updated as the readable Phase 3 documentation trail.
- Issue 3.8: Phase 3 QA report created; Phase 4 approved.

## Next Allowed Work

The next allowed work is Phase 4 Wikipedia Web Scraping:

- Implement controlled Wikipedia HTML handling for the 8 starter cities.
- Keep parser behavior side-effect free on import.
- Preserve `city_id` as the join key.
- Do not start Phase 5 Open-Meteo client, Kafka, Spark Structured Streaming,
  Gold tables, dashboards, or final analytics from this gate.

## Explicitly Not Implemented

- Production Wikipedia scraping.
- Open-Meteo API client behavior.
- Kafka producer behavior.
- Spark Structured Streaming behavior.
- Gold transformations or analytics.
- Final visualizations.
- Cluster Spark Parquet persistence.
