# Audit der früheren Repository-Struktur

## Ausgangslage

Das Repository enthielt zuvor `src/`-Module, pytest-basierte Tests, ältere Notebook-Namen und historische Dokumentationsordner.

## Übernommene Logik

| Frühere Logik | Heutiger Ort |
| --- | --- |
| Stadtreferenz und Validierung | `notebooks/02_city_reference_model.ipynb` |
| Stationszuordnung und EEA-Normalisierung | `notebooks/03_eea_batch_ingestion.ipynb` |
| Datenqualitätsprüfungen | Validierungsabschnitte der Notebooks |
| Kafka-, Spark-, Wikipedia- und Gold-Logik | Notebooks `04` bis `08` |

## Entscheidung

Die nützliche Logik wurde vor der Entfernung der alten Struktur in die Notebooks übertragen oder dokumentiert.
