# ADR-004: Ausführungsumgebung und Speicherstrategie

## Status

Akzeptiert

## Kontext

Der FH-Spark-Cluster war erreichbar, gemeinsamer Speicher ist jedoch nicht bestätigt.

## Entscheidung

Lokale Läufe ohne Docker verwenden `SPARK_MASTER_URL=local[*]`. Für den strikten Kafka-zu-Spark-Nachweis stehen zwei Wege bereit:

1. Docker Compose mit Kafka, Spark-Master, Spark-Worker und Jupyter. Jupyter und Worker binden denselben Projektpfad `/workspace` ein; deshalb ist gemeinsamer Speicher deklarativ bestätigt.
2. FH-Cluster mit den bereitgestellten Endpunkten. Cluster-Speicher wird erst nach erfolgreicher Schreib- und Leseprüfung verwendet.

Notebook `06` verwendet einen entfernten Spark-Master nur bei `ALLOW_SHARED_SPARK_STORAGE=true`. Andernfalls bleibt die Parquet-Ausgabe bewusst bei `local[*]`.
