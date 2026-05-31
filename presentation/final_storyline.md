# Finale Ergebnisgeschichte

## Titel

**Von heterogenen Datenquellen zur nachvollziehbaren Luftqualitätsanalyse europäischer Städte**

## Leitfrage

Welche Luftqualitätsmuster zeigen ausgewählte europäische Städte im historischen Vergleich, und wie lassen sich diese Unterschiede durch urbane Kontextdaten vorsichtig einordnen?

## Argumentationslinie

1. Das Projekt verbindet historische EEA-Dateien, Wikipedia-Web-Scraping und die Open-Meteo-REST-API.
2. Open-Meteo-Ereignisse werden als flache JSON-Nachrichten modelliert und über Kafka für Spark bereitgestellt.
3. Bronze-, Silver- und Gold-Schichten machen Herkunft, Bereinigung und Analysegrenzen nachvollziehbar.
4. Die historischen Gold-Daten beantworten deskriptive Fragen zu PM2.5, PM10 und NO2.
5. Wikipedia-Metadaten ergänzen explorativen Stadtkontext. Bevölkerungsdichte ist kein kausaler Erklärungsfaktor.
6. Die Open-Meteo-Live-Abbildung bleibt eine getrennte Momentaufnahme.

## Hypothesen

- **H1:** Die mittleren historischen PM2.5-Werte unterscheiden sich zwischen den betrachteten Städten.
- **H2:** Die Rangfolge der Städte ist schadstoffabhängig.
- **H3:** Bevölkerungsdichte kann explorativ mit Luftqualitätskennzahlen zusammenhängen, beweist aber keine Ursache.
- **H4:** Live-Daten ergänzen den technischen Datenfluss, nicht die historische Aussage.

## Zulässige Aussagen

| Abbildung | Aussage |
| --- | --- |
| `pm25_city_ranking.png` | Im betrachteten Datensatz unterscheiden sich die mittleren PM2.5-Werte. |
| `pollutant_comparison.png` | Stadtmuster unterscheiden sich zwischen PM2.5, PM10 und NO2. |
| `selected_city_timeseries.png` | Die Tageswerte zeigen kurzfristige Schwankungen ohne langfristige Trendbehauptung. |
| `pollutant_distribution.png` | Median und Streuung ergänzen Mittelwert-Rangfolgen. |
| `density_vs_air_quality.png` | Der Zusammenhang zwischen Dichte und PM2.5 ist ausschließlich explorativ. |
| `live_air_quality_snapshot.png` | Open-Meteo zeigt eine Momentaufnahme, keine langfristige Rangfolge. |

## Lokaler Datenstatus

Der lokale Lauf verwendet für EEA `controlled_sample_fallback` und für den Live-Pfad `phase6_pandas_mock_no_pyspark_silver`. Finale empirische Aussagen erfordern reale EEA-Daten und den strikten FH-Kafka-zu-Spark-Lauf.
