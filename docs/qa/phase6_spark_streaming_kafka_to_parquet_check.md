# QA-Bericht Phase 6: Spark Streaming von Kafka nach Parquet

## Ergebnis

Status: IMPLEMENTIERT, REDUZIERTER LOKALER STRUKTURTEST BESTANDEN, STRIKTER DOCKER-NACHWEIS BESTANDEN

## Modi

| Modus | Zweck | Nachweiswert |
| --- | --- | --- |
| `SPARK_KAFKA_MODE=kafka` | strikter Docker- oder FH-Lauf | erforderlicher finaler Nachweis |
| `SPARK_KAFKA_MODE=auto` | Kafka bevorzugen, erlaubten Fallback nutzen | Entwicklung |
| `SPARK_KAFKA_MODE=mock` | lokaler Spark-Dateistream | Spark-Mechanik ohne Kafka |
| `pandas_mock_no_pyspark` | reduzierter lokaler Strukturtest | weder Spark- noch Kafka-Nachweis |

## Implementierte Prüfungen

- explizites Ereignisschema
- Pflichtfelder, Zeitstempel und plausible Wertebereiche
- Reject-Ausgaben
- Deduplizierung über `event_id`
- Joins mit Stadtreferenz und Metadaten
- Bronze-, Silver- und Live-Snapshot-Parquet
- kontrollierter Abbruch im strikten Modus ohne PySpark

## Lokal geprüft

`192` Bronze-Zeilen, `192` Silver-Zeilen, `0` Rejects und `8` Live-Snapshot-Zeilen.

## Strikter Nachweis

Der Docker-Lauf gibt `selected_source_mode=kafka` und `spark_read_kafka_requirement_proven=True` aus. Ein zusätzlicher FH-Lauf bleibt möglich.

## FH-Nachweis

Der FH-Lauf wurde mit dem gruppenspezifischen Topic `bdeng_g1_air_quality_live` erfolgreich ausgeführt:

| Marker | Ergebnis |
| --- | --- |
| `SPARK_MASTER_URL` | `local[*]` |
| `SPARK_KAFKA_MODE` | `kafka` |
| Kafka-Broker | `172.29.16.101:9092` |
| `selected_source_mode` | `kafka` |
| `spark_read_kafka_requirement_proven` | `True` |
| Bronze-Zeilen | `16` |
| Silver-Zeilen | `16` |
| Reject-Zeilen | `0` |
| Neuester Snapshot | `8` Städte |

Die `16` Bronze- und Silver-Zeilen sind plausibel, weil das Topic Ereignisse aus mehreren Phase-5-Läufen enthält. Der neueste Snapshot reduziert sie korrekt auf eine Zeile pro Stadt.
