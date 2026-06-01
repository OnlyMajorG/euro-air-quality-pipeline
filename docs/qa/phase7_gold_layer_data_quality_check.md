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
