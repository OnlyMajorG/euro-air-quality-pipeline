# Sprechtext zur Präsentation — ca. 40 Sekunden je Folie

> Begleittext zu `Luftqualität-Europa-BDENG.pptx` (Titelfolie + 10 Inhaltsfolien).
> Pro Folie ist der Sprechtext so bemessen, dass er in **~40 Sekunden** den Kern vermittelt
> (~100 Wörter, ~150 Wörter/Minute). Frei sprechen, nicht ablesen — die Stichworte tragen die Aussage.
> Gesamtdauer: ca. 7–8 Minuten, plus Puffer für Übergänge und Fragen.

---

## Titelfolie — Luftqualität in 8 europäischen Hauptstädten

Herzlich willkommen. Wir zeigen euch heute, wie sauber — oder eben nicht sauber — die Luft in acht
europäischen Hauptstädten ist. Das Ganze ist ein Big-Data-Engineering-Projekt: Wir haben Daten aus
drei sehr unterschiedlichen Quellen geholt, über Kafka transportiert, mit Spark verarbeitet und in
einer Bronze-Silver-Gold-Architektur abgelegt. Wichtig vorab: In dieser Präsentation zählen die
**Ergebnisse**, nicht der Code. Die Technik ist nur kurz Kontext. Unser Anspruch dabei ist
wissenschaftliche Ehrlichkeit — wir behaupten nur, was die Daten wirklich hergeben. Lasst uns starten.

---

## Folie 01 — Leitfrage & Maßstab (WHO 2021)

Unsere Leitfrage: Wie unterscheiden sich PM2.5, Feinstaub PM10 und Stickstoffdioxid NO2 zwischen
diesen acht Städten — und wie ordnet man das gesundheitlich ein? Damit wir nicht nur Städte
gegeneinander stellen, brauchen wir einen Maßstab: die WHO-Jahresrichtwerte von 2021. Die liegen bei
fünf Mikrogramm für PM2.5, fünfzehn für PM10 und zehn für NO2. Ganz wichtig und ehrlich gesagt: Das
sind **Gesundheits-Orientierungswerte**, keine gesetzlichen EU-Grenzwerte — die liegen höher. „Über
WHO" heißt also „über dem, was gesund ist", nicht „illegal". Datenbasis ist das volle Jahr 2025.

---

## Folie 02 — Datengrundlage

Kurz zum Fundament, denn Glaubwürdigkeit kommt zuerst: Acht Hauptstädte, 365 Tage im Jahr 2025, drei
Schadstoffe. Dahinter stehen **2,35 Millionen** validierte EEA-Stundenmessungen, die wir zu rund
7.900 Tageswerten in der Gold-Schicht verdichtet haben. Die Daten kommen aus drei verschiedenartigen
Quellen — das war eine Pflichtvorgabe: die EEA als Datei- und Datenbankquelle mit gemessenen Werten,
Wikipedia per Web-Scraping für den Stadtkontext, und Open-Meteo als REST-Schnittstelle für Live-Werte.
192 dieser Live-Ereignisse laufen über Kafka und Spark als Echtzeit-Nachweis. Unser Grundsatz: erst
Umfang und Abdeckung zeigen, dann interpretieren — und Lücken bleiben Lücken.

---

## Folie 03 — Befund 1: Alle Städte über den WHO-Richtwerten

Das ist unser Hauptbefund — und er ist eindeutig: **Keine einzige Stadt ist im grünen Bereich.** Schaut
auf die grünen Balken, das ist NO2: Jeder liegt über der WHO-Linie von zehn. Die Jahresmittel reichen
von 15,3 in Berlin bis 25,0 in Rom — also das Eineinhalb- bis Zweieinhalbfache des Richtwerts. Auch
beim Feinstaub PM2.5, den blauen Balken, ist jede Stadt über dem Wert von fünf. Eine Sache fällt auf:
Bei Rom fehlen die PM-Balken. Dort gibt es im Zeitraum keine validierten Feinstaub-Werte — und das
weisen wir offen aus, statt etwas zu erfinden.

---

## Folie 04 — Befund 2: PM2.5-Rangfolge

Schauen wir den Feinstaub genauer an. Beim PM2.5 liegt der Osten vorn: Warschau mit 14,7 und Prag mit
14,5 führen das Feld an, am unteren Ende stehen Madrid mit 9,3, Amsterdam und Wien. Aber — und das ist
der Punkt — **alle** liegen deutlich über dem WHO-Wert von fünf, teils um das Dreifache. Ganz wichtig
sind die Fehlerbalken: Sie zeigen die Schwankung von Tag zu Tag. Städte, die nah beieinander liegen,
etwa Berlin und Paris oder Wien, Amsterdam und Madrid, sind statistisch **nicht sicher** zu
unterscheiden. Kleine Rangunterschiede sollte man also nicht überinterpretieren.

---

## Folie 05 — Befund 3: Verteilung & Ausreißer

Ein Mittelwert allein kann täuschen — deshalb dieser Blick auf die Verteilungen. In jedem Boxplot zeigt
die Box die mittleren fünfzig Prozent der Tage, die Linie den Median, die Punkte sind Ausreißer-Tage.
Zwei Dinge sieht man sofort: Erstens liegt schon der **Median** bei jedem Schadstoff über dem
WHO-Wert — es ist also nicht nur ein Ausreißerproblem. Zweitens gibt es lange Schwänze nach oben:
einzelne Tage mit massiv höheren Werten, beim PM10 über achtzig Mikrogramm. Diese Spitzen verschwinden
im Jahresmittel — genau deshalb zeigen wir die Streuung und nicht nur den Durchschnitt.

---

## Folie 06 — Befund 4: Saisonalität

Woher kommen diese hohen Einzeltage? Der Tagesverlauf übers Jahr gibt die Antwort: **Der Winter treibt
den Feinstaub.** In der kalten Jahreszeit sehen wir Spitzen von 40 bis fast 50 Mikrogramm — im Sommer
liegen die Werte deutlich niedriger, oft nahe dem WHO-Wert. Zwei bekannte Effekte erklären das: Erstens
das Heizen, das mehr Feinstaub freisetzt. Zweitens Inversionswetterlagen, die die Schadstoffe am Boden
festhalten. Beachtet die Lücken in den Kurven — die lassen wir bewusst offen. Wir interpolieren nicht,
damit fehlende Tage nicht fälschlich wie Messwerte aussehen.

---

## Folie 07 — Befund 5: Bevölkerungsdichte erklärt die Belastung nicht

Jetzt verknüpfen wir zwei Quellen: die Bevölkerungsdichte aus Wikipedia mit dem Feinstaub aus den
EEA-Daten. Naheliegende Vermutung: dichter gleich schmutziger. Unsere Daten stützen das **nicht** — und
das spannend Ehrliche daran: Der Zusammenhang ist nicht robust. Über alle Städte liegt die Korrelation
bei minus 0,23, also nahe null. Nimmt man aber Paris heraus, kippt sie auf minus 0,95. Warum Paris?
Wikipedia führt Paris als Kernkommune mit nur 105 Quadratkilometern — verglichen mit den groß
abgegrenzten anderen Städten ist das schlicht **nicht vergleichbar**. Deshalb markieren wir Paris
gesondert. Klare Botschaft: Dichte erklärt hier nichts, das bleibt rein explorativ.

---

## Folie 08 — Befund 6: Live-Momentaufnahme (Kafka → Spark)

Hier läuft die Pipeline **live**. 192 aktuelle Stundenwerte holen wir von Open-Meteo, schicken sie als
JSON-Nachrichten über ein Kafka-Topic, und Spark Structured Streaming liest diesen Strom und schreibt
ihn in die Silver-Schicht. Genau dieser Kafka-zu-Spark-Weg war die technische Pflichtanforderung — und
hier sieht man, dass er funktioniert. Aber wir trennen sauber: Das sind **Modell-Stundenwerte** von
Open-Meteo, keine validierten Messungen wie bei der EEA. Deshalb stellen wir sie bewusst **nicht** gegen
die WHO-Jahreswerte und vermischen sie nie mit der historischen Analyse. Es ist ein Live-Nachweis,
kein Ersatz für die Messdaten.

---

## Folie 09 — Einordnung: Was die Daten nicht sagen

Diese Folie ist uns besonders wichtig, denn Grenzen offen zu benennen macht eine Analyse stärker, nicht
schwächer. Vier Prinzipien: Erstens, wir bleiben **deskriptiv** — wir beschreiben Muster, behaupten
keine Ursachen. Zweitens, **keine pauschale Rangliste** — die Reihenfolge hängt vom Schadstoff ab,
also betrachten wir jeden einzeln. Drittens, **Lücken bleiben Lücken** — Rom ohne Feinstaubwerte wird
offen ausgewiesen, nicht aufgefüllt. Und viertens, **Quellen sauber getrennt** — gemessene EEA-Historie
und Open-Meteo-Live werden nie vermischt. Kurz: Wir sagen genauso klar, was wir nicht behaupten.

---

## Folie 10 — Fazit: Drei Sätze zum Mitnehmen

Wenn ihr drei Dinge mitnehmt, dann diese. Erstens: **Überall zu viel NO2** — die Jahresmittel liegen
bei 15 bis 25 Mikrogramm statt der zehn, die die WHO empfiehlt. Zweitens: **Schadstoff schlägt Stadt** —
die Rangfolge hängt vom Schadstoff ab, eine einzelne Luftqualitäts-Rangliste wäre irreführend.
Drittens: **Kontext erklärt wenig** — die Bevölkerungsdichte ist kein Erklärungsfaktor; der
Zusammenhang ist nicht robust. Alles beruht auf echten, gemessenen EEA-Daten, transparent verarbeitet.
Der Code liegt offen im Repository. Vielen Dank — wir freuen uns auf eure Fragen.
