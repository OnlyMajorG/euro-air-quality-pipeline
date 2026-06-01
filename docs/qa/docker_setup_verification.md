# QA-Bericht: Lokales Docker-Setup

## Status

BESTANDEN AM 1. JUNI 2026

## Ausgeführte Infrastruktur

| Dienst | Ergebnis |
| --- | --- |
| Kafka `apache/kafka:3.9.2` | erreichbar und gesund |
| Spark-Master `spark:3.5.7-scala2.12-java17-python3-ubuntu` | erreichbar und gesund |
| Spark-Worker | beim Master registriert |
| Jupyter | erreichbar; interne Verbindung zu Kafka und Spark-Master erfolgreich |

## Automatische Prüfung

Notebook `00_project_scope_and_requirements.ipynb` enthält Start, Auswahl und Prüfung der Infrastruktur direkt. Ergebnis: Docker wurde ausgewählt. Kafka auf `localhost:9092`, Spark-Master auf `localhost:7077`, Jupyter auf `localhost:8888` und die internen Container-Verbindungen waren erreichbar.

## Strikter Notebook-Nachweis

| Notebook | Ergebnis |
| --- | --- |
| `05_open_meteo_api_and_kafka_producer.ipynb` | `mode='kafka'`, 8 Ereignisse gesendet, 8 konsumiert, kein Fallback |
| `06_spark_structured_streaming_kafka_to_parquet.ipynb` | `spark_master='spark://spark-master:7077'`, `selected_source_mode='kafka'`, `spark_read_kafka_requirement_proven=True` |
| `07_gold_layer_and_data_quality.ipynb` | `spark_storage_status.passed=True`, Live-Eingabe aus `phase6_spark_stream_silver` |

## Abgrenzung

Der Docker-Nachweis belegt den lokalen Kafka-zu-Spark-Pfad. Für finale empirische Aussagen muss der EEA-API-Analysezeitraum erweitert werden. Ein zusätzlicher FH-Lauf ist optional möglich und benötigt die tatsächlichen FH-Endpunkte sowie ein gruppenspezifisches Topic.
