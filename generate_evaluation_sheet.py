#!/usr/bin/env python3
"""Erzeugt das Auswerteblatt für die 40 festen 1-bis-10-Durchgänge."""

from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "auswerteblatt-1bis10.pdf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = HexColor("#17324d")
BLUE = HexColor("#2e6f9e")
SKY = HexColor("#dcecf5")
PALE = HexColor("#f5f8fb")
INK = HexColor("#17212b")
MUTED = HexColor("#667482")
GRID = HexColor("#b8c7d2")

TASKS = [
    "Addition und Subtraktion",
    "Multiplikation",
    "Division",
    "Einheiten",
    "Schätzen",
    "Verhältnisse",
    "Diagramme",
    "Zwei- und Dreisatz",
    "Ebene Figuren",
    "Körper und Raum",
]


def centered_text(c, text, x, y, font, size):
    c.setFont(font, size)
    ascent = pdfmetrics.getAscent(font, size)
    descent = pdfmetrics.getDescent(font, size)
    c.drawCentredString(x, y - (ascent + descent) / 2, str(text))


def build():
    pdfmetrics.registerFont(TTFont("DV", FONT))
    pdfmetrics.registerFont(TTFont("DV-Bold", BOLD))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    width, height = landscape(A4)
    c = canvas.Canvas(str(OUTPUT), pagesize=(width, height), pageCompression=1)
    c.setTitle("1 bis 10 - Auswerteblatt")
    c.setAuthor("1 bis 10")
    c.setSubject("Auswertung der 40 Kopfrechen-Durchgänge für Klasse 5")

    # Kopf
    c.setFillColor(NAVY)
    c.rect(0, height - 34 * mm, width, 34 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DV-Bold", 9)
    c.drawString(16 * mm, height - 11 * mm, "1 BIS 10 · KOPFRECHNEN · KLASSE 5")
    c.setFont("DV-Bold", 23)
    c.drawString(16 * mm, height - 25 * mm, "Mein Auswerteblatt")

    c.setFillColor(INK)
    c.setFont("DV-Bold", 9)
    c.drawString(16 * mm, height - 44 * mm, "Name")
    c.drawString(126 * mm, height - 44 * mm, "Klasse")
    c.drawString(185 * mm, height - 44 * mm, "Schuljahr")
    c.setStrokeColor(GRID)
    c.setLineWidth(0.8)
    c.line(32 * mm, height - 45 * mm, 116 * mm, height - 45 * mm)
    c.line(143 * mm, height - 45 * mm, 175 * mm, height - 45 * mm)
    c.line(207 * mm, height - 45 * mm, 280 * mm, height - 45 * mm)

    # Kurze, kindgerechte Anleitung
    info_y = height - 61 * mm
    c.setFillColor(SKY)
    c.roundRect(16 * mm, info_y - 9 * mm, width - 32 * mm, 15 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("DV-Bold", 9.5)
    instruction_x = 22 * mm
    instruction_lead = "Nach jedem Durchgang:"
    c.drawString(instruction_x, info_y, instruction_lead)
    c.setFont("DV", 9.5)
    c.drawString(
        instruction_x + pdfmetrics.stringWidth(instruction_lead, "DV-Bold", 9.5) + 3 * mm,
        info_y,
        "Male ein Kästchen aus, wenn die Aufgabe richtig war. Lasse es frei, wenn du noch üben möchtest.",
    )

    # 40 x 10 Auswertungsraster
    cell = 6.1 * mm
    label_w = 10 * mm
    grid_w = 40 * cell
    grid_h = 10 * cell
    total_w = label_w + grid_w
    grid_x = (width - total_w) / 2
    grid_y = 64 * mm

    c.setFillColor(NAVY)
    c.setFont("DV-Bold", 8)
    centered_text(c, "NR.", grid_x + label_w / 2, grid_y + grid_h + 10 * mm, "DV-Bold", 8)
    c.drawString(grid_x + label_w, grid_y + grid_h + 10 * mm, "DURCHGANG / SET")

    # Spaltennummern
    for col in range(40):
        x = grid_x + label_w + col * cell
        if col % 5 == 0:
            c.setFillColor(SKY)
            c.rect(x, grid_y + grid_h + 1.2 * mm, 5 * cell, 7 * mm, fill=1, stroke=0)
        c.setFillColor(NAVY)
        centered_text(c, col + 1, x + cell / 2, grid_y + grid_h + 4.6 * mm, "DV-Bold", 6.5)

    # Zeilen und Kästchen
    for row in range(10):
        y = grid_y + grid_h - (row + 1) * cell
        c.setFillColor(BLUE)
        c.rect(grid_x, y, label_w, cell, fill=1, stroke=0)
        c.setFillColor(white)
        centered_text(c, row + 1, grid_x + label_w / 2, y + cell / 2, "DV-Bold", 8)
        for col in range(40):
            x = grid_x + label_w + col * cell
            c.setFillColor(white if col % 5 else PALE)
            c.rect(x, y, cell, cell, fill=1, stroke=0)

    # Gitternetz mit stärkerer Linie nach jeweils fünf Sets
    c.setStrokeColor(GRID)
    c.setLineWidth(0.45)
    for row in range(11):
        y = grid_y + row * cell
        c.line(grid_x, y, grid_x + total_w, y)
    for col in range(41):
        x = grid_x + label_w + col * cell
        c.setLineWidth(1.1 if col % 5 == 0 else 0.45)
        c.setStrokeColor(BLUE if col % 5 == 0 else GRID)
        c.line(x, grid_y, x, grid_y + grid_h)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.1)
    c.rect(grid_x, grid_y, total_w, grid_h, fill=0, stroke=1)
    c.line(grid_x + label_w, grid_y, grid_x + label_w, grid_y + grid_h)

    # Legende
    legend_y = 46 * mm
    c.setFillColor(NAVY)
    c.setFont("DV-Bold", 9)
    c.drawString(16 * mm, legend_y + 5 * mm, "Die zehn Aufgabentypen")
    col_w = (width - 32 * mm) / 5
    for i, task in enumerate(TASKS):
        col = i % 5
        row = i // 5
        x = 16 * mm + col * col_w
        y = legend_y - row * 11 * mm
        c.setFillColor(BLUE)
        c.circle(x + 3.4 * mm, y, 3.4 * mm, fill=1, stroke=0)
        c.setFillColor(white)
        centered_text(c, i + 1, x + 3.4 * mm, y, "DV-Bold", 7)
        c.setFillColor(INK)
        c.setFont("DV-Bold", 7.7)
        c.drawString(x + 9 * mm, y - 1.2 * mm, task)

    c.setStrokeColor(GRID)
    c.setLineWidth(0.7)
    c.line(16 * mm, 14 * mm, width - 16 * mm, 14 * mm)
    c.setFillColor(MUTED)
    c.setFont("DV", 7)
    c.drawString(16 * mm, 9 * mm, "1 bis 10 · 40 feste Durchgänge")
    c.drawRightString(width - 16 * mm, 9 * mm, "Ein Kästchen für jede richtige Aufgabe")

    c.showPage()
    c.save()

    reader = PdfReader(OUTPUT)
    if len(reader.pages) != 1:
        raise RuntimeError(f"{len(reader.pages)} statt 1 Seite")
    return OUTPUT


if __name__ == "__main__":
    print(build())
