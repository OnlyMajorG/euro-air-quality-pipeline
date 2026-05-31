# ADR-002: Notebook-basierte Umsetzung

## Status

Akzeptiert

## Kontext

Die Arbeitsschritte sollen nachvollziehbar in Jupyter Notebooks dokumentiert werden.

## Entscheidung

Die Implementierungslogik liegt in geordneten Notebooks. Validierungen stehen direkt in den Notebooks und in QA-Dokumenten. Separate `src/`- und `tests/`-Ordner sind nicht die primäre Umsetzungsebene.
