# Cluster Connectivity Check

## Executive Summary

Status: **PASS WITH STORAGE LIMITATION**

FH Spark cluster connectivity and basic Spark compute were verified outside the
core pipeline implementation path. HDFS/shared storage for reliable Parquet
outputs was not verified. The project therefore uses Spark `local[*]` as the
default mode for Parquet-producing pipeline runs.

## Checks Recorded

### Spark Cluster Connectivity

Observed Spark configuration:

```text
Spark Version: 3.5.6
Spark Master: spark://172.29.16.102:7077
Application ID: app-20260530121540-0015
Default Parallelism: 2
Spark UI: http://172.29.16.104:4040
```

Result:

```text
Spark Cluster Connectivity: PASS
Basic Spark Compute: PASS
```

### HDFS Availability

Observed Hadoop filesystem configuration:

```text
fs.defaultFS = file:///
fs.default.name = file:///
hdfs: not found
```

Result:

```text
HDFS Availability: FAIL / not configured
```

### Cluster Parquet Write To Project Path

A Spark cluster write to:

```text
data/silver/_spark_smoke_test_parquet
```

created visible success marker files but did not create a complete readable
Parquet dataset in the Jupyter project file system. Reading the path failed
because no schema could be inferred.

Result:

```text
Spark Cluster -> local Jupyter Parquet path: FAIL
```

## Decision

Use Spark `local[*]` for Parquet-producing pipeline runs.

Use FH Spark cluster only as connectivity/compute evidence unless a confirmed
shared storage path is provided and tested.

Use FH Kafka broker preferentially in later Kafka phases with group-specific
topic naming:

```text
bdeng_g1_air_quality_live
```

## Scope Impact

No core requirement is removed. Kafka, Spark Structured Streaming, Parquet,
Bronze/Silver/Gold, city mapping, notebooks, and final storytelling remain in
scope.

This check only prevents false claims about cluster-based Parquet persistence.
