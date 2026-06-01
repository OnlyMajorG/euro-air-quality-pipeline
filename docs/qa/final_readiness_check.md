# Abschließende Bereitschaftsprüfung

## Checkliste

- [x] Notebooks `00` bis `08` laufen lokal in Reihenfolge durch.
- [x] Keine Geheimnisse oder Zugangsdaten sind versioniert.
- [x] Laufzeitdaten unter `data/` bleiben ignoriert.
- [ ] Gruppenspezifisches Kafka-Topic ist in der nicht versionierten FH-`.env` eingetragen.
- [x] Spark Structured Streaming liest im Docker-Setup aus Kafka und schreibt Parquet.
- [x] Der reduzierte lokale Strukturtest schreibt kompatible Parquet-Übergaben.
- [x] Gold-Datensätze und sechs Abbildungen werden lokal erzeugt.
- [x] Einschränkungen und nicht kausale Interpretation sind dokumentiert.
- [x] Die Storyline ist vollständig.

## Nachgewiesene Docker-Infrastruktur

Der lokale strikte Docker-Nachweis ist unter `docs/qa/docker_setup_verification.md` dokumentiert.

## Offene FH- und Daten-Nachweise

1. Für einen zusätzlichen FH-Lauf die FH-Endpunkte und ein gruppenspezifisches Kafka-Topic konfigurieren.
2. Notebook `03` mit dem neuen Jahresdefault `[2025-01-01, 2026-01-01)` und `EEA_RUN_API_FETCH=true` ausführen.
3. Prüfen, dass nach EEA-Validitätsfiltern tatsächlich mindestens `365` unterschiedliche historische Tage verbleiben.
4. Notebooks `07` und `08` mit dem Jahres-Parquet erneut ausführen und die Abbildungen prüfen.

## Git-Hygiene

- Laufzeitdaten bleiben lokal.
- Unter `data/` werden nur `.gitkeep`-Dateien versioniert.
- Lokale `.env`-Dateien bleiben ignoriert.
- Das öffentliche Repository ist erreichbar: `https://github.com/OnlyMajorG/euro-air-quality-pipeline`.
