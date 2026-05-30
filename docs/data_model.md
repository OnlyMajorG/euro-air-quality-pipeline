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

- Define the full city reference schema.
- Define Bronze schemas per source.
- Define Silver canonical model for city and air quality joins.
- Define Gold analytical tables for the project research question.
