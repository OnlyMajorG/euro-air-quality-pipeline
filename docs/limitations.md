# Einschränkungen

- Die Datenmenge ist überschaubar. Der Schwerpunkt liegt auf Data Engineering, Kafka, Spark, Persistenz und Reproduzierbarkeit.
- Die Analyse ist deskriptiv und explorativ, nicht kausal.
- Wikipedia-Daten können sich ändern und sind keine amtliche Quelle.
- Stadtbezogene Luftqualitätsaggregate vereinfachen die Repräsentativität einzelner Messstationen.
- Der EEA-Standardzeitraum umfasst ein volles Jahr (365 Tage). Bei einem kürzeren Testlauf gelten die Aussagen in NB 09 ausschließlich für den geladenen Zeitraum (das Notebook weist den Zeitraum aus).
- Live-Werte aus Open-Meteo sind Modelldaten und bleiben methodisch von den gemessenen historischen EEA-Werten getrennt.
- Kafka liefert mindestens einmal. Deterministische `event_id`-Werte und Deduplizierung in Spark reduzieren Duplikate.
- Der FH-Pfad ist code-seitig vorbereitet; live getestet wurde der lokale Docker-Pfad.
