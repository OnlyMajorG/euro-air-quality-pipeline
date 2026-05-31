# ADR-003: Bronze-, Silver- und Gold-Schichten mit Parquet

## Status

Akzeptiert

## Entscheidung

Parquet ist das primäre Format für transformierte Daten. Bronze enthält quellnahe Daten, Silver normalisierte und verknüpfbare Daten, Gold analysebereite Ergebnisse. Erzeugte Dateien bleiben lokal unter `data/`.
