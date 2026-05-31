# Prüfung der Cluster-Erreichbarkeit

## Ergebnis

- Spark-Master erreichbar
- grundlegende Spark-Berechnung möglich
- gemeinsamer Speicher nicht bestätigt
- lokale Jupyter-Pfade nicht automatisch für Cluster-Executors sichtbar

## Entscheidung

Lokale Parquet-Ausgaben verwenden Spark `local[*]`. Der FH-Cluster wird für den strikten Kafka-zu-Spark-Nachweis genutzt. Aussagen über Cluster-Speicher erfordern einen erfolgreichen Schreib- und Lesetest.
