# Legacy Source and Test Migration Notes

The repository previously used `src/` modules and `tests/` as the implementation and QA layer. The course-required structure is now notebook-only, so useful logic was migrated before removal.

## Migrated Logic

| Legacy area | Migrated to | Notes |
| --- | --- | --- |
| `src/city_mapping/build_city_reference.py` | `notebooks/02_city_reference_model.ipynb` | City constants, validation rules, CSV/Parquet writer |
| `src/city_mapping/build_station_mapping.py` | `notebooks/03_eea_batch_ingestion.ipynb` | Selected EEA station mapping and station validation basis |
| `src/ingestion/eea_loader.py` | `notebooks/03_eea_batch_ingestion.ipynb` | Local file loading, pollutant normalization, data quality, daily aggregation |
| Placeholder Open-Meteo, Kafka, Spark, Wikipedia, Gold modules | notebooks `04` through `08` | Replaced by notebook implementation templates |
| `tests/test_city_mapping.py` and `tests/test_eea_loader.py` | notebook validation sections | Validation concepts are kept as notebook checks |

## Removed Folders

`src/` and `tests/` were removed after migration so the repository clearly presents notebooks as the main deliverable.

## Non-Deleted Area

`project-resources/` is intentionally preserved locally, ignored by Git, and must not be deleted by agents.
