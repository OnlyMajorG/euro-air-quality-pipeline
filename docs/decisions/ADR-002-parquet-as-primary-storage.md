# ADR-002: Parquet as Primary Storage

## Status
Accepted

## Context
The project requires a performant, interoperable analytics format across Bronze, Silver, and Gold layers.

## Decision
Use Parquet as the primary storage format for pipeline outputs.

## Consequences
Columnar storage improves analytics efficiency and aligns with Spark ecosystem tooling.
