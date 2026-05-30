# ADR-004: Execution Environment And Storage Strategy

## Status
Accepted

## Context
FH/BDENG cluster smoke tests showed that the Spark master
`spark://172.29.16.102:7077` is reachable and can run basic Spark DataFrame
actions. The same tests showed that HDFS is not configured in the tested
environment and that local Jupyter project paths are not reliable shared
storage between Spark driver/Jupyter and Spark executors.

A Spark cluster write to a relative project path under `data/` did not produce
a complete visible Parquet dataset in the Jupyter file system. Treating that
mode as the primary persistence strategy would create false reproducibility
claims.

## Decision
Use Spark `local[*]` as the default execution mode for Parquet-producing
pipeline runs in the project/Jupyter environment.

Use the FH Spark cluster as documented connectivity and compute evidence only,
unless the lecturer/admin provides a confirmed shared storage path.

Use the FH Kafka broker as the preferred Kafka broker for later Kafka phases
when available, with a group-specific topic:

```text
bdeng_g1_air_quality_live
```

Do not claim HDFS or cluster end-to-end Parquet persistence unless shared
storage has been explicitly confirmed and tested.

## Consequences
The project remains reproducible and reviewable because Parquet outputs are
written to the project `data/` folder from a reliable local/Jupyter execution
mode.

The FH Spark cluster remains visible in the project as infrastructure evidence,
but it is not used for final Parquet persistence unless a real shared storage
path becomes available.

Kafka and Spark remain core project requirements. This ADR changes the
execution strategy for reliability; it does not remove Kafka, Spark Structured
Streaming, Parquet, Bronze/Silver/Gold, or city mapping from the core scope.
