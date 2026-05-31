# Cluster-Konfiguration

## Annahmen

Die FH-Umgebung kann VPN-Zugriff, JupyterHub, eine Spark-Master-URL und einen Kafka-Broker erfordern. Zugangsdaten und private Hostnamen dürfen nicht versioniert werden.

## Bekannte Erkenntnisse

- Der Spark-Master war erreichbar.
- Eine grundlegende Spark-Berechnung war möglich.
- Gemeinsamer Speicher für Spark-Worker ist noch nicht bestätigt.
- Lokale Jupyter-Pfade sind nicht automatisch für Cluster-Executors sichtbar.

## Entscheidung

Für reproduzierbare lokale Parquet-Ausgaben wird `SPARK_MASTER_URL=local[*]` verwendet. Der FH-Cluster dient für den strikten Kafka-zu-Spark-Nachweis. Gemeinsamer Cluster-Speicher darf erst nach einem erfolgreichen Schreib- und Lesetest behauptet werden.

Notebook `07` bietet dafür den optionalen Schalter:

```env
RUN_PHASE7_SPARK_STORAGE_PROBE=true
```
