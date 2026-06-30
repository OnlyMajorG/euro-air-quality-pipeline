# Projekt-Briefing für die Präsentationserstellung

> **Zweck dieses Dokuments:** vollständige, eigenständige Beschreibung des Projekts und
> seiner Absichten, damit eine Präsentation erstellt werden kann, **ohne** den Code oder
> frühere Gespräche zu kennen. Alle Zahlen stammen aus einem verifizierten End-to-End-Lauf.

---

## 0. Auftrag (was zu erstellen ist)

Erstelle eine **Abschlusspräsentation** für ein universitäres Big-Data-Engineering-Projekt.

**Harte Vorgaben (Prüfungsordnung):**
- Format: **PDF**.
- **Maximal 10 Inhaltsfolien** (Titelfolie zählt nicht mit).
- Muss enthalten: **Namen der drei Gruppenmitglieder** und **Link zum öffentlichen GitHub-Repo**.
- **Nur Findings**: Die Präsentation soll die *Ergebnisse* vermitteln, **keine** Code- oder
  Implementierungsdetails. Schwerpunkt auf Diagramme/Grafiken. Klar, prägnant, ansprechend.

**Platzhalter, die noch zu füllen sind:**
- Gruppennamen: `[Name 1] · [Name 2] · [Name 3]`
- Repo-Link: `https://github.com/OnlyMajorG/euro-air-quality-pipeline` (muss öffentlich sein).

**Verfügbare Assets (fertige Grafiken):** im Ordner `presentation/figures/` (Details in Abschnitt 6).

---

## 1. Worum geht es? (Projektzweck in zwei Ebenen)

Das Projekt hat **zwei Ebenen**, die klar zu trennen sind:

1. **Data-Engineering (das eigentliche Lernziel):** Daten aus **drei verschiedenartigen
   Quellen** beschaffen, über **Apache Kafka** als zentralen Broker transportieren, mit
   **Apache Spark** verarbeiten und in einer **Medallion-Architektur** (Bronze → Silver →
   Gold) persistieren. Das ist der technische Kern und erfüllt die Pflichtkriterien.
2. **Die Geschichte (Findings):** Damit die Daten greifbar werden, beantworten wir die Frage:
   **Wie sauber ist die Luft in acht europäischen Hauptstädten – gemessen am gesundheitlichen
   Maßstab der WHO?**

Laut Aufgabenstellung zählt in der *Präsentation* die zweite Ebene (Findings). Die Technik
darf als kurzer Kontext (eine Folie) vorkommen, mehr nicht.

### Kernbotschaft (ein Satz)
**Keine der acht Städte hält die WHO-Richtwerte für NO2 ein, und die Rangfolge der Belastung
hängt vom Schadstoff ab – wir zeigen das ehrlich, deskriptiv und ohne die Daten schönzurechnen.**

---

## 2. Das Thema und die Daten

- **Untersuchungsobjekt:** Luftqualität, gemessen an drei Schadstoffen – **PM2.5** (Feinstaub
  < 2,5 µm), **PM10** (< 10 µm), **NO2** (Stickstoffdioxid).
- **Acht Städte:** Wien, Berlin, Paris, Madrid, Rom, Amsterdam, Warschau, Prag.
- **Zeitraum:** volles Kalenderjahr **2025** (01.01.–31.12.), Tagesauflösung.
- **Einheit:** µg/m³ (Mikrogramm pro Kubikmeter Luft).

### Die drei Datenquellen (Pflicht: drei verschiedene Arten)
| Quelle | Art | Liefert |
| --- | --- | --- |
| **EEA Air Quality Downloads** | Datei/Datenbank (Parquet → PostgreSQL) | Gemessene, validierte Stundenwerte (historisch) |
| **Wikipedia** | Web-Scraping (HTML) | Städtische Metadaten: Einwohner, Fläche, Bevölkerungsdichte |
| **Open-Meteo Air Quality API** | REST-API (JSON) | Aktuelle Live-Modellwerte (Echtzeit-Nachweis) |

### Die Pipeline (technischer Kontext, knapp halten)
`EEA · Wikipedia · Open-Meteo → Kafka (Topic) → Spark (Structured Streaming) → Bronze/Silver/Gold (Parquet/PostgreSQL) → Analyse`
- **Kafka** transportiert mindestens eine Quelle (Open-Meteo-Live) als Strom.
- **Spark** liest diesen Strom aus dem Kafka-Topic und verarbeitet ihn (Pflichtkriterium erfüllt).
- **Medallion:** Bronze = roh, Silver = bereinigt/vereinheitlicht, Gold = analysebereit.

---

## 3. Der Maßstab: WHO-2021-Richtwerte

Wir bewerten die Stadt-Jahresmittel anhand der **WHO-2021-Jahres-Richtwerte** für gesunde Luft:

| Schadstoff | WHO-2021-Jahresrichtwert |
| --- | --- |
| PM2.5 | **5 µg/m³** |
| PM10 | **15 µg/m³** |
| NO2 | **10 µg/m³** |

**Wichtige Einordnung (immer ehrlich kommunizieren):** Das sind **Gesundheits-
Orientierungswerte der WHO**, *keine* gesetzlichen EU-Grenzwerte (die EU-Grenze für NO2 liegt
z. B. bei 40 µg/m³). Aussage also: „über dem, was die WHO als gesund ansieht" – **nicht** „illegal".

---

## 4. Die zentralen Befunde (mit exakten Zahlen)

1. **Alle Städte überschreiten den WHO-NO2-Richtwert.** NO2-Jahresmittel zwischen 15,3 und
   25,0 µg/m³ – also das 1,5- bis 2,5-Fache des WHO-Werts (10).
2. **PM2.5 überschreitet überall den WHO-Wert (5).** Höchste Werte in Warschau und Prag,
   niedrigste in Madrid/Amsterdam/Wien.
3. **Die Rangfolge hängt vom Schadstoff ab.** Eine Stadt kann bei NO2 vorn liegen, bei PM2.5
   aber nicht – darum gibt es **keine** pauschale „Luftqualitäts-Rangliste". Grund: NO2 ist
   verkehrsgeprägt, PM stärker durch Heizung/Witterung bestimmt.
4. **Saisonalität:** PM-Werte sind im Winter höher (Heizen + Inversionswetterlagen halten
   Schadstoffe am Boden).
5. **Bevölkerungsdichte erklärt die Belastung nicht.** Der explorative Zusammenhang Dichte ↔ PM2.5
   ist **nicht robust**: r = −0,23 über alle Städte (n = 7), aber −0,95 ohne Paris (n = 6). Paris
   ist als Kernkommune (~105 km²) mit den anderen, größer abgegrenzten Städten **nicht direkt
   vergleichbar** (Modifiable Areal Unit Problem) und wird daher gesondert markiert.
6. **Live-Nachweis:** 192 aktuelle Werte (8 Städte × 24 h) flossen über Kafka → Spark – als
   Beleg der laufenden Pipeline, **getrennt** von der historischen Messanalyse.

---

## 5. Wissenschaftliche Ehrlichkeit (Pflicht-Botschaft, eigene Folie wert)

- **Deskriptiv, nicht kausal** – wir beschreiben Muster, behaupten keine Ursachen.
- **Keine pauschale Stadt-Rangliste** – jeder Schadstoff wird einzeln betrachtet.
- **Lücken bleiben Lücken** – **Rom** hat im Zeitraum keine validierten PM2.5/PM10-Werte; das
  wird **offen ausgewiesen, nicht interpoliert/aufgefüllt**.
- **Quellen sauber getrennt** – gemessene EEA-Historie vs. Open-Meteo-Live-Modellwerte werden
  nie vermischt; Live-Stundenwerte werden bewusst **nicht** gegen die WHO-*Jahres*werte gestellt.

---

## 6. Die fertigen Grafiken (in `presentation/figures/`)

Alle Grafiken sind vorhanden und enthalten bereits die WHO-Referenzlinien. Pro Grafik: was sie
zeigt und welcher Befund dazugehört.

1. **`pollutant_comparison.png`** — Gruppierte Balken je Stadt (blau = PM2.5, orange = PM10,
   grün = NO2) mit gestrichelten WHO-Linien (5/15/10). **Headline-Grafik:** Alle über WHO; Rom
   nur NO2 (PM fehlt → Lücke sichtbar). → Befund 1 & 3.
2. **`pm25_city_ranking.png`** — Horizontale Balken, PM2.5-Mittel je Stadt, Fehlerbalken
   (Standardabweichung), `n` = Zahl der Tageswerte, WHO-Linie bei 5. → Befund 2.
3. **`pollutant_distribution.png`** — Boxplots je Schadstoff mit WHO-Markern; Median überall
   über WHO; lange Oberschwänze = belastete Einzeltage. → Streuung/Ausreißer.
4. **`selected_city_timeseries.png`** — PM2.5-Tagesverlauf der datenreichsten Städte über das
   Jahr; Lücken bleiben sichtbar; Winter höher. → Befund 4 (Saisonalität).
5. **`density_vs_air_quality.png`** — Streudiagramm Bevölkerungsdichte (Wikipedia) vs. PM2.5
   (EEA); Paris als „nicht vergleichbar" gesondert markiert; r = −0,23 (alle, n = 7) vs. −0,95
   (ohne Paris, n = 6) → Zusammenhang nicht robust. → Befund 5.
6. **`live_air_quality_snapshot.png`** — Aktuelle Stundenwerte je Stadt aus Open-Meteo
   (Kafka → Spark). → Befund 6 (Live-Nachweis).

---

## 7. Empfohlene Foliengliederung (Titel + 10)

| # | Folie | Inhalt / Grafik |
| --- | --- | --- |
| – | **Titel** | Projekttitel, Leitfrage, Pipeline-Zeile, **Namen**, **Repo-Link** |
| 1 | Leitfrage & Maßstab | Forschungsfrage + WHO-Werte (Text) |
| 2 | Datengrundlage | 8 Städte · 365 Tage · 3 Schadstoffe · 2,35 Mio. Messungen · 3 Quellarten (Text) |
| 3 | Befund 1: Alle über WHO | `pollutant_comparison.png` |
| 4 | Befund 2: PM2.5-Rangfolge | `pm25_city_ranking.png` |
| 5 | Befund 3: Verteilung/Ausreißer | `pollutant_distribution.png` |
| 6 | Befund 4: Saisonalität | `selected_city_timeseries.png` |
| 7 | Befund 5: Dichte erklärt nichts | `density_vs_air_quality.png` |
| 8 | Befund 6: Live-Momentaufnahme | `live_air_quality_snapshot.png` |
| 9 | Einordnung | Was die Daten (nicht) sagen – die vier Ehrlichkeits-Prinzipien (Text) |
| 10 | Fazit | 3 Kernaussagen + Repo-Link (Text) |

**Drei Kernaussagen für Folie 10:**
1. Überall zu viel NO2 (15–25 statt 10 µg/m³).
2. Schadstoff schlägt Stadt – getrennt betrachten.
3. Kontext (Dichte) erklärt wenig.

---

## 8. Tonalität & Stil

- **Sachlich, ehrlich, wissenschaftlich** – Grenzen offen benennen wirkt stärker, nicht schwächer.
- **Diagramme im Mittelpunkt**, wenig Text pro Folie (Stichpunkte, keine Fließtexte).
- **Keine Übertreibung**, keine Kausalbehauptungen, keine erfundenen Werte.
- Sprache: Deutsch.

---

## 9. Faktencheck – exakte Zahlen (aus verifiziertem End-to-End-Lauf)

| Größe | Wert |
| --- | --- |
| Gemessene EEA-Stundenwerte (Bronze) | 2.352.005 |
| Tagesmittel (Silver/Gold) | 7.938 (365 Tage, 8 Städte, 3 Schadstoffe) |
| **NO2-Jahresmittel** (µg/m³) | Rom 25,0 · Paris 23,0 · Prag 22,7 · Warschau 22,6 · Madrid 22,5 · Amsterdam 18,1 · Wien 16,0 · Berlin 15,3 |
| **PM2.5-Jahresmittel** (µg/m³) | Warschau 14,7 · Prag 14,5 · Berlin 11,4 · Paris 11,1 · Wien 9,8 · Amsterdam 9,5 · Madrid 9,3 · (Rom: keine Daten) |
| **PM10-Jahresmittel** (µg/m³) | Höchste: Warschau 21,0 · Prag 20,7; Spanne ca. 14–21 |
| WHO-2021-Jahresrichtwerte | PM2.5 5 · PM10 15 · NO2 10 |
| Dichte ↔ PM2.5 | r = −0,23 (alle, n = 7) vs. −0,95 (ohne Paris, n = 6); explorativ, nicht robust, kein Signifikanztest |
| Live-Events über Kafka → Spark | 192 (8 Städte × 24 h) |
| Abdeckung | Rom: 0 PM-Tage, 364 NO2-Tage; übrige Städte 348–365 Tage je Schadstoff |

---

## 10. Was die Präsentation NICHT enthalten soll

- Keine Code-Snippets, keine Notebook-Screenshots, keine Implementierungsdetails.
- Keine kausalen Aussagen („Stadt X ist schmutzig, weil …").
- Keine pauschale Gesamt-Rangliste der Städte.
- Keine erfundenen/aufgefüllten Werte für fehlende Daten (Rom-PM offen lassen).
- Mehr als 10 Inhaltsfolien.
