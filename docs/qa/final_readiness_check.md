# Abschließende Bereitschaftsprüfung

## Checkliste

- [x] Notebooks `00` bis `08` laufen lokal in Reihenfolge durch.
- [x] Keine Geheimnisse oder Zugangsdaten sind versioniert.
- [x] Laufzeitdaten unter `data/` bleiben ignoriert.
- [ ] Gruppenspezifisches Kafka-Topic ist in der nicht versionierten FH-`.env` eingetragen.
- [ ] Spark Structured Streaming liest in der FH-Umgebung aus Kafka und schreibt Parquet.
- [x] Der reduzierte lokale Strukturtest schreibt kompatible Parquet-Übergaben.
- [x] Gold-Datensätze und sechs Abbildungen werden lokal erzeugt.
- [x] Einschränkungen und nicht kausale Interpretation sind dokumentiert.
- [x] Die Storyline ist vollständig.

## Offene FH-Nachweise

1. Gruppenspezifisches Kafka-Topic konfigurieren.
2. Reale EEA-Daten für Notebook `03` bereitstellen.
3. Notebook `05` im strikten Kafka-Modus ausführen.
4. Notebook `06` im strikten Spark-Kafka-Modus ausführen.
5. Notebooks `07` und `08` erneut ausführen und die Abbildungen prüfen.

## Git-Hygiene

- Laufzeitdaten bleiben lokal.
- Unter `data/` werden nur `.gitkeep`-Dateien versioniert.
- Lokale `.env`-Dateien bleiben ignoriert.
- Das öffentliche Repository ist erreichbar: `https://github.com/OnlyMajorG/euro-air-quality-pipeline`.
