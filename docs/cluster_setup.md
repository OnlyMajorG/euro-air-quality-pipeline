# Cluster Setup And Execution Modes

## Purpose

This document records the adapted execution strategy after FH/BDENG cluster
smoke tests. The core project scope is unchanged: Kafka, Spark Structured
Streaming, Parquet, Bronze/Silver/Gold, and Jupyter documentation remain part
of the project.

The change is only about where Parquet-producing pipeline runs are executed.

## Execution Modes

| Mode | Purpose | Spark master | Storage | Status |
| --- | --- | --- | --- | --- |
| `local_project` | Default for reproducible pipeline runs and Parquet outputs. | `local[*]` | `data/` in this project | Required standard |
| `fh_cluster_connectivity` | FH Spark cluster connectivity and compute evidence. | `spark://172.29.16.102:7077` | No final project storage | Documented evidence only |
| `fh_cluster_shared_storage` | Optional cluster end-to-end mode. | FH Spark master | Confirmed shared storage path | Only if provided and tested |

## Current Decision

Spark `local[*]` is the default for Parquet-producing pipeline runs.

The FH Spark cluster was tested successfully for connectivity and basic
compute, but HDFS was not available and no reliable shared storage path was
confirmed. Therefore, cluster-based Parquet writes to local project paths must
not be treated as final project storage.

## Configuration

Use `.env.example` for the standard local project mode:

```env
EXECUTION_ENV=local_project
SPARK_MASTER_URL=local[*]
KAFKA_BOOTSTRAP_SERVERS=172.29.16.101:9092
KAFKA_TOPIC_AIR_QUALITY_LIVE=bdeng_g1_air_quality_live
DATA_DIR=data
CHECKPOINT_DIR=data/checkpoints
```

Use `.env.cluster.example` only if a confirmed shared storage path is provided:

```env
EXECUTION_ENV=fh_cluster_shared_storage
SPARK_MASTER_URL=spark://172.29.16.102:7077
DATA_DIR=<confirmed_shared_storage_path>/euro-air-quality-pipeline/data
CHECKPOINT_DIR=<confirmed_shared_storage_path>/euro-air-quality-pipeline/checkpoints
```

## Rules

- Do not use HDFS paths unless HDFS is explicitly available.
- Do not claim that Spark cluster writes to `data/` are reliable unless a
  shared storage test proves it.
- Do not use local `file://` cluster executor outputs as final project storage.
- Do not remove Kafka or Spark from the core scope because of cluster storage
  limitations.
- Prefer FH Kafka for later Kafka phases, but keep local Kafka as fallback.
- Use group-specific Kafka topics, not generic topic names.
