# Architektur

## Pipeline

1. Historische EEA-Dateien bilden die Datei- und Batch-Quelle.
2. Wikipedia-Stadtseiten liefern Kontextdaten über Web-Scraping.
3. Die Open-Meteo-REST-API liefert aktuelle Luftqualitätsdaten.
4. Notebook `05` speichert Bronze-JSON und validierte JSONL-Ereignisse.
5. Bei erreichbarem Broker werden Open-Meteo-Ereignisse an ein gruppenspezifisches Kafka-Topic gesendet und mit einem begrenzten Consumer-Test geprüft.
6. Spark Structured Streaming liest Kafka-Ereignisse, validiert das Schema, ergänzt Stadtkontext und schreibt Parquet-Dateien.
7. Notebook `07` erstellt Gold-Datensätze und einen Qualitätsbericht.
8. Notebook `08` erzeugt Diagramme und die Ergebnisgeschichte.

## Ereignisvertrag

Notebook `05_open_meteo_api_and_kafka_producer.ipynb` erzeugt flache JSON-Ereignisse mit `event_id`, `schema_version`, `source`, `city_id`, `event_time_utc`, `ingestion_time_utc`, `data_status`, `pm2_5`, `pm10` und `no2`.

## Kafka-Modi

- `KAFKA_MODE=kafka`: strikter FH-Nachweismodus; Brokerfehler brechen den Lauf ab.
- `KAFKA_MODE=auto`: Kafka bevorzugen und nur bei erlaubtem Fallback den Mock-Broker verwenden.
- `KAFKA_MODE=mock`: lokaler JSONL-Mock-Broker.

## Spark-Kafka-Modi

- `SPARK_KAFKA_MODE=kafka`: strikter FH-Nachweismodus.
- `SPARK_KAFKA_MODE=auto`: Kafka bevorzugen und bei erlaubtem Fallback den lokalen Spark-Dateistream verwenden.
- `SPARK_KAFKA_MODE=mock`: lokale Spark-Structured-Streaming-Verarbeitung aus JSONL.
- `pandas_mock_no_pyspark`: reduzierter Strukturtest, wenn PySpark lokal fehlt.

Der pandas-Pfad prüft Verträge, Qualitätsregeln, Joins und Parquet-Übergaben. Er ist weder ein Spark- noch ein Kafka-Nachweis. Der strikte Modus bricht ohne PySpark kontrolliert ab.

## Gold-Schicht

Notebook `07_gold_layer_and_data_quality.ipynb` schreibt reproduzierbare Gold-Parquet-Dateien. Historische EEA-Daten und der Open-Meteo-Live-Snapshot bleiben getrennt. Fallback-Herkunft wird über `live_input_mode` sichtbar gespeichert.

## Notebook-basierte Umsetzung

Die Implementierungslogik liegt in den geordneten Notebooks `00` bis `08`. Notebook `09` ist ein abgesichertes Hilfsnotebook zum Zurücksetzen lokaler Laufzeitdaten.
