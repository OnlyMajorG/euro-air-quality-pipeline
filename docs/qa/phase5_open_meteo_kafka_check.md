# QA-Bericht Phase 5: Open-Meteo und Kafka-Produzent

## Ergebnis

Status: IMPLEMENTIERT, LOKALER MOCK BESTANDEN, FH-NACHWEIS OFFEN

Notebook `05_open_meteo_api_and_kafka_producer.ipynb` lädt Open-Meteo-Daten, speichert Bronze-JSON, erzeugt validierte JSONL-Ereignisse und enthält einen Kafka-Produzenten mit begrenztem Consumer-Test.

## Lokal geprüft

- acht eindeutige Städte
- sichtbare Herkunft über `data_status`
- JSONL-Ereignisbatch
- deterministische `event_id`
- lokaler JSONL-Mock-Broker
- Schutztest: eine unsichere Kafka-Placeholder-Konfiguration wird abgelehnt

## Ereignisvertrag

`event_id`, `schema_version`, `source`, `city_id`, `event_time_utc`, `ingestion_time_utc`, `data_status`, `pm2_5`, `pm10`, `no2`

## Offener FH-Nachweis

Notebook `05` muss mit gruppenspezifischem Topic, erreichbarem Broker, `KAFKA_MODE=kafka`, deaktiviertem Mock-Fallback und aktivem Produzenten ausgeführt werden.
