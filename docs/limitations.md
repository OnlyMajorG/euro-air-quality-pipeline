# Einschränkungen

- Die Datenmenge ist überschaubar. Der Schwerpunkt liegt auf Data Engineering, Kafka, Spark, Persistenz und Reproduzierbarkeit.
- Die Analyse ist deskriptiv und explorativ, nicht kausal.
- Wikipedia-Daten können sich ändern und sind keine amtliche Quelle.
- Stadtbezogene Luftqualitätsaggregate vereinfachen die Repräsentativität einzelner Messstationen.
- **Rom** hat im Zeitraum keine validierten PM2.5/PM10-Stationen. Die Lücke wird offen als `<NA>` ausgewiesen (nicht als `0` dargestellt, nicht interpoliert); Rom erscheint daher nur bei NO2 und bleibt aus den PM-Abbildungen und -Rangfolgen ausgeschlossen.
- Der explorative Zusammenhang zwischen **Bevölkerungsdichte und PM2.5 ist nicht robust**: über alle Städte r ≈ −0,23, ohne **Paris** dagegen r ≈ −0,95. Paris wird von Wikipedia als Kernkommune (~105 km²) geführt und ist mit den größer abgegrenzten anderen Städten nicht direkt vergleichbar (Modifiable Areal Unit Problem). Das Flag `density_comparable` markiert das transparent; Bevölkerungsdichte ist daher kein Erklärungsfaktor.
- Der EEA-Standardzeitraum umfasst ein volles Jahr (365 Tage). Bei einem kürzeren Testlauf gelten die Aussagen in NB 09 ausschließlich für den geladenen Zeitraum (das Notebook weist den Zeitraum aus).
- Live-Werte aus Open-Meteo sind Modelldaten und bleiben methodisch von den gemessenen historischen EEA-Werten getrennt.
- Kafka liefert mindestens einmal. Deterministische `event_id`-Werte und Deduplizierung in Spark reduzieren Duplikate.
- Der FH-Pfad ist code-seitig vorbereitet; live getestet wurde der lokale Docker-Pfad.
