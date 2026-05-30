# Data Model

## Phase 2 City Reference Scope

Phase 2 defines the controlled starter city list for the city reference model.
This is city-reference work only. It does not implement EEA ingestion,
Wikipedia scraping, Open-Meteo API calls, Kafka, Spark, Gold tables, or final
analytics.

The list starts with exactly 8 European cities. Vienna and Berlin are included
because they were the Phase 1 pilot cities and all three planned source
categories were feasible for them.

| city_id_candidate | city_name | country_code | latitude | longitude | selection_rationale |
| --- | --- | --- | ---: | ---: | --- |
| vienna_at | Vienna | AT | 48.2082 | 16.3738 | Phase 1 pilot city; Open-Meteo, EEA metadata, and Wikipedia feasibility confirmed. |
| berlin_de | Berlin | DE | 52.5200 | 13.4050 | Phase 1 pilot city; Open-Meteo, EEA metadata, and Wikipedia feasibility confirmed. |
| paris_fr | Paris | FR | 48.8566 | 2.3522 | Major European capital with expected air-quality monitoring and rich city metadata. |
| madrid_es | Madrid | ES | 40.4168 | -3.7038 | Major European capital; useful southern European comparison city. |
| rome_it | Rome | IT | 41.9028 | 12.4964 | Major European capital; useful Mediterranean comparison city. |
| amsterdam_nl | Amsterdam | NL | 52.3676 | 4.9041 | Major European city with expected monitoring coverage and compact urban context. |
| warsaw_pl | Warsaw | PL | 52.2297 | 21.0122 | Major Central/Eastern European capital for regional diversity. |
| prague_cz | Prague | CZ | 50.0755 | 14.4378 | Central European capital with expected source coverage and manageable scope. |

## Canonical City Reference Schema

The city reference table is the controlled join surface for later phases. It
does not prove that downstream EEA, Wikipedia, Open-Meteo, Kafka, Spark, or
analytics outputs already exist. It only defines the stable city-level fields
that later source-specific work must map to.

### Identifier Convention

`city_id` is the stable technical identifier for joins. It uses lowercase
ASCII text in the pattern `<normalized_city_name>_<country_code_lower>`.
Spaces and punctuation are replaced or removed during normalization. The
country code suffix uses ISO 3166-1 alpha-2 in lowercase form.

Examples:

- `vienna_at`
- `berlin_de`
- `amsterdam_nl`

Once a `city_id` is used by downstream data, it should not be renamed without a
documented migration note. Downstream jobs should join on `city_id`, not on free
text city names.

### Schema

| field | type | required | nullability | rule |
| --- | --- | --- | --- | --- |
| city_id | string | yes | non-null | Unique stable key using lowercase `<normalized_city_name>_<country_code_lower>`. |
| city_name | string | yes | non-null | Human-readable display name, for example `Vienna`. |
| city_name_normalized | string | yes | non-null | Lowercase normalized city name used to derive `city_id`. |
| country_code | string | yes | non-null | ISO 3166-1 alpha-2 country code in uppercase, for example `AT`. |
| latitude | float | yes | non-null | WGS84 city coordinate used for Open-Meteo feasibility and later source alignment; must be between -90 and 90. |
| longitude | float | yes | non-null | WGS84 city coordinate used for Open-Meteo feasibility and later source alignment; must be between -180 and 180. |
| population | integer | no | nullable | Future contextual metadata, expected from Wikipedia or another documented reference source. |
| area_km2 | float | no | nullable | Future contextual metadata, expected from Wikipedia or another documented reference source. |
| population_density | float | no | nullable | Future contextual or derived metadata; may stay null if population or area is unavailable. |
| mapping_notes | string | yes | non-null | Short explanation of why the city belongs in the controlled starter scope and how source alignment should be interpreted. |
| eea_station_selection_notes | string | yes | non-null | Notes for future EEA station-to-city matching; this is not an implemented station mapping. |
| wikipedia_page_title | string | no | nullable | Planned Wikipedia page title used for metadata linkage. |
| wikipedia_url | string | no | nullable | Planned Wikipedia page URL used for traceability. |
| wikipedia_metadata_notes | string | no | nullable | Notes about expected Wikipedia metadata fields, ambiguity, or fallback handling. |
| open_meteo_coordinate_notes | string | no | nullable | Notes about coordinate assumptions for future Open-Meteo API checks. |

### Constraints And Validation Rules

- `city_id` must be unique across the city reference table.
- Required fields must not be null or empty.
- `country_code` must be exactly two uppercase letters.
- `latitude` and `longitude` must be numeric and within WGS84 ranges.
- Optional metadata fields may be null during Phase 2 and must not block city
  reference creation.
- EEA station mapping remains a documented mapping decision until later
  ingestion phases; Phase 2 must not download or process full EEA datasets.
- Wikipedia fields are linkage metadata only in Phase 2; production scraping
  and parser implementation remain out of scope.
- The schema is intentionally small enough to support focused tests in
  `tests/test_city_mapping.py`.

### Phase 2.3 Local Builder

`src/city_mapping/build_city_reference.py` implements the first deterministic
city reference builder from local constants. The module is side-effect free on
import. It writes the following local Silver artifacts only when explicitly
called:

- `data/silver/city_reference.csv`
- `data/silver/city_reference.parquet`

Both generated files are ignored by `.gitignore` under the repository data
policy. They are local Phase 2 deliverables, not committed source data.

## Phase 2 Scope Boundary

Allowed in Phase 2:

- define stable city identifiers,
- document the city reference scope,
- design the city reference schema,
- prepare EEA station mapping rules,
- prepare Wikipedia metadata join rules,
- prepare Open-Meteo coordinate and field mapping rules,
- add city reference validation tests.

Not allowed in Phase 2:

- EEA data download or ingestion,
- production Wikipedia scraping,
- Open-Meteo production client behavior,
- Kafka producer implementation,
- Spark Structured Streaming,
- Bronze/Silver/Gold transformations beyond the local city reference outputs
  planned for later Phase 2 issues,
- final analytics or visualizations.

## Later Data Model Work

TODO:

- Define Bronze schemas per source.
- Define Silver canonical model for city and air quality joins.
- Define Gold analytical tables for the project research question.
