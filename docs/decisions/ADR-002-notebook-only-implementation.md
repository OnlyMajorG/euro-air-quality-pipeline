# ADR-002: Notebook-Only Implementation

## Status

Accepted

## Context

The course requires each implementation step to be documented in Jupyter notebooks and the public GitHub repository is expected to share the notebooks.

## Decision

All implementation logic will live in ordered notebooks. `src/` and `tests/` are not used as the primary implementation or QA layer. Useful legacy logic was migrated into the notebooks and documented in `docs/archive/legacy_src_notes.md`.

## Consequences

The notebooks are the main executable deliverable. Validation code appears inside notebooks and QA Markdown files rather than in a separate production test suite.
