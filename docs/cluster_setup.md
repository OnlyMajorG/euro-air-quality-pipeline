# FH-Cluster-Konfiguration

## Annahmen

Die FH-Umgebung kann VPN-Zugriff, JupyterHub, eine Spark-Master-URL und einen Kafka-Broker erfordern.
Zugangsdaten und private Hostnamen dürfen nicht versioniert werden.

## Vorgehen

1. Die nicht versionierte `.env` aus `.env.cluster.example` ableiten und die FH-Werte eintragen
   (`KAFKA_BOOTSTRAP_SERVERS`, gruppenspezifisches `KAFKA_TOPIC_AIR_QUALITY_LIVE`).
2. Notebook `00` ausführen. Bei `EXECUTION_ENV=fh_jupyterhub` prüft es nur die Erreichbarkeit des
   FH-Kafka (kein Docker).
3. Notebooks `01`–`09` im FH-Kernel ausführen, `10` zum Aufräumen.

## Entscheidungen für die FH

- **Spark:** `SPARK_MASTER_URL=local[*]` — Spark läuft im Notebook-Prozess, da kein gemeinsamer
  Cluster-Storage für entfernte Worker bestätigt ist. Der Kafka-Nachweis (Lesen aus dem FH-Broker)
  bleibt davon unberührt.
- **EEA-Bronze:** `EEA_BRONZE_STORAGE_MODE=parquet`, da die FH kein PostgreSQL hat. Notebook `04`
  erzeugt `data/bronze/eea/eea_observation.parquet` direkt aus der EEA-API.
- **Kafka-Connector:** `SPARK_KAFKA_CONNECTOR_PACKAGE` leer lassen, wenn der Connector im FH-Kernel
  bereits vorhanden ist.

Der EEA-Default `[2025-01-01, 2026-01-01)` umfasst 365 Tage. Für einen kürzeren Testlauf `EEA_DATE_END`
näher an `EEA_DATE_START` setzen.
