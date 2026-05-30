# Cluster Connectivity Check

## Summary

Known findings:

- Spark master reachable.
- Basic DataFrame action works.
- HDFS/shared storage not available or not confirmed.
- Local Jupyter path is not shared with cluster executors.

## Decision

Use Spark `local[*]` for reliable Parquet-producing pipeline notebooks. Use FH cluster mode only for connectivity and compute smoke tests unless shared storage is confirmed.
