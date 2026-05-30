# ADR-003: Parquet Bronze/Silver/Gold Storage

## Status

Accepted

## Context

The project needs a reproducible flat-file storage layout for raw, normalized, and analysis-ready datasets.

## Decision

Use Parquet as the primary transformed-data format and organize outputs into Bronze, Silver, and Gold layers under `data/`.

## Consequences

Generated data remains local and ignored by Git. Bronze stores source-shaped evidence, Silver stores normalized joinable datasets, and Gold stores analysis-ready outputs.
