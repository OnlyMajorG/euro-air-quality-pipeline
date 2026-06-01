# QA-Bericht Phase 8: Analyse, Visualisierung und Storytelling

## Ergebnis

Status: LOKAL BESTANDEN, REALE EEA-DATEN FÜR FINALE AUSSAGEN ERFORDERLICH

Notebook `08_analysis_visualization_and_storytelling.ipynb` verwendet ausschließlich Gold-Datensätze und erzeugt eine deutschsprachige Ergebnisgeschichte.

## Methodische Regeln

- historische EEA-Werte und Open-Meteo-Live-Werte bleiben getrennt
- PM2.5, PM10 und NO2 werden getrennt interpretiert
- Ausreißer bleiben in Boxplots sichtbar
- Bevölkerungsdichte wird explorativ und nicht kausal eingeordnet
- kontrollierte Samples demonstrieren nur die Mechanik

## Erzeugte Abbildungen

`pm25_city_ranking.png`, `pollutant_comparison.png`, `selected_city_timeseries.png`, `pollutant_distribution.png`, `density_vs_air_quality.png`, `live_air_quality_snapshot.png`

## Lokale Marker

```text
EEA-Sample-Fallback aktiv: True
Live-Eingabemodus im strikten Docker-Lauf: phase6_spark_stream_silver
Finale historische Aussagen zulässig: False
```
