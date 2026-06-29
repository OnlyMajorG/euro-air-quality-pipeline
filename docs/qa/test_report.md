# Testbericht — End-to-End-Lauf

Vollständiger Durchlauf der Pipeline (Notebooks `00`–`10`) im lokalen Docker-Pfad mit dem
**365-Tage-Standardzeitraum** (`2025-01-01` bis `2026-01-01`). Jedes Notebook wurde mit
`jupyter nbconvert --execute` ausgeführt; Notebook `07` lief im Docker-Jupyter-Container
(Spark 3.5.7, Java 17, Kafka-Connector).

| NB | Ergebnis |
| --- | --- |
| `00` Infrastruktur | `docker compose up`; Ports Kafka/Spark/PostgreSQL/Jupyter erreichbar |
| `01` Scope | Anforderungs-Mapping vollständig |
| `02` Quellen-Check | Open-Meteo, Wikipedia, EEA-API und Kafka/Spark erreichbar |
| `03` Stadtreferenz | 8 Städte, Invarianten bestanden |
| `04` EEA (PostgreSQL) | Bronze nach PostgreSQL, **7 938 Silver-Tageszeilen über 365 Tage** |
| `04` EEA (Parquet, FH-Pfad) | separat geprüft: Bronze-Parquet + Silver identisch erzeugt |
| `05` Wikipedia | **8 von 8 Städten `parse_status=success`** |
| `06` Open-Meteo + Kafka | **192 Events** (8 Städte × 24 h) an Topic `air_quality_live` |
| `07` Spark Streaming | `spark_read_kafka_requirement_proven=True`, **192 Silver-Zeilen** |
| `08` Gold | 6 Tabellen: daily 7 938, ranking 22, context 22, live 8, **live_vs_historical_median 24** (22 `comparable` / 2 `no_historical_reference`), quality 5 Zeilen (Spalte `coverage_days`; Live-Snapshot und Vergleich `<NA>`); Struktur-Assertions bestanden |
| `09` Storytelling | 7 Abbildungen; Geltungs-Hinweis „365 Tage"; Rom-Lücke (PM2.5/PM10) als `<NA>` ausgewiesen; Dichte-Korrelation mit und ohne Paris ausgewiesen; Live-vs-EEA-Median-Vergleich als explorative Abbildung 7 |
| `10` Reset | löscht `data/`-Dateien und fährt die Infrastruktur herunter |

## Belege für die Datenqualität

- **EEA-Filter** (`Validity > 0`, `Verification > 0`, `Value >= 0`) greifen: nur formal geprüfte
  Messungen fließen in die Tagesaggregation. Rom hat im Zeitraum keine validierten PM-Werte und wird
  in den PM-Rangfolgen offen als fehlend ausgewiesen (keine erfundenen Werte).
- **Kafka → Spark** ist real nachgewiesen: 192 produzierte Events werden von Spark aus dem Topic
  gelesen, gegen den Event-Vertrag (`schema_version`, `source`, Plausibilitätsbereiche) validiert,
  per `dropDuplicates(["event_id"])` dedupliziert und mit der Stadtreferenz verknüpft.
- **Storytelling (NB 09)** bleibt deskriptiv: Mittelwerte mit Standardabweichung und Beobachtungszahl
  (`n`), sichtbare Saisonalität im Jahresverlauf, strikte Trennung von EEA-historisch und
  Open-Meteo-live, Bevölkerungsdichte nur explorativ.
- **Robustheit offengelegt:** Der Zusammenhang Dichte ↔ PM2.5 ist nicht robust (r ≈ −0,23 über alle
  Städte, ≈ −0,95 ohne Paris). Paris ist als Kernkommune nicht direkt vergleichbar (Modifiable Areal
  Unit Problem), wird über `density_comparable` markiert und im Streudiagramm gesondert dargestellt;
  die Korrelation wird mit und ohne Paris ausgewiesen.
- **Live-vs-Median-Vergleich (explorativ):** `live_vs_historical_median` stellt den Open-Meteo-Live-Wert
  dem historischen EEA-Median 2025 gegenüber (Quartile als Streubreite). Die Quellen werden ausdrücklich
  als Modellwert vs. Messdaten gekennzeichnet; kein WHO-Jahres- oder Kausalbezug. Wo keine historische
  Referenz existiert (Rom PM2.5/PM10), bleibt der Vergleich offen (`no_historical_reference`).

## Bekannte Grenzen des Tests

- Der **FH-JupyterHub-Pfad** wurde code-seitig geprüft, aber nicht live ausgeführt (Cluster von der
  Testumgebung nicht erreichbar). Der lokale Docker-Pfad ist vollständig verifiziert.
