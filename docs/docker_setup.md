# Lokales Docker-Setup

## Zweck

Das Docker-Setup bildet den Kafka-zu-Spark-Pfad lokal mit Docker Desktop ab. `docker compose` startet:

- einen Kafka-Broker im KRaft-Modus
- eine PostgreSQL-Datenbank für historische EEA-Bronze-Daten
- einen Spark-Master und einen Spark-Worker
- Jupyter Notebook mit den Python-Abhängigkeiten des Projekts

Das Projektverzeichnis wird in Jupyter und Spark-Worker unter `/workspace` eingebunden, daher haben
Driver und Worker gemeinsamen Speicher. Die Spark-Streaming-Checkpoints liegen in einem gemeinsamen
Docker-Named-Volume. Jupyter verwendet Python `3.10`, passend zur Python-Version des Spark-Images,
damit PySpark-Jobs mit Python-Serialisierung funktionieren.

## Start über Notebook `00`

Docker Desktop starten, dann Notebook `00_infrastructure_startup.ipynb` ausführen. Es führt
`docker compose up -d --build` aus und wartet, bis Kafka, Spark, PostgreSQL und Jupyter erreichbar sind.

Danach `http://localhost:8888` öffnen und die Notebooks `01` bis `09` in Reihenfolge ausführen.
Notebook `07` (Spark Structured Streaming) muss im Docker-Jupyter laufen.

| Dienst | URL |
| --- | --- |
| Jupyter Notebook | `http://localhost:8888` |
| PostgreSQL | `localhost:5432` |
| Spark-Master-UI | `http://localhost:8080` |
| Spark-Worker-UI | `http://localhost:8081` |

Die Datei `.env.docker.example` wird automatisch in den Jupyter-Container geladen. PostgreSQL-Daten
bleiben im Named Volume `postgres-data`, bis es entfernt wird.

## Infrastruktur-Nachweis

1. Notebook `04`: reale EEA-API-Daten in `bronze.eea_observation`
2. Notebook `06`: Events werden an Kafka gesendet
3. Notebook `07`: `spark_read_kafka_requirement_proven == True`

Der erste Spark-Kafka-Lauf lädt den passenden Connector aus Maven Central; dafür benötigt der
Jupyter-Container Netzwerkzugriff.

## Stop über Notebook `10`

Notebook `10_reset_data.ipynb` löscht die erzeugten Laufzeitdateien (außer `.gitkeep`) und fährt mit
`docker compose down` die Infrastruktur herunter. Die gelöschten Daten lassen sich durch erneutes
Ausführen der Pipeline wiederherstellen. Für einen vollständigen Reset inkl. Datenbank
`docker compose down -v` im Terminal verwenden.
