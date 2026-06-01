# Einschränkungen

- Die Datenmenge ist überschaubar. Der Schwerpunkt liegt auf Data Engineering, Kafka, Spark, Persistenz und Reproduzierbarkeit.
- Die Analyse ist deskriptiv und explorativ, nicht kausal.
- Wikipedia-Daten können sich ändern und sind keine amtliche Quelle.
- Gemeinsamer FH-Cluster-Speicher darf erst nach einem erfolgreichen Test behauptet werden.
- Stadtbezogene Luftqualitätsaggregate vereinfachen die Repräsentativität einzelner Messstationen.
- Kontrollierte EEA-Samples demonstrieren Verarbeitungsschritte, erlauben aber keine finalen empirischen Aussagen.
- Lokale Kafka-Mocks belegen nur die Mechanik. Der Kafka-Nachweis erfordert einen strikten Docker- oder FH-Lauf.
- Der lokale Spark-Dateistream ist kein Kafka-Nachweis.
- Der Modus `pandas_mock_no_pyspark` ist weder ein Spark- noch ein Kafka-Nachweis.
- Live-Werte aus Open-Meteo bleiben methodisch von historischen EEA-Werten getrennt.
- Kafka liefert mindestens einmal. Deterministische `event_id`-Werte und Deduplizierung reduzieren Duplikate.
- MongoDB und eine reine Wien-Wetteranalyse gehören bewusst nicht zum eingefrorenen Projektumfang.
