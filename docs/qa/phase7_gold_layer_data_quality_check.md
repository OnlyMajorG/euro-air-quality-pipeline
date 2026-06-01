# QA-Bericht Phase 7: Gold-Schicht und Datenqualität

## Ergebnis

Status: LOKAL BESTANDEN, ERWEITERTER EEA-API-ZEITRAUM FÜR FINALE AUSSAGEN ERFORDERLICH

Notebook `07_gold_layer_and_data_quality.ipynb` erzeugt fünf Gold-Parquet-Dateien und hält historische EEA-Daten und den Live-Snapshot getrennt.

## Lokal geprüft

| Prüfung | Ergebnis |
| --- | --- |
| Historische Tageswerte | `44` Zeilen |
| Schadstoff-Rangfolgen | `22` Zeilen |
| Stadtkontext | `22` Zeilen |
| Live-Snapshot | `8` Zeilen |
| Qualitätsbericht | `4` Zeilen |
| Doppelte Gold-Schlüssel | `0` |
| Live-Herkunft im strikten Docker-Lauf | `phase6_spark_stream_silver` |
| Historischer EEA-API-Zeitraum | `2` Tage |
| Mindestzeitraum für finale Aussagen | `365` Tage |
| Finale empirische Aussagen erlaubt | `False` |

Der kurze reale EEA-API-Zeitraum dient als reproduzierbarer Smoke-Test. Für finale empirische Aussagen muss Notebook `03` mit einem ausreichend langen EEA-API-Zeitraum ausgeführt werden.

## FH-Nachweis

Der FH-Lauf wurde nach dem erfolgreichen Kafka-zu-Spark-Lauf ausgeführt:

| Marker | Ergebnis |
| --- | --- |
| EEA-Herkunft | `real_eea_api_parquet` |
| Historische Tageswerte | `154` Zeilen |
| Historischer Zeitraum | `7` Tage |
| Mindestzeitraum für finale Aussagen | `365` Tage |
| `history_window_sufficient` | `False` |
| `final_analytical_claims_allowed` | `False` |
| Spark-Speicherprobe mit `local[*]` | bestanden |
| Live-Eingabe | `phase6_spark_stream_silver` |
| Gelesene Live-Ereignisse | `16` |
| Neuester Live-Snapshot | `8` Städte |
| Gold-Rangfolgen | `22` Zeilen |
| Gold-Stadtkontext | `22` Zeilen |
| Duplikate | `0` |
| Historisch oder live unplausible Werte | `0` |

Die Warnung zur optionalen Hadoop-GCS-Dateisystemklasse beeinflusst den Lauf nicht. Die Speicherprobe, Gold-Erzeugung und Readbacks wurden erfolgreich abgeschlossen. Die Probe belegt den lokalen FH-JupyterHub-Pfad mit `local[*]`, nicht einen gemeinsam sichtbaren Remote-Worker-Speicher.
