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

Alternativ steht ein lokales Docker-Compose-Setup bereit. Dort teilen sich Jupyter und Spark-Worker den eingebundenen Pfad `/workspace`; deshalb ist `ALLOW_SHARED_SPARK_STORAGE=true` zulässig. Details stehen in `docs/docker_setup.md`.

Notebook `07` bietet dafür den optionalen Schalter:

```env
RUN_PHASE7_SPARK_STORAGE_PROBE=true
```

Vor dem FH-Lauf die nicht versionierte `.env` aus `.env.cluster.example` ableiten, Platzhalter ersetzen und Notebook `00` mit `PROJECT_EXECUTION_MODE=fh` ausführen. Die Erreichbarkeitsprüfung liegt vollständig im Notebook.

Notebook `03` verwendet in der FH `EEA_BRONZE_STORAGE_MODE=parquet`. PostgreSQL ist dort nicht erforderlich. Ein Docker-Lauf exportiert automatisch `data/bronze/eea/eea_observation.parquet`; alternativ kann die FH diese Datei mit `EEA_RUN_API_FETCH=true` selbst aus der EEA API erzeugen.

Notebook `05` begrenzt den Kafka-Nachweis mit `KAFKA_CONNECTION_TIMEOUT_SECONDS` und `KAFKA_OPERATION_TIMEOUT_MS`. Die Ausgaben `kafka_phase=tcp_preflight`, `producer_metadata`, `producer_send`, `consumer_create_after_send` und `consumer_poll` zeigen, in welcher Netzwerkphase eine FH-Konfiguration scheitert.

Wenn eine ältere Notebook-Ausführung bereits in der Kafka-Zelle hängt, brechen Sie den Kernel-Lauf einmal ab und starten den Kernel nach dem Aktualisieren von Notebook `05` neu. Führen Sie anschließend alle Zellen bis einschließlich der Definition von `publish_and_consume_kafka()` erneut aus. Die aktuelle Version erstellt den Smoke-Test-Consumer erst nach dem Senden und verwendet keine Vorab-Offset-Initialisierung. Bleibt der Lauf bei `tcp_preflight`, ist der konfigurierte Broker-Port aus dem JupyterHub nicht erreichbar. Scheitert er nach `producer_metadata`, muss zusätzlich der vom Broker beworbene advertised listener geprüft werden.
