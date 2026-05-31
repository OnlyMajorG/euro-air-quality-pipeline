# Datenquellen

## Übersicht

| Quelle | Typ | Zweck | Notebook |
| --- | --- | --- | --- |
| Historische EEA-Luftqualitätsdaten | Datei und Batch | PM2.5-, PM10- und NO2-Messungen | `03_eea_batch_ingestion.ipynb` |
| Wikipedia-Stadtseiten | Web-Scraping | Bevölkerung, Fläche und Bevölkerungsdichte | `04_wikipedia_web_scraping.ipynb` |
| Open-Meteo Air Quality API | REST-API | Aktuelle Ereignisse für den Kafka-Pfad | `05_open_meteo_api_and_kafka_producer.ipynb` |

## EEA

Notebook `03` erwartet lokale CSV- oder Parquet-Dateien. Messungen werden auf PM2.5, PM10 und NO2 gefiltert, normalisiert, einer `city_id` zugeordnet und auf Tageswerte aggregiert. Ohne realen Extrakt kann ein kontrolliertes Sample den technischen Ablauf demonstrieren. Dieses Sample ist keine Grundlage für finale empirische Aussagen.

## Wikipedia

Wikipedia dient ausschließlich als Kontextquelle. Das HTML-Parsing ist defensiv implementiert. Fehlende oder mehrdeutige Werte bleiben leer und werden nicht geraten.

## Open-Meteo

Open-Meteo liefert REST-API-Daten und Kafka-Ereignisse. Die API-Felder werden auf `pm2_5`, `pm10` und `no2` vereinheitlicht. Notebook `05` speichert pro Stadt eine Bronze-JSON-Datei, ein Manifest und einen validierten JSONL-Batch.

## Gold-Ausgaben

| Datensatz | Kontext | Zweck |
| --- | --- | --- |
| `city_air_quality_daily_summary.parquet` | `eea_historical` | Historische Tageswerte |
| `pollutant_ranking_by_city.parquet` | `eea_historical` | Schadstoffspezifische Rangfolgen |
| `city_context_air_quality.parquet` | `eea_historical` | Rangfolgen mit Stadtkontext |
| `live_air_quality_latest.parquet` | `open_meteo_live` | Getrennter aktueller API- und Kafka-Snapshot |
| `data_quality_summary.parquet` | Qualitätsmetadaten | Zeilenzahlen, Duplikate, fehlende Werte und Herkunft |
