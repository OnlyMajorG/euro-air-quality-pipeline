# ADR-004: Execution Environment and Storage Strategy

## Status

Accepted

## Context

The FH Spark cluster was reachable and could execute basic compute, but shared storage was not confirmed.

## Decision

Use `local_project` with `SPARK_MASTER_URL=local[*]` for reliable Parquet-producing pipeline notebooks. Use the FH Spark cluster for connectivity and compute smoke tests only. Use `fh_cluster_shared_storage` only if a real shared path is confirmed.

## Consequences

The repository must not claim cluster Spark writes Parquet into the local project `data/` folder unless this is proven.
