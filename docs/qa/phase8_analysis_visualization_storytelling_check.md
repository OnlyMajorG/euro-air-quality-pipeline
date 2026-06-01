# QA-Bericht Phase 8: Analyse, Visualisierung und Storytelling

## Ergebnis

Status: LOKAL BESTANDEN, ERWEITERTER EEA-API-ZEITRAUM FÜR FINALE AUSSAGEN ERFORDERLICH

Notebook `08_analysis_visualization_and_storytelling.ipynb` verwendet ausschließlich Gold-Datensätze und erzeugt eine deutschsprachige Ergebnisgeschichte.

## Methodische Regeln

- historische EEA-Werte und Open-Meteo-Live-Werte bleiben getrennt
- PM2.5, PM10 und NO2 werden getrennt interpretiert
- Ausreißer bleiben in Boxplots sichtbar
- Bevölkerungsdichte wird explorativ und nicht kausal eingeordnet
- kurze reale EEA-API-Zeiträume demonstrieren nur die Mechanik
- Städte ohne Messwerte für einen Schadstoff werden transparent ausgewiesen
- Boxplots mit wenigen Tageswerten werden ausdrücklich als Smoke-Test-Visualisierung behandelt

## Erzeugte Abbildungen

`pm25_city_ranking.png`, `pollutant_comparison.png`, `selected_city_timeseries.png`, `pollutant_distribution.png`, `density_vs_air_quality.png`, `live_air_quality_snapshot.png`

## Lokale Marker

```text
Historischer EEA-API-Zeitraum: 2 Tage
Mindestzeitraum für finale Aussagen: 365 Tage
Stadt ohne PM2.5-Messwerte im geprüften Zeitraum: Rome
Live-Eingabemodus im strikten Docker-Lauf: phase6_spark_stream_silver
Finale historische Aussagen zulässig: False
```

## FH-Nachweis

Notebook `08` wurde nach dem erfolgreichen FH-Gold-Lauf ausgeführt:

| Marker | Ergebnis |
| --- | --- |
| EEA-Herkunft | `eea_downloads_api_parquet` |
| EEA-Datenstatus | `real_eea_api_parquet` |
| Historischer Zeitraum | `2025-01-01` bis `2025-01-07` |
| Historische Tageswerte | `154` |
| Städte | `8` |
| Schadstoffe | `no2`, `pm10`, `pm2_5` |
| Live-Eingabe | `phase6_spark_stream_silver` |
| Live-Snapshot-Zeitpunkt | `2026-06-01 23:00:00+00:00` |
| Stadt ohne PM2.5-Messwerte | `Rome` |
| PM2.5-Ranking | `7` Städte |
| Explorative Spearman-Rangkorrelation | `rho=-0.393`, `n=7` Städte |
| Erzeugte Abbildungen | `6` |
| Historische und Live-Daten getrennt | `PASS` |
| `final_analytical_claims_allowed` | `False` |

Der FH-Lauf ist technisch bestanden. Die Rangkorrelation und die Diagramme dienen bei sieben historischen Tagen ausschließlich als Smoke-Test und explorative Darstellung. Finale fachliche Aussagen erfordern weiterhin mindestens `365` historische Tage.
