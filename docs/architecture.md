# Architektur

## Pipeline (Notebooks 00–10)

1. **`00`** startet die Infrastruktur: lokal `docker compose up` (Kafka, Spark, PostgreSQL, Jupyter),
   auf der FH eine Erreichbarkeitsprüfung.
2. **`01`** beschreibt Umfang, Leitfrage und Anforderungs-Mapping.
3. **`02`** prüft die Erreichbarkeit der drei Quellen und der Infrastruktur.
4. **`03`** erstellt die Stadtreferenz (`city_id`) als gemeinsame Grundlage.
5. **`04`** ruft historische EEA-Messungen ab. Lokal nach PostgreSQL (`bronze.eea_observation`),
   auf der FH nach `data/bronze/eea/eea_observation.parquet`. Beide Wege erzeugen dasselbe
   Silver-Parquet `eea_city_daily.parquet` mit Tageswerten.
6. **`05`** scrapt Wikipedia-Stadtseiten und speichert Stadtmetadaten als Silver.
7. **`06`** ruft die Open-Meteo-REST-API ab, baut versionierte Events und sendet sie mit einem
   `confluent-kafka`-Producer an das Topic.
8. **`07`** liest die Events mit Spark Structured Streaming aus Kafka, validiert das Schema, ergänzt
   Stadtkontext und schreibt das Silver-Parquet `open_meteo_city_hourly`. Das Kafka-Topic ist die Rohschicht.
9. **`08`** erstellt fünf Gold-Tabellen und einen Qualitätsbericht.
10. **`09`** erzeugt die Abbildungen und die Ergebnisgeschichte.
11. **`10`** löscht Laufzeitdaten und fährt die lokale Infrastruktur herunter.

## Ereignisvertrag

Notebook `06` erzeugt flache JSON-Events mit `event_id` (SHA256, deterministisch), `schema_version`
(`"1.0"`), `source` (`"open_meteo"`), `city_id`, `event_time_utc`, `ingestion_time_utc`, `data_status`,
`pm2_5`, `pm10` und `no2`. Die deterministische `event_id` erlaubt Deduplizierung in Spark.

## Kafka und Spark

Beide Zielumgebungen (lokales Docker und FH) verwenden einen **echten** Kafka-Broker — keine
Mock-/Fallback-Modi. Spark liest mit `readStream.format("kafka")` und `from_json()` (explizites Schema)
und schreibt mit `writeStream.format("parquet")`.

## Gold-Schicht

Notebook `08` schreibt reproduzierbare Gold-Parquet-Dateien. Historische EEA-Daten und der
Open-Meteo-Live-Snapshot bleiben über `dataset_context` getrennt (`eea_historical` / `open_meteo_live`).
