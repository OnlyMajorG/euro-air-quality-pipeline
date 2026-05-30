# Current Project Status

Last updated: 2026-05-30

## Status

Current phase: **Phase 3 in progress**

Decision: **Phase 2 complete (PASS); Phase 3 active through Issue 3.4**

## Summary

The repository contains a clean university Big Data Engineering project
skeleton, completed Phase 1 source feasibility documentation, completed Phase 2
city reference work, and early Phase 3 EEA batch ingestion implementation.

The adapted execution strategy is now documented: Spark `local[*]` is the
default for Parquet-producing pipeline runs. The FH Spark cluster is documented
as connectivity and compute evidence only until a confirmed shared storage path
exists.

## Current Known Issues

| Severity | Issue | Source |
| --- | --- | --- |
| Minor | Docker Compose uses `latest` image tags. | `docs/qa/phase0_qa_report.md` |
| Major | FH Spark cluster storage is not confirmed for Parquet outputs. | `docs/qa/cluster_connectivity_check.md`, ADR-004 |
| Major | Placeholder station mappings remain for Paris, Madrid, Rome, Amsterdam, Warsaw, and Prague. | `src/city_mapping/build_station_mapping.py` |

## Resolved Issues

| Date | Issue | Evidence |
| --- | --- | --- |
| 2026-05-30 | All seven notebooks were invalid JSON because they contained extra literal text after the closing JSON object. | Notebook JSON validation now passes. |
| 2026-05-30 | README lagged behind the active phase. | README now states Phase 3 in progress and documents execution modes. |
| 2026-05-30 | `pytest` and `pyarrow` were missing from the active local interpreter. | Installed locally; tests pass. |

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

## Next Allowed Work

The next allowed work remains Phase 3 EEA Batch Ingestion:

- Resolve placeholder station mappings before real ingestion.
- Complete Issue 3.5 data quality documentation and validation policy.
- Complete Issue 3.6 reproducible EEA city daily Silver Parquet output.
- Complete Issue 3.7 notebook 02 final documentation.
- Complete Issue 3.8 Phase 3 QA report and gate decision.

## Explicitly Not Implemented

- Production Wikipedia scraping.
- Open-Meteo API client behavior.
- Kafka producer behavior.
- Spark Structured Streaming behavior.
- Gold transformations or analytics.
- Final visualizations.
- Cluster Spark Parquet persistence.
