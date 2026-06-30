# Präsentationsstruktur

## Ziel: maximal 10 Minuten

| Zeit | Inhalt | Evidenz |
| --- | --- | --- |
| 0:00-0:45 | Leitfrage, Umfang und Hypothesen | Notebook `00`, Storyline |
| 0:45-1:45 | Drei Datenquellen | README, Datenflussdiagramm |
| 1:45-3:00 | Bronze, Silver, Gold, Kafka und Spark | Architekturdiagramm, Notebooks `04`–`07` |
| 3:00-4:00 | Datenqualität und Aussagegrenzen | Notebook `08` |
| 4:00-5:00 | PM2.5-Rangfolge | `pm25_city_ranking.png` |
| 5:00-6:00 | Schadstoffvergleich | `pollutant_comparison.png` |
| 6:00-7:00 | Zeitreihe und Verteilung | `selected_city_timeseries.png`, `pollutant_distribution.png` |
| 7:00-8:00 | Bevölkerungsdichte als explorativer Kontext | `density_vs_air_quality.png` |
| 8:00-8:45 | Getrennte Live-Momentaufnahme | `live_air_quality_snapshot.png` |
| 8:45-10:00 | Einschränkungen und Fazit | Storyline, README |

## Sprechregeln

- Immer „im betrachteten Datensatz“ formulieren.
- Zeitraum, Quelle und Beobachtungsanzahl nennen.
- Live-Werte nie als historischen Trend interpretieren.
- Korrelation nie als Kausalität darstellen.
- Auf echten, validierten EEA-Messdaten aufsetzen (kein Sample-Fallback) und die Reproduzierbarkeit betonen.
- Den Live-vs-EEA-Median-Vergleich nur als explorative Lage-Einordnung darstellen (Modellwert vs. Messdaten, kein Trend- oder WHO-Bezug).
