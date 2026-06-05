# ADR-004: Ausführungsumgebung und Speicherstrategie

## Status

Akzeptiert

## Kontext

Der FH-Spark-Cluster war erreichbar, gemeinsamer Speicher ist jedoch nicht bestätigt.

## Entscheidung

Die Ausführungsumgebung wird allein über `EXECUTION_ENV` in der `.env` gewählt; es gibt keine Auto-Erkennung im Code. Für den Kafka-zu-Spark-Nachweis stehen zwei Wege bereit:

1. **Docker Compose** mit Kafka, Spark-Master, Spark-Worker und Jupyter. Jupyter und Worker binden denselben Projektpfad `/workspace` ein, daher ist gemeinsamer Speicher vorhanden. Notebook `07` nutzt `SPARK_MASTER_URL=spark://spark-master:7077`.
2. **FH-Cluster** mit den bereitgestellten Endpunkten. Da kein gemeinsamer Cluster-Speicher bestätigt ist, läuft Spark dort mit `SPARK_MASTER_URL=local[*]` (im Notebook-Prozess); der Kafka-Nachweis bleibt davon unberührt.

Analog wählt `EEA_BRONZE_STORAGE_MODE` das EEA-Bronze-Backend: `postgres` lokal, `parquet` auf der FH.
