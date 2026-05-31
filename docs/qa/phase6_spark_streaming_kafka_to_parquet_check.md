# Phase 6 Spark Streaming Kafka to Parquet Check

## Scope

Notebook `06_spark_structured_streaming_kafka_to_parquet.ipynb` implements the Spark processing handoff after the Phase-5 Open-Meteo producer.

## Execution Modes

| Mode | Purpose | Requirement evidence |
| --- | --- | --- |
| `SPARK_KAFKA_MODE=kafka` | Strict FH JupyterHub run with reachable Kafka and Spark Kafka connector | Required final evidence |
| `SPARK_KAFKA_MODE=auto` | Prefer Kafka, allow explicit local fallback | Development and diagnosis |
| `SPARK_KAFKA_MODE=mock` | Spark Structured Streaming file source based on Phase-5 JSONL | Local functional verification only |

## Implemented Checks

- SparkSession uses `SPARK_MASTER_URL`.
- Kafka broker, topic and mode are loaded from `.env`.
- Real mode uses `spark.readStream.format("kafka")`.
- Mock mode uses Spark `readStream.text()` and the same downstream transformations.
- JSON is parsed with an explicit `StructType`.
- Required fields, event schema, timestamps and pollutant ranges are validated.
- Invalid JSON, invalid events and unknown cities are routed to reject output.
- Valid events are deduplicated by deterministic `event_id`.
- Static city reference and Wikipedia metadata are joined by `city_id`.
- Bronze, Silver and reject Parquet outputs use separate checkpoints.
- Silver Parquet is read back and validated.
- A latest live snapshot is written with at most one row per city.
- No output may be written below `notebooks/data/`.

## Local Verification

Run notebooks `02` through `06` in order. A successful offline run reports:

```text
selected_source_mode: mock
local_spark_streaming_fallback_tested: True
```

This verifies local Spark functionality but does not satisfy the course requirement that Spark reads Kafka.

## FH Evidence Run

Configure the non-versioned `.env` on JupyterHub:

```env
SPARK_KAFKA_MODE=kafka
ALLOW_SPARK_KAFKA_MOCK_FALLBACK=false
RUN_OPEN_METEO_KAFKA_PRODUCER=true
KAFKA_MODE=kafka
ALLOW_KAFKA_MOCK_FALLBACK=false
```

Run notebook `05`, then notebook `06`. The accepted Phase-6 evidence is:

```text
selected_source_mode: kafka
spark_read_kafka_requirement_proven: True
```

If JupyterHub does not preinstall the Spark Kafka connector, set `SPARK_KAFKA_CONNECTOR_PACKAGE` to the package version matching its Spark and Scala runtime.

## Verification Performed on the Development Machine

The following checks were executed on May 31, 2026:

| Check | Result |
| --- | --- |
| All notebook `06` code cells parse as Python | Passed |
| Real Kafka source code uses `readStream.format("kafka")` | Passed |
| Mock source code uses Spark `readStream.text()` | Passed |
| Explicit schema, parsing, validation, deduplication, joins, checkpointing, Parquet read-back and latest snapshot contracts exist | Passed |
| Spark local compute smoke test with JDK 17: `spark.range(3).count()` | Passed, result `3` |
| Kafka broker TCP connectivity: `172.29.16.101:9092` | Reachable |
| Spark master TCP connectivity: `172.29.16.102:7077` | Reachable |
| Native Windows local file-stream and Parquet end-to-end run | Blocked by missing `HADOOP_HOME` Windows binaries (`winutils.exe` and `hadoop.dll`) |
| Strict FH Kafka-to-Spark evidence run | Must be executed on FH JupyterHub with its non-versioned `.env` |

The Windows limitation is environmental rather than a mock-path substitution. The strict acceptance criterion remains a successful JupyterHub execution with `selected_source_mode=kafka`.
