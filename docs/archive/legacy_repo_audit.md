# Legacy Repository Audit

## Scope

This audit records the pre-refactor repository state before the notebook-only structure was finalized.

## Existing Implementation Surface

The repository previously contained:

- `src/` package modules for city reference, station mapping, EEA loading, Kafka placeholders, Spark job placeholders and shared utilities.
- `tests/` with pytest-based validation for city mapping and EEA loading.
- Earlier phase notebooks with old names.
- Phase-oriented documentation under `docs/status/`, `docs/implementation/` and older ADR names.

## Useful Logic Preserved

| Legacy source | Preserved in |
| --- | --- |
| city reference constants and validation | `notebooks/02_city_reference_model.ipynb` |
| EEA station mapping | `notebooks/03_eea_batch_ingestion.ipynb` |
| EEA row normalization, data quality and daily aggregation | `notebooks/03_eea_batch_ingestion.ipynb` |
| city/EEA validation test intent | validation sections in notebooks `02` and `03` |
| placeholder source modules | replaced by notebook implementations or templates in notebooks `04` to `08` |

## Removal Decision

`src/` and `tests/` were removed only after the useful logic was migrated or documented. This keeps the repository aligned with the course requirement that implementation steps are documented in Jupyter notebooks.

## Protected Area

`project-resources/` is course/reference material, is ignored by Git, and must not be deleted by AI agents.
