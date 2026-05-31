# ADR-004: Ausführungsumgebung und Speicherstrategie

## Status

Akzeptiert

## Kontext

Der FH-Spark-Cluster war erreichbar, gemeinsamer Speicher ist jedoch nicht bestätigt.

## Entscheidung

Lokale Parquet-Ausgaben verwenden `SPARK_MASTER_URL=local[*]`. Der FH-Cluster dient dem strikten Kafka-zu-Spark-Nachweis. Cluster-Speicher wird erst nach erfolgreicher Schreib- und Leseprüfung verwendet.
