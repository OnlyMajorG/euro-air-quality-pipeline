# Lokales Docker-Setup

## Zweck

Das Docker-Setup bildet den strikten Kafka-zu-Spark-Pfad lokal mit Docker Desktop ab. Es startet:

- einen Kafka-Broker im KRaft-Modus
- einen Spark-Master
- einen Spark-Worker
- Jupyter Notebook mit den Python-Abhängigkeiten des Projekts

Notebook `05` veröffentlicht Open-Meteo-Ereignisse an Kafka. Notebook `06` liest sie mit Spark Structured Streaming aus Kafka und schreibt Parquet-Dateien. Das Projektverzeichnis wird in Jupyter und Spark-Worker unter `/workspace` eingebunden. Dadurch ist gemeinsamer Speicher für Driver und Worker vorhanden.

Die Spark-Streaming-Checkpoints liegen in einem gemeinsamen Docker-Named-Volume. Für den kleinen lokalen Nachweislauf ist `SPARK_SQL_SHUFFLE_PARTITIONS=1` gesetzt, damit Checkpoint-State auf Docker Desktop reproduzierbar geschrieben wird.

Der lokale Spark-Worker läuft im Compose-Setup als `root`, weil Jupyter und Worker denselben Windows-Bind-Mount beschreiben. Das ist eine lokale Entwicklungsentscheidung und keine Produktionskonfiguration.

Jupyter verwendet im Docker-Setup Python `3.10`, passend zur Python-Minor-Version des offiziellen Spark-Worker-Images. Dadurch funktionieren auch PySpark-Jobs mit Python-Serialisierung.

## Start über Notebook 00

Der Benutzerablauf erfolgt ausschließlich über Notebooks. In einem lokal verfügbaren Jupyter Notebook `00_project_scope_and_requirements.ipynb` öffnen und ausführen. Notebook `00` startet Docker Desktop bei Bedarf, führt Docker Compose aus und prüft die Host-Endpunkte.

Danach `http://localhost:8888` öffnen und Notebook `00` im Docker-Jupyter erneut ausführen. Dort werden Kafka und Spark im internen Compose-Netzwerk geprüft. Anschließend die Notebooks `01` bis `09` in Reihenfolge ausführen.

Die Oberflächen sind anschließend erreichbar:

| Dienst | URL |
| --- | --- |
| Jupyter Notebook | `http://localhost:8888` |
| Spark-Master | `http://localhost:8080` |
| Spark-Worker | `http://localhost:8081` |

Die Docker-Konfiguration liegt in `.env.docker.example` und wird automatisch in den Jupyter-Container geladen. Sie verwendet einen lokalen, nicht gruppenspezifischen Kafka-Topic-Namen.

## Notebook-Lauf

Die Notebooks werden in Jupyter in der Reihenfolge `00` bis `08` ausgeführt. Für den Infrastruktur-Nachweis sind insbesondere relevant:

1. Notebook `05`: `broker_result["mode"] == "kafka"`
2. Notebook `06`: `selected_source_mode == "kafka"`
3. Notebook `06`: `spark_read_kafka_requirement_proven == True`
4. Notebook `07`: erfolgreiche Spark-Speicherprobe

Der erste Spark-Kafka-Lauf lädt den passenden Connector aus Maven Central. Dafür benötigt der Jupyter-Container Netzwerkzugriff.

## Stop über Notebook 09

Notebook `09_reset_data.ipynb` löscht standardmäßig die erzeugten Laufzeitdateien und startet einen kurzlebigen Docker-Helper. Dieser fährt den Compose-Stack nach Abschluss der Notebook-Zelle herunter. Für eine reine Löschvorschau `DRY_RUN=true` setzen.

## FH-Umgebung

Die FH-Umgebung bleibt eine zweite, unabhängige Ausführungsoption. Vor der Ausführung von Notebook `00` müssen die Platzhalter in `.env` durch die tatsächlichen FH-Endpunkte, das Gruppen-Topic und gegebenenfalls einen bestätigten gemeinsamen Speicherpfad ersetzt werden. Mit `PROJECT_EXECUTION_MODE=fh` prüft Notebook `00` ausschließlich die FH-Umgebung. `ALLOW_SHARED_SPARK_STORAGE=true` darf erst nach bestätigtem gemeinsamem Speicher gesetzt werden.
