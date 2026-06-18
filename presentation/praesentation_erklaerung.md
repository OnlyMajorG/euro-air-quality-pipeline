# Präsentation – Erklärung & Sprecherleitfaden

> Begleitdokument zu `euro_air_quality_findings.pdf` (Titelfolie + 10 Folien).
> Es erklärt, **was wir zeigen wollen**, und gibt für **jede Folie und jede Grafik**
> die Bedeutung, die wichtigsten Zahlen und Stichpunkte zum Sprechen.

---

## 1. Was wollen wir überhaupt erklären?

Das Projekt hat **zwei Ebenen** – wichtig, beide auseinanderzuhalten:

1. **Data-Engineering (das eigentliche Lernziel der LV):** Wir holen Daten aus
   **drei verschiedenartigen Quellen**, transportieren sie über **Kafka**, verarbeiten
   sie mit **Spark** und legen sie in einer **Medallion-Architektur** (Bronze → Silver →
   Gold) ab. Das ist der technische Kern.
2. **Die Geschichte (Findings):** Damit die Daten „lebendig" werden, beantworten wir
   eine konkrete Frage: **Wie sauber ist die Luft in acht europäischen Hauptstädten –
   gemessen am gesundheitlichen Maßstab der WHO?**

> **Wichtig laut Aufgabenstellung:** In der *Präsentation* zählen die **Findings**, nicht
> der Code. Deshalb zeigt das Deck Diagramme und Aussagen – die Technik nur als kurzer
> Kontext auf Folie 2. Die technische Tiefe steckt in den Notebooks (`00`–`10`) und im Repo.

### Die Kernbotschaft in einem Satz
**Keine der acht Städte hält die WHO-Richtwerte für NO2 ein, und die Rangfolge hängt vom
Schadstoff ab – wir zeigen das ehrlich, deskriptiv und ohne die Daten schönzurechnen.**

---

## 2. Der rote Faden (Dramaturgie)

| Phase | Folien | Zweck |
| --- | --- | --- |
| **Frage & Maßstab** | 1–2 | Worum geht es, woran messen wir, wie viele Daten |
| **Befunde** | 3–8 | Sechs Diagramme, jeder ein eigener Befund |
| **Ehrlichkeit** | 9 | Was die Daten *nicht* sagen (wissenschaftliche Sauberkeit) |
| **Fazit** | 10 | Drei Kernaussagen + Repo-Link |

Wir bauen bewusst von „alle sind betroffen" (Folie 3) über die Differenzierung
(Folien 4–7) bis zur ehrlichen Einordnung (Folie 9). So bleibt es eine *Geschichte*,
keine Diagramm-Aufzählung.

---

## 3. Der Maßstab: WHO-2021-Richtwerte (einmal verstehen, überall nutzen)

Die Weltgesundheitsorganisation (WHO) hat 2021 **Jahres-Richtwerte** für gesunde Luft
veröffentlicht. Wir vergleichen unsere Stadt-Jahresmittel damit:

| Schadstoff | WHO-2021-Jahresrichtwert | Was es ist |
| --- | --- | --- |
| **PM2.5** | **5 µg/m³** | Feinstaub < 2,5 µm – dringt tief in die Lunge, gesundheitlich am kritischsten |
| **PM10** | **15 µg/m³** | Gröberer Staub < 10 µm |
| **NO2** | **10 µg/m³** | Stickstoffdioxid – v. a. aus Verkehr/Verbrennung |

> **Ehrlich bleiben:** Das sind **Gesundheits-Orientierungswerte**, *keine* gesetzlichen
> EU-Grenzwerte (die liegen höher, z. B. NO2 40 µg/m³). Wir sagen also nicht „illegal",
> sondern „über dem, was die WHO als gesund ansieht". µg/m³ = Mikrogramm pro Kubikmeter Luft.

---

## 4. Folie für Folie

### Titelfolie
- **Zeigt:** Projekttitel, Leitfrage als Untertitel, die Pipeline in einer Zeile
  (EEA · Wikipedia · Open-Meteo → Kafka → Spark → Bronze/Silver/Gold), **Namen**, **Repo-Link**.
- **Sagen:** Kurz Thema + dass es ein Big-Data-Engineering-Projekt ist. Nicht vorlesen.
- ⚠️ **Vor der Abgabe:** echte Namen statt `[Name 1/2/3]` eintragen, Repo öffentlich schalten.

### Folie 1 – Leitfrage & Maßstab
- **Zeigt:** die Forschungsfrage und die drei WHO-Werte.
- **Bedeutung:** definiert den „Messlatte", an der alles Folgende gemessen wird.
- **Sagen:** „Wir vergleichen acht Hauptstädte – und zwar gegen den WHO-Gesundheitsmaßstab,
  nicht gegeneinander im luftleeren Raum."

### Folie 2 – Datengrundlage
- **Zeigt:** Umfang (8 Städte · 365 Tage 2025 · 3 Schadstoffe), **2,35 Mio.** gemessene
  EEA-Stundenwerte → **7.938** Tagesmittel, die drei Quellarten, 192 Live-Events.
- **Bedeutung:** Glaubwürdigkeit. Wir zeigen *zuerst* den Datenumfang, *dann* Aussagen –
  ein wissenschaftlicher Grundsatz.
- **Sagen:** „Die Aussagen stehen auf 2,35 Millionen echten Messungen, nicht auf Beispielen.
  Drei Quellarten: Datei/Datenbank, Web-Scraping, REST-API – plus ein Live-Strom über Kafka/Spark."

### Folie 3 – Befund 1: *Alle Städte über den WHO-Richtwerten*  ▸ `pollutant_comparison.png`
- **Grafik:** Gruppierte Balken je Stadt – **blau = PM2.5, orange = PM10, grün = NO2**.
  Die **gestrichelten Linien** sind die WHO-Werte (blau 5, orange 15, grün 10).
- **Was man sieht:** Jeder grüne Balken (NO2) ragt über die grüne Linie; jeder blaue (PM2.5)
  über die blaue. Bei **Rom** fehlen blau/orange – dort gibt es keine validierten PM-Werte.
- **Kernzahlen:** NO2-Jahresmittel **15,3–25,0 µg/m³** (WHO: 10) → 1,5- bis 2,5-fach drüber.
- **Sagen:** „Egal welche Stadt – beim NO2 ist keine im grünen Bereich. Das ist der Hauptbefund."

### Folie 4 – Befund 2: *PM2.5 – die östlichen Hauptstädte führen*  ▸ `pm25_city_ranking.png`
- **Grafik:** Horizontale Balken, PM2.5-Mittel je Stadt, **Fehlerbalken = Standardabweichung**
  der Tageswerte, `n` = Zahl der Tageswerte. Gestrichelte Linie = WHO 5 µg/m³.
- **Was man sieht:** **Warschau (14,7)** und **Prag (14,5)** oben, **Madrid/Amsterdam/Wien
  (~9–10)** unten. Rom fehlt (kein PM2.5).
- **Bedeutung:** Reihenfolge *innerhalb* von PM2.5. Fehlerbalken warnen: benachbarte Städte
  sind nicht sicher unterscheidbar.
- **Sagen:** „Beim Feinstaub liegt der Osten vorn – aber alle über dem WHO-Wert. Die Fehlerbalken
  zeigen, dass man kleine Rangunterschiede nicht überinterpretieren darf."

### Folie 5 – Befund 3: *Verteilungen und Ausreißer*  ▸ `pollutant_distribution.png`
- **Grafik:** Boxplot je Schadstoff. Box = mittlere 50 % der Tage, Linie = Median, Punkte =
  Ausreißer-Tage. Rote Striche = WHO-Werte.
- **Was man sieht:** Der **Median liegt bei jedem Schadstoff über dem WHO-Wert**; lange
  Schwänze nach oben = einzelne stark belastete Tage.
- **Bedeutung:** Mittelwerte allein verbergen Streuung. Die Ausreißer-Tage sind real
  (oft Winter, siehe Folie 6).
- **Sagen:** „Nicht nur der Durchschnitt ist zu hoch – es gibt einzelne Tage, die weit darüber liegen."

### Folie 6 – Befund 4: *Saisonalität – der Winter treibt PM2.5*  ▸ `selected_city_timeseries.png`
- **Grafik:** Tagesverlauf der datenreichsten Städte übers Jahr. **Punkte = vorhandene Tage,
  Lücken bleiben Lücken** (keine Interpolation).
- **Was man sieht:** Höhere Werte im Winter, niedrigere im Sommer.
- **Bedeutung / Research:** Winter = mehr **Heizen** + **Inversionswetterlagen** (Schadstoffe
  bleiben am Boden). Das erklärt die Ausreißer-Tage aus Folie 5.
- **Sagen:** „Das Muster ist saisonal: Heizperiode und Wetterlagen im Winter heben die Werte –
  ein bekannter Effekt, den unsere Daten sichtbar machen."

### Folie 7 – Befund 5: *Bevölkerungsdichte erklärt die Belastung nicht*  ▸ `density_vs_air_quality.png`
- **Grafik:** Streudiagramm Dichte (x, aus **Wikipedia**) vs. PM2.5 (y, aus **EEA**), je Punkt eine Stadt.
- **Was man sieht:** Kein klarer Trend. **Pearson r = −0,23 (n = 7)**. Paris ist mit
  ~19.430 Einw./km² extrem dicht, aber bei PM2.5 nur mittig.
- **Bedeutung:** Ein bewusst **negativer/exploratives** Ergebnis – Dichte ist *kein*
  Erklärungsfaktor. **Kein Signifikanztest**, nur Orientierung.
- **Sagen:** „Man könnte denken: dichter = schmutziger. Unsere Daten stützen das nicht.
  Wichtig: Das ist explorativ, wir behaupten keine Ursache." *(Hier zeigt sich auch, dass
  zwei verschiedene Quellen – Scraping + EEA – sinnvoll verknüpft wurden.)*

### Folie 8 – Befund 6: *Live-Momentaufnahme (Kafka → Spark)*  ▸ `live_air_quality_snapshot.png`
- **Grafik:** Aktuelle Stundenwerte je Stadt aus **Open-Meteo**, über **Kafka** produziert und
  von **Spark** aus dem Topic gelesen.
- **Bedeutung:** Der **Live-Nachweis** der Pipeline – das ist genau der von der Aufgabe geforderte
  Kafka→Spark-Weg.
- **Ehrlich trennen:** Das sind **Modell-Stundenwerte**, *kein* Ersatz für die gemessenen
  EEA-Jahresdaten – deshalb **bewusst nicht** gegen die WHO-*Jahres*werte gestellt.
- **Sagen:** „Hier läuft die Pipeline live: Open-Meteo → Kafka → Spark. Diese Werte halten wir
  strikt getrennt von der historischen Messanalyse."

### Folie 9 – Einordnung: *Was die Daten (nicht) sagen*
- **Zeigt:** vier Ehrlichkeits-Prinzipien (deskriptiv statt kausal; keine pauschale Rangliste;
  Lücken offen; Live vs. historisch getrennt).
- **Bedeutung:** Das ist **Pflichtteil eines guten Data-Science-Projekts** – die Grenzen klar
  benennen wirkt stärker, nicht schwächer.
- **Sagen:** „Wir sagen genauso klar, was wir *nicht* behaupten: keine Ursachen, keine
  Gesamtrangliste, keine erfundenen Werte für Rom."

### Folie 10 – Fazit: *Kernaussagen*
- **Zeigt:** 3 Aussagen + Repo-Link.
  1. Überall zu viel NO2 (15–25 statt 10 µg/m³).
  2. Schadstoff schlägt Stadt – getrennt betrachten.
  3. Kontext (Dichte) erklärt wenig.
- **Sagen:** Die drei Sätze sind die *einzigen* Dinge, die das Publikum mitnehmen soll. Repo zeigen.

---

## 5. Wahrscheinliche Rückfragen – ehrliche Antworten

- **„Warum nur 8 Städte / ein Jahr?"** – Fokus liegt auf dem Engineering-Setup, nicht auf
  Datenmenge. Es sind trotzdem 2,35 Mio. Messungen.
- **„Ist das wirklich Big Data?"** – Ehrlich: grenzwertig. Aber wir wenden die *Verfahren*
  (Kafka, Spark, verteilte Verarbeitung, Schichtenarchitektur) korrekt an – darum geht es.
- **„Warum fehlt Rom bei PM?"** – Im Zeitraum keine von der EEA *validierten* PM-Werte. Wir
  füllen nichts auf, sondern weisen es offen aus.
- **„WHO-Wert überschritten – heißt das illegal?"** – Nein. WHO = Gesundheitsempfehlung,
  EU-Grenzwerte sind höher. Wir messen an Gesundheit, nicht an Gesetz.
- **„Warum NO2 im Sommer/Winter unterschiedlich?"** – NO2 ist verkehrsgeprägt, PM stärker
  heizungs-/wetterabhängig – darum unterschiedliche Muster (Folien 3 & 6).

---

## 6. Mini-Glossar

- **PM2.5 / PM10** – Feinstaub-Partikel < 2,5 bzw. < 10 µm. Kleiner = gesundheitlich kritischer.
- **NO2** – Stickstoffdioxid, v. a. aus Verbrennung/Verkehr.
- **µg/m³** – Mikrogramm pro Kubikmeter Luft (die Konzentrationseinheit).
- **EEA** – European Environment Agency; liefert gemessene, validierte Stundenwerte.
- **Open-Meteo** – kostenlose Wetter-/Luft-API; liefert *Modell*-Werte (Echtzeit).
- **Kafka** – Nachrichten-Broker; transportiert Datenströme über „Topics".
- **Spark** – verteilte Verarbeitungs-Engine; liest hier den Kafka-Strom und verarbeitet ihn.
- **Medallion (Bronze/Silver/Gold)** – Datenschichten: roh → bereinigt → analysebereit.
- **Deskriptiv** – beschreibend (Muster zeigen), *nicht* kausal (Ursachen behaupten).

---

## 7. Faktencheck – alle Zahlen aus dem verifizierten End-to-End-Lauf

| Größe | Wert |
| --- | --- |
| Gemessene EEA-Stundenwerte (Bronze) | 2.352.005 |
| Tagesmittel (Silver/Gold) | 7.938 über 365 Tage, 8 Städte |
| NO2-Jahresmittel (µg/m³) | Rom 25,0 · Paris 23,0 · Prag 22,7 · Warschau 22,6 · Madrid 22,5 · Amsterdam 18,1 · Wien 16,0 · Berlin 15,3 |
| PM2.5-Jahresmittel (µg/m³) | Warschau 14,7 · Prag 14,5 · Berlin 11,4 · Paris 11,1 · Wien 9,8 · Amsterdam 9,6 · Madrid 9,3 · (Rom fehlt) |
| WHO-2021-Jahresrichtwerte | PM2.5 5 · PM10 15 · NO2 10 |
| Dichte ↔ PM2.5 | Pearson r = −0,23 (n = 7), explorativ |
| Live-Events über Kafka→Spark | 192 (8 Städte × 24 h) |
