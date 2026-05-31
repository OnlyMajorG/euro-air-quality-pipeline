# QA-Bericht Phase 6: Spark Streaming von Kafka nach Parquet

## Ergebnis

Status: IMPLEMENTIERT, REDUZIERTER LOKALER STRUKTURTEST BESTANDEN, FH-NACHWEIS OFFEN

## Modi

| Modus | Zweck | Nachweiswert |
| --- | --- | --- |
| `SPARK_KAFKA_MODE=kafka` | strikter FH-Lauf | erforderlicher finaler Nachweis |
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

## Offener FH-Nachweis

Der finale Lauf muss `selected_source_mode=kafka` und `spark_read_kafka_requirement_proven=True` ausgeben.
