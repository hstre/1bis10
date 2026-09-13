#!/usr/bin/env python3
"""Erzeugt 120 feste Karten für das Kopfrechen-Duell."""

from pathlib import Path
import random

from pypdf import PdfReader
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "kopfrechen-kartenspiel.pdf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = HexColor("#17324d")
BLUE = HexColor("#2e6f9e")
SKY = HexColor("#dcecf5")
PALE = HexColor("#f5f8fb")
INK = HexColor("#17212b")
MUTED = HexColor("#667482")
GRID = HexColor("#b8c7d2")


def cards(category, pairs):
    return [{"category": category, "question": q, "answer": a} for q, a in pairs]


CATEGORIES = [
    cards("Addition und Subtraktion", [
        ("48 + 27", "75"), ("93 - 38", "55"), ("125 + 75 + 34", "234"),
        ("402 - 198", "204"), ("67 + 29", "96"), ("315 - 97", "218"),
        ("36 + 64 + 27", "127"), ("700 - 286", "414"), ("248 + 152", "400"),
        ("503 - 275", "228"),
    ]),
    cards("Multiplikation", [
        ("14 · 6", "84"), ("18 · 5", "90"), ("13 · 9", "117"), ("25 · 8", "200"),
        ("16 · 7", "112"), ("12 · 15", "180"), ("24 · 5", "120"),
        ("11 · 18", "198"), ("14 · 14", "196"), ("32 · 4", "128"),
    ]),
    cards("Division", [
        ("126 : 9", "14"), ("144 : 12", "12"), ("175 : 7", "25"),
        ("216 : 12", "18"), ("240 : 6", "40"), ("256 : 8", "32"),
        ("396 : 11", "36"), ("450 : 9", "50"), ("525 : 7", "75"),
        ("288 : 12", "24"),
    ]),
    cards("Einheiten", [
        ("4 km sind wie viele Meter?", "4000 m"),
        ("650 cm sind wie viele Meter?", "6,5 m"),
        ("3,2 m sind wie viele Zentimeter?", "320 cm"),
        ("6 Zentner sind wie viele Kilogramm?", "300 kg"),
        ("7500 ml sind wie viele Liter?", "7,5 l"),
        ("3 min 20 s sind wie viele Sekunden?", "200 s"),
        ("2 h 25 min sind wie viele Minuten?", "145 min"),
        ("8 kg sind wie viele Gramm?", "8000 g"),
        ("4,5 l sind wie viele Milliliter?", "4500 ml"),
        ("3200 mm sind wie viele Meter?", "3,2 m"),
    ]),
    cards("Schätzen", [
        ("49 · 21 liegt näher bei 100, 1000 oder 10 000?", "1000"),
        ("198 + 305 liegt näher bei 50, 500 oder 5000?", "500"),
        ("Wie hoch ist ungefähr eine Zimmertür?", "etwa 2 m"),
        ("Wie schwer ist ungefähr ein Apfel?", "etwa 200 g"),
        ("603 - 298 liegt näher bei 30, 300 oder 3000?", "300"),
        ("Wie viel fasst ungefähr ein Trinkglas?", "etwa 200 ml"),
        ("39 · 51 liegt näher bei 200, 2000 oder 20 000?", "2000"),
        ("Wie lang ist ungefähr ein Linienbus?", "etwa 12 m"),
        ("1002 - 497 liegt näher bei 50, 500 oder 5000?", "500"),
        ("Wie schwer ist ungefähr ein erwachsener Mensch?", "etwa 70 kg"),
    ]),
    cards("Verhältnisse", [
        ("Kürze 6 : 8 vollständig.", "3 : 4"),
        ("Kürze 12 : 18 vollständig.", "2 : 3"),
        ("4 von 10 Feldern: Welcher gekürzte Bruch?", "2/5"),
        ("Erweitere 2 : 5 mit 4.", "8 : 20"),
        ("Kürze 14 : 21 vollständig.", "2 : 3"),
        ("Sind 8 : 12 und 10 : 15 gleich?", "ja"),
        ("5 rote zu 3 blauen Kugeln. Rot : Blau?", "5 : 3"),
        ("Kürze 18 : 24 vollständig.", "3 : 4"),
        ("Erweitere 3 : 4 mit 5.", "15 : 20"),
        ("6 von 9 Feldern: Welcher gekürzte Bruch?", "2/3"),
    ]),
    cards("Diagramme und Daten", [
        ("Mo: 3, Di: 8, Mi: 5. An welchem Tag ist der Wert am größten?", "Dienstag"),
        ("Mo: 6, Di: 6, Mi: 2. An welchen Tagen liegt das Maximum?", "Montag und Dienstag"),
        ("Die Werte sind 4, 7 und 3. Wie groß ist ihre Summe?", "14"),
        ("Die Werte sind 9, 4 und 7. Unterschied zwischen größtem und kleinstem Wert?", "5"),
        ("Eine Achse zeigt 0, 5, 10, 15. Wie groß ist die Schrittweite?", "5"),
        ("Die Werte sind 8, 3 und 6. Welcher Wert ist am kleinsten?", "3"),
        ("Die Werte sind 5, 5 und 5. Wie groß ist ihre Summe?", "15"),
        ("Die Werte sind 7, 4 und 7. Wie viele Maxima gibt es?", "2"),
        ("Die Werte sind 2, 8 und 5. Wie groß ist der Unterschied?", "6"),
        ("Welche Achse zeigt meistens die Werte?", "die senkrechte Achse"),
    ]),
    cards("Zwei- und Dreisatz", [
        ("3 Brezeln kosten 6 €. Was kosten 7 Brezeln?", "14 €"),
        ("4 Hefte kosten 12 €. Was kosten 9 Hefte?", "27 €"),
        ("2 Pakete wiegen 10 kg. Wie viel wiegen 7 Pakete?", "35 kg"),
        ("5 Kisten enthalten 40 Flaschen. Wie viele enthalten 8 Kisten?", "64 Flaschen"),
        ("3 km dauern 15 min. Wie lange dauern 7 km?", "35 min"),
        ("4 Äpfel kosten 8 €. Was kosten 6 Äpfel?", "12 €"),
        ("6 Bücher kosten 24 €. Was kosten 5 Bücher?", "20 €"),
        ("3 Portionen brauchen 18 Kartoffeln. Wie viele brauchen 7 Portionen?", "42 Kartoffeln"),
        ("5 Runden bringen 30 Punkte. Wie viele bringen 9 Runden?", "54 Punkte"),
        ("4 Minuten: 20 Seiten. Wie viele Seiten in 9 Minuten?", "45 Seiten"),
    ]),
    cards("Ebene Figuren", [
        ("Wie viele Seiten hat ein Achteck?", "8"),
        ("Wie heißt ein Vieleck mit 6 Seiten?", "Sechseck"),
        ("Wie viele Spiegelachsen hat ein Quadrat?", "4"),
        ("Wie heißt ein Viereck mit vier rechten Winkeln?", "Rechteck"),
        ("Wie heißt ein Dreieck mit drei gleich langen Seiten?", "gleichseitiges Dreieck"),
        ("Wie viele Spiegelachsen hat ein gleichschenkliges Dreieck?", "1"),
        ("Wie heißt die Strecke vom Kreismittelpunkt zum Rand?", "Radius"),
        ("Wie viele Ecken hat ein Zehneck?", "10"),
        ("Ein Kreis hat Radius 7 cm. Wie groß ist sein Durchmesser?", "14 cm"),
        ("Wie heißt die längste Seite im rechtwinkligen Dreieck?", "Hypotenuse"),
    ]),
    cards("Körper und Raum", [
        ("Wie viele Ecken hat ein Würfel?", "8"),
        ("Wie viele Kanten hat ein Quader?", "12"),
        ("Wie viele Flächen hat ein Würfel?", "6"),
        ("Welcher Körper hat keine Ecken und Kanten?", "Kugel"),
        ("Welcher Körper hat zwei Kreisflächen?", "Zylinder"),
        ("Wie viele Ecken hat eine quadratische Pyramide?", "5"),
        ("Wie viele Kanten hat eine dreieckige Pyramide?", "6"),
        ("Zwei Würfel in einer Reihe: Wie viele Außenflächen?", "10"),
        ("Vier Würfel in einer Reihe: Wie viele Außenflächen?", "18"),
        ("Aus welchen Flächen besteht ein Würfel?", "aus 6 Quadraten"),
    ]),
]

EXTRA_ADD = cards("Plus und Minus", [
    ("58 + 36", "94"), ("84 - 29", "55"), ("175 + 225 + 16", "416"),
    ("612 - 298", "314"), ("39 + 48 + 61", "148"), ("1000 - 475", "525"),
    ("267 + 133", "400"), ("450 - 186", "264"), ("725 + 98", "823"),
    ("904 - 387", "517"),
])

EXTRA_MIX = cards("Mal oder Geteilt", [
    ("17 · 6", "102"), ("168 : 8", "21"), ("19 · 7", "133"),
    ("225 : 9", "25"), ("15 · 16", "240"), ("324 : 12", "27"),
    ("27 · 9", "243"), ("420 : 7", "60"), ("18 · 14", "252"),
    ("360 : 8", "45"),
])


def wrap(text, font, size, width):
    lines, line = [], ""
    for word in text.split():
        candidate = word if not line else f"{line} {word}"
        if pdfmetrics.stringWidth(candidate, font, size) <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centered_baseline(font, size, center_y):
    ascent = pdfmetrics.getAscent(font, size)
    descent = pdfmetrics.getDescent(font, size)
    return center_y - (ascent + descent) / 2


def draw_card(c, x, y, width, height, card, number):
    inset = 1.2 * mm
    left = x + inset
    bottom = y + inset
    inner_w = width - 2 * inset
    inner_h = height - 2 * inset

    c.setFillColor(white)
    c.setStrokeColor(GRID)
    c.setLineWidth(0.7)
    c.roundRect(left, bottom, inner_w, inner_h, 2.5 * mm, fill=1, stroke=1)

    bar_h = 8 * mm
    c.setFillColor(NAVY)
    c.roundRect(left, bottom + inner_h - bar_h, inner_w, bar_h, 2.5 * mm, fill=1, stroke=0)
    c.rect(left, bottom + inner_h - bar_h, inner_w, bar_h / 2, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DV-Bold", 6.3)
    c.drawString(left + 3 * mm, bottom + inner_h - 5.2 * mm, card["category"].upper())
    c.drawRightString(left + inner_w - 3 * mm, bottom + inner_h - 5.2 * mm, f"#{number:03d}")

    answer_h = 12 * mm
    c.setFillColor(SKY)
    c.roundRect(left + 1.5 * mm, bottom + 1.5 * mm, inner_w - 3 * mm, answer_h, 2 * mm, fill=1, stroke=0)
    c.saveState()
    c.translate(left + inner_w / 2, bottom + 1.5 * mm + answer_h / 2)
    c.rotate(180)
    c.setFillColor(NAVY)
    answer_size = 8.2 if len(card["answer"]) < 24 else 7.2
    c.setFont("DV-Bold", answer_size)
    c.drawCentredString(0, centered_baseline("DV-Bold", answer_size, 0), f"Lösung: {card['answer']}")
    c.restoreState()

    question = card["question"]
    size = 13
    if len(question) > 30:
        size = 10.8
    if len(question) > 58:
        size = 9.2
    max_w = inner_w - 8 * mm
    lines = wrap(question, "DV-Bold", size, max_w)
    while len(lines) > 4 and size > 7.8:
        size -= 0.5
        lines = wrap(question, "DV-Bold", size, max_w)
    leading = size * 1.28
    area_bottom = bottom + answer_h + 5 * mm
    area_top = bottom + inner_h - bar_h - 4 * mm
    block_h = len(lines) * leading
    baseline = area_bottom + (area_top - area_bottom + block_h) / 2 - leading
    c.setFillColor(INK)
    c.setFont("DV-Bold", size)
    for line in lines:
        c.drawCentredString(left + inner_w / 2, baseline, line)
        baseline -= leading


def page_cards(page_index):
    page = [category[page_index] for category in CATEGORIES]
    page.extend([EXTRA_ADD[page_index], EXTRA_MIX[page_index]])
    random.Random(101 + page_index).shuffle(page)
    return page


def build():
    pdfmetrics.registerFont(TTFont("DV", FONT))
    pdfmetrics.registerFont(TTFont("DV-Bold", BOLD))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    page_w, page_h = A4
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle("Kopfrechen-Duell - 120 Karten")
    c.setAuthor("1 bis 10")
    c.setSubject("Kartenspiel für zwei Schülerinnen und Schüler, Klasse 5")

    margin_x = 8 * mm
    grid_bottom = 8 * mm
    grid_top = page_h - 20 * mm
    card_w = (page_w - 2 * margin_x) / 3
    card_h = (grid_top - grid_bottom) / 4

    for page_index in range(10):
        c.setFillColor(NAVY)
        c.setFont("DV-Bold", 11)
        c.drawString(margin_x, page_h - 8 * mm, "KOPFRECHEN-DUELL")
        c.drawRightString(page_w - margin_x, page_h - 8 * mm, f"BLATT {page_index + 1} VON 10")
        c.setFillColor(MUTED)
        c.setFont("DV", 6.6)
        c.drawString(
            margin_x,
            page_h - 14 * mm,
            "Mischen und verdeckt auslegen · Der Jüngere beginnt · Ziehen · fragen · Sanduhr · prüfen · Rollen tauschen",
        )
        c.drawRightString(page_w - margin_x, page_h - 14 * mm, "An den gestrichelten Linien schneiden")

        for position, card in enumerate(page_cards(page_index)):
            row, col = divmod(position, 3)
            x = margin_x + col * card_w
            y = grid_top - (row + 1) * card_h
            draw_card(c, x, y, card_w, card_h, card, page_index * 12 + position + 1)

        c.setStrokeColor(MUTED)
        c.setDash(2, 2)
        c.setLineWidth(0.5)
        for col in range(4):
            x = margin_x + col * card_w
            c.line(x, grid_bottom, x, grid_top)
        for row in range(5):
            y = grid_bottom + row * card_h
            c.line(margin_x, y, page_w - margin_x, y)
        c.setDash()
        c.showPage()

    c.save()
    reader = PdfReader(OUTPUT)
    if len(reader.pages) != 10:
        raise RuntimeError(f"{len(reader.pages)} statt 10 Seiten")
    return OUTPUT


if __name__ == "__main__":
    print(build())
