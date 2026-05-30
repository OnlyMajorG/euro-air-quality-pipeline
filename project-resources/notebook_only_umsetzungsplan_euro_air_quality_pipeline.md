# Umsetzungsplan: Notebook-only `euro-air-quality-pipeline`

**Projekt:** Luftqualitätsmuster in europäischen Städten  
**Repository:** `euro-air-quality-pipeline`  
**Projektart:** Big Data Engineering / Data Science Projekt  
**Strukturentscheidung:** Notebook-only Implementierung  
**Status:** adaptiert an die offiziellen LV-Anforderungen und die bisher getestete FH-/BDENG-Clusterumgebung

---

## 1. Executive Summary

Dieses Projekt wird als **Notebook-only Data-Engineering-Projekt** umgesetzt.

Die offizielle Aufgabenstellung verlangt ein Data-Science-Projekt mit Fokus auf Big Data Engineering. Im Zentrum stehen nicht primär komplexe Algorithmen, sondern die praktische Anwendung verschiedener Technologien:

- mindestens drei verschiedene Datenquellen,
- Datei-/Batch-Quelle oder Datenbank,
- Web Scraping,
- REST API,
- Kafka Producer,
- Spark liest aus Kafka,
- ETL/ELT-Speicherung,
- Visualisierung des Datenflusses,
- Storytelling,
- Dokumentation jedes Schritts in Jupyter Notebooks,
- öffentliches GitHub-Repository zur Bereitstellung der Notebooks.

Daher wird die Projektlogik bewusst in nummerierten Jupyter Notebooks umgesetzt. Es gibt keinen produktionsnahen `src/`-Layer und keinen klassischen `tests/`-Ordner. Qualitätssicherung erfolgt durch Validierungszellen, klare Notebook-Struktur, dokumentierte Entscheidungen und QA-Dokumente.

---

## 2. Projektziel

### 2.1 Thema

**European Air Quality Patterns**

Das Projekt untersucht Luftqualitätsmuster ausgewählter europäischer Städte anhand historischer, aktueller und kontextueller Datenquellen.

### 2.2 Leitfrage

> Welche Luftqualitätsmuster zeigen ausgewählte europäische Städte im historischen und aktuellen Vergleich, und wie lassen sich diese Unterschiede durch urbane Kontextdaten einordnen?

### 2.3 Technisches Ziel

Aufbau einer nachvollziehbaren Big-Data-Engineering-Pipeline, die:

1. historische Luftqualitätsdaten verarbeitet,
2. Stadtmetadaten per Web Scraping extrahiert,
3. aktuelle Luftqualitätsdaten per REST API bezieht,
4. API-Daten über Kafka bereitstellt,
5. Kafka-Daten mit Spark Structured Streaming verarbeitet,
6. transformierte Ergebnisse als Parquet speichert,
7. Ergebnisse in Jupyter visualisiert,
8. den Datenfluss und die technischen Entscheidungen dokumentiert.

---

## 3. Core Scope

| Bereich | Festlegung |
|---|---|
| Thema | Luftqualitätsmuster europäischer Städte |
| Städte | Start mit 8 Städten |
| Schadstoffe | PM2.5, PM10, NO2 |
| Datei-/Batch-Quelle | EEA historische Luftqualitätsdaten |
| Web-Scraping-Quelle | Wikipedia-Stadtseiten |
| REST-API-Quelle | Open-Meteo Air Quality API |
| Broker | Kafka |
| Streaming / Processing | Spark Structured Streaming |
| Storage | Parquet mit Bronze/Silver/Gold-Struktur |
| Dokumentation | Jupyter Notebooks |
| Visualisierung | Matplotlib / Pandas |
| Präsentation | Storyline + Abbildungen |
| Repository | öffentliches GitHub-Repo |

---

## 4. Non-Goals

| Nicht-Ziel | Begründung |
|---|---|
| Produktionsreife Plattform | Kursprojekt, kein Enterprise Deployment |
| Airflow | nicht erforderlich, hoher Zusatzaufwand |
| dbt | nicht notwendig für Notebook-/Parquet-Setup |
| PostgreSQL im Core | Parquet erfüllt Storage-Anforderung einfacher |
| Dashboard | optionaler Scope Creep |
| Machine Learning | nicht gefordert; Fokus liegt auf Data Engineering |
| Kausalanalyse | Datenlage und Scope reichen dafür nicht |
| vollständige Cluster-Storage-Integration | bisher kein Shared Storage nachgewiesen |

---

## 5. Execution Strategy

### 5.1 Bisheriger Cluster-Befund

Die FH-/BDENG-Clusterumgebung wurde getestet:

| Test | Ergebnis |
|---|---|
| Spark Master erreichbar | bestanden |
| Spark Version abrufbar | bestanden |
| `df.show()` mit Spark Cluster | bestanden |
| Spark UI sichtbar | bestanden |
| HDFS verfügbar | nicht verfügbar |
| `fs.defaultFS` | `file:///` |
| `hdfs` CLI | nicht vorhanden |
| lokaler Jupyter-Pfad als Shared Storage | nicht zuverlässig |
| Spark-Cluster schreibt vollständige Parquet-Dateien in `data/` | nicht nachgewiesen |

### 5.2 Konsequenz

Die Parquet-produzierende Pipeline wird standardmäßig mit Spark `local[*]` ausgeführt.

```text
SPARK_MASTER_URL=local[*]
```

Der FH Spark Cluster bleibt dokumentierter Connectivity- und Compute-Nachweis, wird aber nicht als finaler Parquet-Storage-Pfad verwendet, solange kein gemeinsamer Storage bestätigt wurde.

### 5.3 Execution Modes

| Modus | Zweck | Spark Master | Storage |
|---|---|---|---|
| `local_project` | Standard-Pipeline | `local[*]` | `data/` |
| `fh_cluster_connectivity` | Spark-Smoke-Test | `spark://<fh-spark-master>:7077` | kein finaler Storage |
| `fh_cluster_shared_storage` | optionaler Cluster-End-to-End-Modus | FH Spark Master | nur bestätigter Shared Storage |

---

## 6. Zielstruktur des Repositories

```text
euro-air-quality-pipeline/
│
├── README.md
├── requirements.txt
├── .env.example
├── .env.cluster.example
├── .gitignore
├── LICENSE
│
├── notebooks/
│   ├── 00_project_scope_and_requirements.ipynb
│   ├── 01_source_spike_and_cluster_check.ipynb
│   ├── 02_city_reference_model.ipynb
│   ├── 03_eea_batch_ingestion.ipynb
│   ├── 04_wikipedia_web_scraping.ipynb
│   ├── 05_open_meteo_api_and_kafka_producer.ipynb
│   ├── 06_spark_structured_streaming_kafka_to_parquet.ipynb
│   ├── 07_gold_layer_and_data_quality.ipynb
│   └── 08_analysis_visualization_and_storytelling.ipynb
│
├── docs/
│   ├── architecture.md
│   ├── data_sources.md
│   ├── cluster_setup.md
│   ├── limitations.md
│   ├── decisions/
│   │   ├── ADR-001-scope-freeze.md
│   │   ├── ADR-002-notebook-only-implementation.md
│   │   ├── ADR-003-parquet-bronze-silver-gold.md
│   │   └── ADR-004-execution-environment-and-storage-strategy.md
│   ├── qa/
│   │   ├── phase0_qa_report.md
│   │   ├── cluster_connectivity_check.md
│   │   └── final_readiness_check.md
│   └── diagrams/
│       ├── architecture.mmd
│       └── dataflow.mmd
│
├── data/
│   ├── bronze/
│   │   ├── eea/.gitkeep
│   │   ├── wikipedia_html/.gitkeep
│   │   └── open_meteo_raw/.gitkeep
│   ├── silver/.gitkeep
│   ├── gold/.gitkeep
│   ├── checkpoints/.gitkeep
│   └── samples/.gitkeep
│
└── presentation/
    ├── final_storyline.md
    ├── presentation_outline.md
    └── figures/.gitkeep
```

---

## 7. Notebook Standardstruktur

Jedes Notebook muss dieselbe Grundstruktur verwenden:

```text
1. Purpose
2. Inputs
3. Outputs
4. Technologies used
5. Configuration
6. Implementation
7. Validation / Quality Checks
8. Results
9. Limitations
10. Next step
```

Diese Struktur ersetzt klassische Unit Tests teilweise durch nachvollziehbare, sichtbare Validierungsschritte im Notebook.

---

## 8. Requirement Mapping

| LV-Anforderung | Umsetzung | Nachweis |
|---|---|---|
| Thema selbst wählen | European Air Quality Patterns | Notebook 00 |
| supplementary research | Datenquellen, Kontext, Luftqualität | Notebook 00, 01, docs |
| provided infrastructure kennenlernen | FH Spark/Kafka Check | Notebook 01, `docs/qa/cluster_connectivity_check.md` |
| mindestens 3 Datenquellen | EEA, Wikipedia, Open-Meteo | Notebooks 03, 04, 05 |
| Datei-/DB-Quelle | EEA historische Daten | Notebook 03 |
| Web Scraping | Wikipedia | Notebook 04 |
| REST API | Open-Meteo | Notebook 05 |
| Kafka Producer | Open-Meteo Events nach Kafka | Notebook 05 |
| Spark liest Kafka | Structured Streaming | Notebook 06 |
| ETL/ELT speichern | Parquet Bronze/Silver/Gold | Notebooks 03, 06, 07 |
| Storytelling | Luftqualitätsmuster | Notebook 08 |
| Datenfluss visualisieren | Mermaid Diagramme | `docs/diagrams/` |
| jedes Schritt in Jupyter dokumentieren | Notebook 00–08 | `notebooks/` |
| Public GitHub Repo | Notebooks teilen | README / GitHub |

---

## 9. Phase 0 — Refactor auf Notebook-only

### Ziel

Das bestehende Repository wird auf die Notebook-only-Struktur umgebaut.

### Aufgaben

1. Bestehende Repo-Struktur analysieren.
2. Falls `src/` oder `tests/` existieren: nützliche Logik identifizieren.
3. Relevante Logik in passende Notebooks migrieren.
4. Zielstruktur erstellen.
5. README auf Notebook-only umstellen.
6. ADR-002 für Notebook-only-Entscheidung erstellen.
7. ADR-004 für Execution-/Storage-Strategie erstellen.
8. `.gitignore` aktualisieren.
9. `.env.example` und `.env.cluster.example` erstellen.
10. Phase-0-QA dokumentieren.

### Deliverables

| Artefakt | Pfad |
|---|---|
| Zielstruktur | gesamtes Repo |
| README | `README.md` |
| Notebook-only ADR | `docs/decisions/ADR-002-notebook-only-implementation.md` |
| Storage ADR | `docs/decisions/ADR-004-execution-environment-and-storage-strategy.md` |
| QA Report | `docs/qa/phase0_qa_report.md` |

### Acceptance Criteria

| ID | Kriterium |
|---|---|
| P0-AC1 | Alle Zielordner existieren |
| P0-AC2 | Alle neun Notebooks existieren |
| P0-AC3 | README beschreibt Notebook-only-Struktur |
| P0-AC4 | Kein nützlicher Code wurde ungesichert gelöscht |
| P0-AC5 | `.gitignore` ignoriert Daten und Secrets |
| P0-AC6 | Keine falschen Cluster-Storage-Behauptungen |
| P0-AC7 | Phase 1 kann beginnen |

### Definition of Done

Phase 0 ist abgeschlossen, wenn die Zielstruktur steht, die Notebook-Reihenfolge klar ist und der Umbau dokumentiert wurde.

---

## 10. Phase 1 — Source Spike und Cluster Check

### Ziel

Quellen und Infrastruktur werden geprüft, bevor die eigentliche Pipeline implementiert wird.

### Notebook

```text
notebooks/01_source_spike_and_cluster_check.ipynb
```

### Aufgaben

1. Open-Meteo API für 1–2 Pilotstädte testen.
2. Wikipedia HTML für 1–2 Städte abrufen.
3. EEA-Datenquelle recherchieren und Beispielzugang dokumentieren.
4. FH Spark Cluster Smoke-Test dokumentieren.
5. HDFS-/Shared-Storage-Befund dokumentieren.
6. Entscheidung bestätigen: Spark `local[*]` für Parquet-produzierende Pipeline.

### Outputs

| Output | Ziel |
|---|---|
| Open-Meteo Sample | `data/bronze/open_meteo_raw/` |
| Wikipedia Sample HTML | `data/bronze/wikipedia_html/` |
| Cluster Check | `docs/qa/cluster_connectivity_check.md` |
| Data Source Notes | `docs/data_sources.md` |

### Acceptance Criteria

| ID | Kriterium |
|---|---|
| P1-AC1 | Jede Datenquelle wurde geprüft |
| P1-AC2 | Open-Meteo API ist grundsätzlich nutzbar |
| P1-AC3 | Wikipedia Scraping ist grundsätzlich möglich |
| P1-AC4 | EEA als Datei-/Batch-Quelle ist dokumentiert |
| P1-AC5 | FH Spark Cluster Befund ist dokumentiert |
| P1-AC6 | Storage-Strategie ist entschieden |

---

## 11. Phase 2 — City Reference Model

### Ziel

Ein stabiler City-Referenzdatensatz wird erstellt.

### Notebook

```text
notebooks/02_city_reference_model.ipynb
```

### Aufgaben

1. 8 Zielstädte definieren.
2. `city_id` erzeugen.
3. Koordinaten erfassen.
4. Länderkennung ergänzen.
5. Validierungen durchführen:
   - eindeutige `city_id`,
   - keine Nullwerte in Join-Schlüsseln,
   - gültige Koordinaten.
6. CSV und Parquet schreiben.

### Outputs

| Output | Ziel |
|---|---|
| City Reference CSV | `data/silver/city_reference.csv` |
| City Reference Parquet | `data/silver/city_reference.parquet` |

### Acceptance Criteria

| ID | Kriterium |
|---|---|
| P2-AC1 | Mindestens 8 Städte vorhanden |
| P2-AC2 | `city_id` eindeutig |
| P2-AC3 | Koordinaten vorhanden |
| P2-AC4 | Parquet ist lesbar |
| P2-AC5 | City Reference wird in Folge-Notebooks verwendet |

---

## 12. Phase 3 — EEA Batch Ingestion

### Ziel

Historische Luftqualitätsdaten werden als Datei-/Batch-Quelle verarbeitet.

### Notebook

```text
notebooks/03_eea_batch_ingestion.ipynb
```

### Aufgaben

1. EEA-Daten laden oder Beispiel-Datensatz dokumentiert einbinden.
2. Relevante Spalten identifizieren.
3. PM2.5, PM10, NO2 filtern.
4. Zeitstempel normalisieren.
5. Werte validieren.
6. Stadtzuordnung über `city_id` herstellen.
7. Tagesaggregation bilden.
8. Silver Parquet schreiben.

### Output

```text
data/silver/eea_city_daily.parquet
```

### Acceptance Criteria

| ID | Kriterium |
|---|---|
| P3-AC1 | Datei-/Batch-Quelle wird sichtbar verwendet |
| P3-AC2 | PM2.5, PM10, NO2 werden verarbeitet |
| P3-AC3 | Aggregation ist nachvollziehbar |
| P3-AC4 | Output liegt als Parquet vor |
| P3-AC5 | Datenqualität wird kommentiert |

---

## 13. Phase 4 — Wikipedia Web Scraping

### Ziel

Stadtmetadaten werden per Web Scraping gewonnen.

### Notebook

```text
notebooks/04_wikipedia_web_scraping.ipynb
```

### Aufgaben

1. Wikipedia URLs für Zielstädte definieren.
2. HTML mit `requests` abrufen.
3. Roh-HTML speichern.
4. Relevante Werte extrahieren:
   - Bevölkerung,
   - Fläche,
   - Bevölkerungsdichte.
5. Parser-Logik direkt im Notebook erklären.
6. Ausgabe als Parquet speichern.
7. Scraping-Limitations dokumentieren.

### Outputs

```text
data/bronze/wikipedia_html/*.html
data/silver/city_metadata.parquet
```

### Acceptance Criteria

| ID | Kriterium |
|---|---|
| P4-AC1 | Web Scraping ist sichtbar umgesetzt |
| P4-AC2 | Roh-HTML wird gespeichert |
| P4-AC3 | Metadaten enthalten `city_id` |
| P4-AC4 | Parser-Limitations sind dokumentiert |
| P4-AC5 | Output ist als Parquet lesbar |

---

## 14. Phase 5 — Open-Meteo REST API und Kafka Producer

### Ziel

Open-Meteo API-Daten werden abgefragt und über Kafka bereitgestellt.

### Notebook

```text
notebooks/05_open_meteo_api_and_kafka_producer.ipynb
```

### Aufgaben

1. Open-Meteo API Request definieren.
2. API-Daten für Zielstädte abrufen.
3. Internes Event-Schema definieren.
4. Events erzeugen:
   - `event_id`,
   - `schema_version`,
   - `city_id`,
   - `event_time_utc`,
   - `ingestion_time_utc`,
   - `pm2_5`,
   - `pm10`,
   - `no2`.
5. Kafka Producer direkt im Notebook implementieren.
6. Events an gruppenspezifisches Topic senden.
7. Consumer-Test dokumentieren.

### Kafka Topic

```text
bdeng_g1_air_quality_live
```

Gruppenkennung bei Bedarf anpassen.

### Acceptance Criteria

| ID | Kriterium |
|---|---|
| P5-AC1 | REST API wird real verwendet |
| P5-AC2 | Kafka Producer wird real verwendet |
| P5-AC3 | Events haben stabiles Schema |
| P5-AC4 | Topic ist gruppenspezifisch |
| P5-AC5 | Keine Secrets im Notebook |
| P5-AC6 | Consumer-Test ist dokumentiert |

---

## 15. Phase 6 — Spark Structured Streaming Kafka to Parquet

### Ziel

Spark liest Kafka-Daten, verarbeitet sie und speichert Ergebnisse als Parquet.

### Notebook

```text
notebooks/06_spark_structured_streaming_kafka_to_parquet.ipynb
```

### Standard Execution Mode

```text
SPARK_MASTER_URL=local[*]
```

### Aufgaben

1. SparkSession mit `local[*]` starten.
2. Kafka Topic mit Spark Structured Streaming lesen.
3. JSON mit explizitem Schema parsen.
4. Pollutant-Felder flatten.
5. Join mit `city_reference.parquet`.
6. Join mit `city_metadata.parquet`.
7. Daten transformieren oder aggregieren.
8. Checkpoint-Pfad setzen.
9. Parquet schreiben.
10. Parquet zurücklesen und prüfen.

### Outputs

```text
data/bronze/open_meteo_stream/
data/silver/open_meteo_city_hourly/
data/gold/live_air_quality_latest/
data/checkpoints/air_quality_live/
```

### Acceptance Criteria

| ID | Kriterium |
|---|---|
| P6-AC1 | Spark liest real aus Kafka |
| P6-AC2 | Spark verarbeitet Daten sichtbar |
| P6-AC3 | JSON Schema ist explizit |
| P6-AC4 | Join mit City-Daten funktioniert |
| P6-AC5 | Parquet Output ist lesbar |
| P6-AC6 | Cluster-Storage-Limitation wird dokumentiert |

---

## 16. Phase 7 — Gold Layer und Data Quality

### Ziel

Analysefertige Gold-Datensätze werden erzeugt.

### Notebook

```text
notebooks/07_gold_layer_and_data_quality.ipynb
```

### Aufgaben

1. Silver EEA laden.
2. City Metadata laden.
3. Stream Output laden.
4. Gold Tables erzeugen:
   - `city_air_quality_daily_summary.parquet`,
   - `pollutant_ranking_by_city.parquet`,
   - `city_context_air_quality.parquet`,
   - `live_air_quality_latest.parquet`.
5. Datenqualität prüfen:
   - Missing values,
   - duplicates,
   - plausible ranges,
   - schema consistency.
6. historische und aktuelle Daten sauber trennen.

### Acceptance Criteria

| ID | Kriterium |
|---|---|
| P7-AC1 | Gold Tables existieren |
| P7-AC2 | Gold Tables sind lesbar |
| P7-AC3 | Data Quality Checks sichtbar |
| P7-AC4 | historische und aktuelle Daten sind getrennt |
| P7-AC5 | Analyse kann auf Gold Layer aufbauen |

---

## 17. Phase 8 — Analysis, Visualization and Storytelling

### Ziel

Ergebnisse werden visualisiert und in eine verständliche Story überführt.

### Notebook

```text
notebooks/08_analysis_visualization_and_storytelling.ipynb
```

### Aufgaben

1. Gold Tables laden.
2. Kernvisualisierungen erstellen:
   - PM2.5 Ranking je Stadt,
   - PM10/NO2 Vergleich,
   - Zeitreihe für 2–3 Städte,
   - Boxplot oder Verteilung,
   - Bevölkerungsdichte vs Luftqualität als explorativer Kontext.
3. Abbildungen speichern.
4. Storyline formulieren.
5. Limitations explizit nennen.

### Outputs

```text
presentation/figures/*.png
presentation/final_storyline.md
presentation/presentation_outline.md
```

### Acceptance Criteria

| ID | Kriterium |
|---|---|
| P8-AC1 | 4–6 Visualisierungen vorhanden |
| P8-AC2 | Jede Visualisierung hat Aussage |
| P8-AC3 | Keine Kausalitätsüberdehnung |
| P8-AC4 | Storyline ist präsentierbar |
| P8-AC5 | Figuren sind gespeichert |

---

## 18. Final QA und Abgabe

### Ziel

Das Projekt wird auf Vollständigkeit, Konsistenz und Abgabereife geprüft.

### Aufgaben

1. README gegen tatsächlichen Stand prüfen.
2. Notebook-Reihenfolge prüfen.
3. Requirement-Mapping prüfen.
4. Cluster-Limitationen prüfen.
5. Keine Secrets im Repo.
6. Keine großen Daten im Repo.
7. Präsentation gegen Notebooks abgleichen.

### Deliverable

```text
docs/qa/final_readiness_check.md
```

### Acceptance Criteria

| ID | Kriterium |
|---|---|
| F-AC1 | Alle MUST-HAVE-Kriterien sind einem Notebook zugeordnet |
| F-AC2 | Alle Notebooks haben Purpose, Inputs, Outputs, Validation, Limitations |
| F-AC3 | Kafka und Spark sind real verwendet |
| F-AC4 | Parquet Outputs sind reproduzierbar |
| F-AC5 | README ist ehrlich |
| F-AC6 | Keine nicht belegten Cluster-Behauptungen |
| F-AC7 | Repo ist öffentlich teilbar |

---

## 19. `.env.example`

```env
EXECUTION_ENV=local_project

SPARK_MASTER_URL=local[*]
CLUSTER_SPARK_MASTER_URL=spark://<fh-spark-master-host>:7077

KAFKA_BOOTSTRAP_SERVERS=<kafka-host>:9092
KAFKA_TOPIC_AIR_QUALITY_LIVE=bdeng_gXX_air_quality_live

DATA_DIR=data
CHECKPOINT_DIR=data/checkpoints

PROJECT_TIMEZONE=UTC
LOG_LEVEL=INFO
```

---

## 20. `.env.cluster.example`

```env
EXECUTION_ENV=fh_cluster_shared_storage

SPARK_MASTER_URL=spark://<fh-spark-master-host>:7077
KAFKA_BOOTSTRAP_SERVERS=<fh-kafka-broker-host>:9092
KAFKA_TOPIC_AIR_QUALITY_LIVE=bdeng_gXX_air_quality_live

DATA_DIR=<confirmed_shared_storage_path>/euro-air-quality-pipeline/data
CHECKPOINT_DIR=<confirmed_shared_storage_path>/euro-air-quality-pipeline/checkpoints
```

---

## 21. `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]

# Environments
.venv/
venv/
.env
.env.*
!.env.example
!.env.cluster.example

# Jupyter
.ipynb_checkpoints/

# OS / IDE
.DS_Store
Thumbs.db
.vscode/
.idea/

# Logs / temp
*.log
tmp/
temp/

# Data outputs
data/**/*.parquet
data/**/*.csv
data/**/*.json
data/**/*.html
data/checkpoints/

# Keep folder structure
!data/**/.gitkeep
```

---

## 22. Kritische Bewertung

Notebook-only ist für diese LV vertretbar, weil die Aufgabenstellung explizit verlangt, jeden Schritt in Jupyter Notebooks zu dokumentieren und ein öffentliches GitHub-Repository zur Bereitstellung der Notebooks zu erstellen.

### Stärken

- sehr nahe an der Aufgabenstellung,
- klare Nachvollziehbarkeit,
- niedrigerer Software-Engineering-Overhead,
- gute Präsentierbarkeit,
- alle Technologien sichtbar in Notebooks.

### Schwächen

| Schwäche | Gegenmaßnahme |
|---|---|
| Notebooks können lang werden | klare Aufteilung 00–08 |
| Code ist weniger wiederverwendbar | Validierungszellen und strukturierte Sections |
| schwerer testbar als `src/` | Qualitätssicherung in Notebook-Abschnitten |
| Gefahr von Hidden State | Notebooks regelmäßig Kernel-restart-and-run-all testen |
| Cluster-Claims können ungenau werden | ADR-004 und Cluster QA |

### Professionelles Urteil

```text
Notebook-only ist weniger produktionsnah als ein modulares src/-Projekt.
Für diese konkrete LV ist es aber angemessen, solange die Notebooks sauber,
sequenziell, kritisch dokumentiert und ausführbar sind.
```

---

## 23. Minimaler Erfolgspfad

Wenn Zeit knapp wird, muss diese Kette funktionieren:

```text
00 Scope dokumentiert
01 Quellen und Cluster geprüft
02 city_reference.parquet erstellt
03 EEA Batch-Daten als Parquet
04 Wikipedia-Metadaten als Parquet
05 Open-Meteo Events nach Kafka
06 Spark liest Kafka und schreibt Parquet
07 Gold Tables erstellt
08 Visualisierungen und Storyline
README mappt alle MUST-HAVE-Kriterien
```

---

## 24. Final Decision

Das Projekt wird als **Notebook-only Big Data Engineering Project** umgesetzt.

Nicht verhandelbar:

- kein einzelnes Riesen-Notebook,
- keine Secrets im Repo,
- keine großen Daten im GitHub-Repo,
- keine falschen Cluster-Storage-Behauptungen,
- Kafka und Spark müssen real verwendet werden,
- jeder MUST-HAVE-Punkt muss in einem Notebook sichtbar nachweisbar sein.
