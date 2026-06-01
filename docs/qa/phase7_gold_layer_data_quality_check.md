# QA-Bericht Phase 7: Gold-Schicht und Datenqualität

## Ergebnis

Status: LOKAL BESTANDEN, REALE EEA-DATEN FÜR FINALE AUSSAGEN ERFORDERLICH

Notebook `07_gold_layer_and_data_quality.ipynb` erzeugt fünf Gold-Parquet-Dateien und hält historische EEA-Daten und den Live-Snapshot getrennt.

## Lokal geprüft

| Prüfung | Ergebnis |
| --- | --- |
| Historische Tageswerte | `720` Zeilen |
| Schadstoff-Rangfolgen | `24` Zeilen |
| Stadtkontext | `24` Zeilen |
| Live-Snapshot | `8` Zeilen |
| Qualitätsbericht | `4` Zeilen |
| Doppelte Gold-Schlüssel | `0` |
| Live-Herkunft im strikten Docker-Lauf | `phase6_spark_stream_silver` |
| Finale empirische Aussagen erlaubt | `False` |
