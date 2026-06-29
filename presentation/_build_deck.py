# -*- coding: utf-8 -*-
"""Build the findings-focused presentation PDF (title + 10 slides) from the
generated figures. Findings only, no code — per assignment presentation rules."""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "presentation" / "figures"
OUT = ROOT / "presentation" / "euro_air_quality_findings.pdf"

REPO = "https://github.com/OnlyMajorG/euro-air-quality-pipeline"
NAMES = "[Name 1]  ·  [Name 2]  ·  [Name 3]"   # <-- vor Abgabe ausfüllen
DATE = "Juni 2026"

NAVY = "#1F3A5F"
ACCENT = "#C44E52"
GREY = "#555555"
W, H = 13.333, 7.5  # 16:9


def new_slide():
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    return fig, ax


def header(ax, kicker, title):
    ax.add_patch(plt.Rectangle((0, 0.88), 1, 0.12, color=NAVY, zorder=0))
    ax.text(0.045, 0.945, kicker, color="#9DB4D0", fontsize=12,
            fontweight="bold", va="center")
    ax.text(0.045, 0.905, title, color="white", fontsize=21,
            fontweight="bold", va="center")


def footer(ax, page):
    ax.text(0.045, 0.03, "Euro Air Quality Pipeline", color=GREY, fontsize=8)
    ax.text(0.955, 0.03, f"{page}", color=GREY, fontsize=8, ha="right")


def figure_slide(pdf, kicker, title, img, bullets, page):
    fig, ax = new_slide()
    header(ax, kicker, title)
    im = mpimg.imread(str(img))
    ih, iw = im.shape[0], im.shape[1]
    # place image on left ~62% width, vertically centred in content area
    box_l, box_r, box_b, box_t = 0.04, 0.62, 0.10, 0.82
    bw, bh = box_r - box_l, box_t - box_b
    ar_img, ar_box = iw / ih, (bw * W) / (bh * H)
    if ar_img > ar_box:
        dw = bw; dh = bw * W / ar_img / H
    else:
        dh = bh; dw = bh * H * ar_img / W
    iax = fig.add_axes([box_l + (bw - dw) / 2, box_b + (bh - dh) / 2, dw, dh])
    iax.imshow(im); iax.axis("off")
    y = 0.74
    for b in bullets:
        ax.text(0.655, y, "▸", color=ACCENT, fontsize=14, fontweight="bold", va="top")
        ax.text(0.685, y, b, color="#222222", fontsize=12.5, va="top",
                wrap=True, linespacing=1.45)
        y -= 0.135
    footer(ax, page)
    pdf.savefig(fig); plt.close(fig)


def text_slide(pdf, kicker, title, blocks, page, big=None):
    fig, ax = new_slide()
    header(ax, kicker, title)
    if big:
        ax.text(0.5, 0.6, big, color=NAVY, fontsize=46, fontweight="bold",
                ha="center", va="center")
    y = 0.74
    for head, body in blocks:
        if head:
            ax.text(0.06, y, head, color=NAVY, fontsize=15, fontweight="bold", va="top")
            y -= 0.07
        if body:
            ax.text(0.07, y, body, color="#222222", fontsize=13, va="top",
                    linespacing=1.5)
            y -= 0.055 * (1 + body.count("\n")) + 0.04
    footer(ax, page)
    pdf.savefig(fig); plt.close(fig)


with PdfPages(str(OUT)) as pdf:
    # ---- Title slide (excluded from the 10) ----
    fig, ax = new_slide()
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=NAVY, zorder=0))
    ax.text(0.5, 0.66, "Luftqualität in 8 europäischen Hauptstädten",
            color="white", fontsize=30, fontweight="bold", ha="center")
    ax.text(0.5, 0.575, "Wie weit über gesunder Luft liegen Europas Städte?",
            color="#9DB4D0", fontsize=17, ha="center", style="italic")
    ax.text(0.5, 0.44, "Ein Big-Data-Engineering-Projekt",
            color="white", fontsize=14, ha="center")
    ax.text(0.5, 0.395,
            "EEA  ·  Wikipedia  ·  Open-Meteo   →   Kafka   →   Spark   →   Bronze/Silver/Gold",
            color="#9DB4D0", fontsize=12.5, ha="center")
    ax.text(0.5, 0.20, NAMES, color="white", fontsize=15, ha="center", fontweight="bold")
    ax.text(0.5, 0.13, REPO, color="#9DB4D0", fontsize=12, ha="center")
    ax.text(0.5, 0.08, DATE, color="#6E86A8", fontsize=11, ha="center")
    pdf.savefig(fig); plt.close(fig)

    # ---- Slide 1: question & WHO yardstick ----
    text_slide(
        pdf, "01 · Leitfrage", "Der Maßstab: WHO-2021-Richtwerte",
        [("Leitfrage",
          "Wie unterscheiden sich PM2.5-, PM10- und NO2-Werte zwischen acht\n"
          "europäischen Hauptstädten – und wie ordnet man sie gesundheitlich ein?"),
         ("WHO-2021-Jahresrichtwerte (Gesundheits-Orientierung)",
          "PM2.5 = 5 µg/m³        PM10 = 15 µg/m³        NO2 = 10 µg/m³"),
         ("Datenjahr",
          "Vollständiges Kalenderjahr 2025, gemessene Werte der EEA.")],
        1)

    # ---- Slide 2: scope ----
    text_slide(
        pdf, "02 · Datengrundlage", "Was in die Analyse einfließt",
        [("Umfang",
          "8 Hauptstädte   ·   365 Tage (2025)   ·   3 Schadstoffe"),
         ("Gemessene Datenbasis",
          "2,35 Mio. validierte EEA-Stundenmessungen  →  7 938 Tagesmittel (Gold)."),
         ("Drei Quellarten",
          "EEA-Download (Datei/DB)  ·  Wikipedia (Web-Scraping)  ·  Open-Meteo (REST-API).\n"
          "Live-Strom über Kafka → Spark: 192 Ereignisse als Echtzeit-Nachweis."),
         ("Wissenschaftlicher Grundsatz",
          "Erst Umfang & Abdeckung zeigen, dann interpretieren – Lücken bleiben Lücken.")],
        2)

    # ---- Slide 3: pollutant comparison (headline) ----
    figure_slide(
        pdf, "03 · Befund 1", "Alle Städte über den WHO-Richtwerten",
        FIG / "pollutant_comparison.png",
        ["Jeder NO2-Jahreswert (grün) liegt über der WHO-Linie von 10 µg/m³.",
         "PM2.5 (blau) überschreitet bei allen Städten den Richtwert von 5 µg/m³.",
         "Rom hat nur validierte NO2-Werte – PM fehlt und wird offen ausgewiesen."],
        3)

    # ---- Slide 4: PM2.5 ranking ----
    figure_slide(
        pdf, "04 · Befund 2", "PM2.5: Die östlichen Hauptstädte führen",
        FIG / "pm25_city_ranking.png",
        ["Höchste PM2.5-Mittel: Warschau & Prag (≈ 14,6 µg/m³).",
         "Niedrigste: Madrid, Amsterdam, Wien (≈ 9–10 µg/m³).",
         "Fehlerbalken = Tag-zu-Tag-Streuung; n = Zahl der Tageswerte."],
        4)

    # ---- Slide 5: distribution ----
    figure_slide(
        pdf, "05 · Befund 3", "Verteilungen und Ausreißer",
        FIG / "pollutant_distribution.png",
        ["Der Median jedes Schadstoffs liegt über dem WHO-Richtwert.",
         "Lange Oberschwänze: einzelne stark belastete Tage (Winterspitzen).",
         "Mittelwerte allein verbergen diese Streuung – darum Verteilung zeigen."],
        5)

    # ---- Slide 6: timeseries / seasonality ----
    figure_slide(
        pdf, "06 · Befund 4", "Saisonalität: der Winter treibt PM2.5",
        FIG / "selected_city_timeseries.png",
        ["Tagesverlauf der datenreichsten Städte – Lücken bleiben sichtbar.",
         "Höhere Werte im Winter: Heizung + Inversionswetterlagen.",
         "Erklärt, warum einzelne Tage den Jahresmittelwert spürbar heben."],
        6)

    # ---- Slide 7: density ----
    figure_slide(
        pdf, "07 · Befund 5", "Bevölkerungsdichte erklärt die Belastung nicht",
        FIG / "density_vs_air_quality.png",
        ["Nicht robust: r = −0,23 über alle (n=7), aber −0,95 ohne Paris (n=6).",
         "Paris = Kernkommune (~105 km²) → mit den anderen nicht vergleichbar (MAUP).",
         "Bewusst explorativ, kein Signifikanztest – keine Kausalität."],
        7)

    # ---- Slide 8: live snapshot ----
    figure_slide(
        pdf, "08 · Befund 6", "Live-Momentaufnahme (Kafka → Spark)",
        FIG / "live_air_quality_snapshot.png",
        ["Open-Meteo-Modellwerte, über Kafka produziert und von Spark gelesen.",
         "Stundenwerte – bewusst getrennt von den gemessenen EEA-Jahresdaten.",
         "Zeigt die Pipeline live, nicht als Ersatz für die historische Analyse."],
        8)

    # ---- Slide 9: honesty / limits ----
    text_slide(
        pdf, "09 · Einordnung", "Was die Daten (nicht) sagen",
        [("Deskriptiv, nicht kausal",
          "Wir beschreiben Muster, erklären keine Ursachen."),
         ("Keine pauschale Stadt-Rangliste",
          "Die Reihenfolge hängt vom Schadstoff ab – jeder wird einzeln betrachtet."),
         ("Ehrlich mit Lücken",
          "Rom ohne validierte PM-Werte: ausgewiesen, nicht aufgefüllt."),
         ("Sauber getrennt",
          "Gemessene EEA-Historie vs. Open-Meteo-Live-Modellwerte – nie vermischt.")],
        9)

    # ---- Slide 10: takeaways ----
    text_slide(
        pdf, "10 · Fazit", "Kernaussagen",
        [("1.  Überall zu viel NO2",
          "Alle acht Städte überschreiten den WHO-NO2-Richtwert (15–25 statt 10 µg/m³)."),
         ("2.  Schadstoff schlägt Stadt",
          "PM und NO2 folgen unterschiedlichen Mustern – getrennt betrachten."),
         ("3.  Kontext erklärt wenig",
          "Bevölkerungsdichte ist kein Erklärungsfaktor für die Belastung."),
         ("Repository", REPO)],
        10)

print("PDF geschrieben:", OUT)
