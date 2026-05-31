# Phase 5 Open-Meteo API And Kafka Producer Check

## Executive Summary

Overall status: IMPLEMENTED, LOCAL MOCK PASS, FH KAFKA EVIDENCE RUN REQUIRED

Notebook `05_open_meteo_api_and_kafka_producer.ipynb` is implemented and reproducibly executable. It loads the city reference, requests Open-Meteo air-quality payloads, stores Bronze JSON, creates a provenance-labeled JSONL event batch, validates the flat event schema, publishes events and proves delivery with a bounded consumer smoke test.

The local environment validates the mock-broker path. The strict FH Kafka evidence run must be executed inside FH JupyterHub because the private broker is not reachable from this workstation.

## Scope Decision

The proposed MongoDB/Vienna-only Spark analytics epic was not applied. The repository has no `vienna_hourly_joined` collection, no weather dataset, and no Docker Compose stack. Introducing those assumptions would conflict with the frozen European EEA/Wikipedia/Open-Meteo/Kafka/Spark scope and would skip the required Kafka producer dependency.

Spark reads from Kafka in Phase 6.

## Checks Performed

| Check | Result | Evidence |
| --- | --- | --- |
| Phase 0 to 5 dependency chain | PASS | notebooks `00` to `05` execute in order |
| Full local notebook smoke run | PASS | notebooks `00` to `08` execute with local Bronze readback and external producers disabled |
| City reference input | PASS | 8 unique cities |
| Open-Meteo API attempt | PARTIAL | 7 city Bronze payloads were fetched successfully; Prague used controlled fallback after a transient TLS reset |
| Local Bronze JSON | PASS | one JSON payload per city under `data/bronze/open_meteo_raw/` |
| Ingestion manifest | PASS | `open_meteo_ingestion_manifest.json` records per-city provenance |
| JSONL event output | PASS | 8 events by default, latest hour per city |
| Stable event IDs | PASS | all 8 default-run `event_id` values are unique |
| Event schema | PASS | flat schema includes `data_status` for downstream filtering |
| Kafka producer implementation | PASS | guarded `kafka-python` producer sends keyed JSON events and waits for delivery futures |
| Kafka consumer implementation | PASS | bounded consumer uses unique group, timeout, maximum messages and schema validation |
| Local mock producer/consumer | PASS | JSONL mock broker sent and consumed 8 events |
| FH Kafka broker-backed delivery | REQUIRES JUPYTERHUB RUN | run strict mode against the private broker configured in the non-versioned JupyterHub `.env` |
| Phase 6 local PySpark execution | BLOCKED EXTERNALLY | `pyspark` is listed in `requirements.txt` but is not installed in the active Python environment |

## Event Contract

```text
event_id
schema_version
source
city_id
event_time_utc
ingestion_time_utc
data_status
pm2_5
pm10
no2
```

## Current Local Event Provenance

| Status | Events | Meaning |
| --- | ---: | --- |
| `loaded_local_bronze` | 7 | Locally preserved Bronze payload originally fetched from Open-Meteo |
| `controlled_offline_fallback` | 1 | Mechanics-only fallback for Prague; exclude from analytical claims |

## Required External Evidence Run

Before claiming Phase 5 Kafka completion:

1. Install dependencies with `python -m pip install -r requirements.txt`.
2. Keep the FH-provided broker and group topic in `.env`.
3. Set `KAFKA_MODE=kafka`.
4. Set `ALLOW_KAFKA_MOCK_FALLBACK=false`.
5. Set `ALLOW_CONTROLLED_OPEN_METEO_FALLBACK=false`.
6. Set `RUN_OPEN_METEO_API_FETCH=true`.
7. Set `RUN_OPEN_METEO_KAFKA_PRODUCER=true`.
8. Run notebook `05` and verify `broker.mode == "kafka"`, `sent > 0`, `delivery_errors == 0`, and `consumed >= 1`.
9. Verify that all city statuses are `fetched_api`.
10. Use the Phase-6 Spark Kafka read to prove broker delivery end to end.

## Final Decision

Phase 5 implementation and local mock execution are complete. The strict FH Kafka evidence run remains required before marking the external Kafka acceptance criteria complete. Phase 6 may be implemented against the documented event contract.

## Local Fallback Validation

The auto mode was tested locally with FH-shaped configuration values while `kafka-python` was intentionally unavailable. The notebook fell back to the mock broker, sent 8 latest-hour events and consumed all 8 events. The result exposed the fallback reason instead of claiming Kafka delivery.

Strict `KAFKA_MODE=kafka` was also tested locally with mock fallback disabled. The notebook failed closed with the visible missing-`kafka-python` error, proving that strict FH evidence mode cannot silently degrade to mock delivery.
