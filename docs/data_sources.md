# Datenquellen

## Übersicht

| Quelle | Typ | Zweck | Notebook |
| --- | --- | --- | --- |
| Historische EEA-Luftqualitätsdaten | EEA Downloads API (Datei/DB) | PM2.5-, PM10- und NO2-Messungen | `04_eea_batch_ingestion.ipynb` |
| Wikipedia-Stadtseiten | Web-Scraping | Bevölkerung, Fläche und Bevölkerungsdichte | `05_wikipedia_web_scraping.ipynb` |
| Open-Meteo Air Quality API | REST-API | Aktuelle Ereignisse für den Kafka-Pfad | `06_open_meteo_api_and_kafka_producer.ipynb` |

## EEA

Notebook `04` ruft über `/ParquetFile/urls` stadtbezogene EEA-Parquet-URLs ab und filtert PM2.5, PM10 und NO2. Lokal speichert es die Messungen in `bronze.eea_observation` im PostgreSQL-Container, auf der FH ohne PostgreSQL in `data/bronze/eea/eea_observation.parquet`. Die Silver-Verarbeitung aggregiert in beiden Modi auf Tageswerte. Der Default `[2025-01-01, 2026-01-01)` umfasst exakt `365` Tage; für einen kürzeren Testlauf `EEA_DATE_END` näher an `EEA_DATE_START` setzen.

## Wikipedia

Wikipedia dient ausschließlich als Kontextquelle. Das HTML-Parsing ist defensiv: fehlende oder mehrdeutige Werte bleiben leer und werden nicht geraten. `parse_status` dokumentiert den Erfolg je Stadt. Zusätzlich kennzeichnet das Flag `density_comparable` (mit Begründung in `area_basis_note`) Städte, deren Fläche/Dichte nicht direkt vergleichbar ist — z. B. **Paris**, das Wikipedia als Kernkommune (~105 km²) statt als größeres Verwaltungsgebiet führt (Modifiable Areal Unit Problem). Notebook `09` wertet dieses Flag aus, statt die Werte stillschweigend zu vermischen.

## Open-Meteo

Open-Meteo liefert REST-API-Daten für den Kafka-Pfad. Die API-Felder werden auf `pm2_5`, `pm10` und `no2` vereinheitlicht. Notebook `06` speichert pro Stadt eine Bronze-JSON-Datei und einen validierten JSONL-Batch und sendet die Events mit einem `confluent-kafka`-Producer an das Topic.

## Gold-Ausgaben

| Datensatz | Kontext | Zweck |
| --- | --- | --- |
| `city_air_quality_daily_summary.parquet` | `eea_historical` | Historische Tageswerte |
| `pollutant_ranking_by_city.parquet` | `eea_historical` | Schadstoffspezifische Rangfolgen |
| `city_context_air_quality.parquet` | `eea_historical` | Rangfolgen mit Stadtkontext (inkl. `density_comparable`, `area_basis_note`) |
| `live_air_quality_latest.parquet` | `open_meteo_live` | Getrennter aktueller API- und Kafka-Snapshot |
| `data_quality_summary.parquet` | Qualitätsmetadaten | Zeilen- und Spaltenzahl, fehlende Werte und abgedeckter Zeitraum (`coverage_days`; für den Live-Snapshot `<NA>`, da Momentaufnahme) |
