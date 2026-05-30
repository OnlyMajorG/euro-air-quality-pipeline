# Phase 4 Pre-Check

## Purpose

This pre-check records the Phase 4 starting boundary before Wikipedia scraping
work begins. It is documentation only and does not fetch pages, scrape HTML, or
implement parser logic.

## Approved Phase 4 Scope

Allowed:

- controlled Wikipedia HTML handling for the 8 starter cities,
- defensive parser implementation,
- city metadata joined through `city_id`,
- parser tests,
- notebook 03 documentation.

Not allowed:

- Open-Meteo production client behavior,
- Kafka producer implementation,
- Spark Structured Streaming,
- Gold tables,
- dashboards or final visualizations.

## Starter City Pages To Review

| city_id | expected English Wikipedia page |
| --- | --- |
| `vienna_at` | `Vienna` |
| `berlin_de` | `Berlin` |
| `paris_fr` | `Paris` |
| `madrid_es` | `Madrid` |
| `rome_it` | `Rome` |
| `amsterdam_nl` | `Amsterdam` |
| `warsaw_pl` | `Warsaw` |
| `prague_cz` | `Prague` |

## Gate Decision

Phase 4 may start. The first implementation issue must keep the Wikipedia
module side-effect free on import and must not perform uncontrolled crawling.
