# Cluster Setup

## Assumptions

The FH environment may require VPN, JupyterHub access, a Spark master URL, and a Kafka broker URL. Credentials and private hostnames must not be committed.

## Known Spark Cluster Findings

- Spark master connectivity was tested successfully.
- A basic Spark DataFrame action worked.
- HDFS/shared storage was not confirmed.
- Local Jupyter paths are not automatically shared with cluster executors.

## Decision

Use Spark `local[*]` for reliable Parquet-producing notebook runs. Use the FH Spark cluster only for connectivity and compute smoke tests unless a confirmed shared storage path is provided.
