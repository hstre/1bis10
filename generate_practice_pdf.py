#!/usr/bin/env python3
"""Erzeugt das feste 1-bis-10-Uebungsheft fuer Klasse 6."""

from __future__ import annotations

import math
import random
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "1bis10-uebungsheft-klasse6.pdf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = HexColor("#17324d")
BLUE = HexColor("#2e6f9e")
SKY = HexColor("#dcecf5")
INK = HexColor("#17212b")
MUTED = HexColor("#667482")
GRID = HexColor("#d7e0e7")
RED = HexColor("#d94b45")

CATEGORIES = [
    "Addition und Subtraktion",
    "Multiplikation",
    "Division",
    "Einheiten",
    "Schaetzen",
    "Verhaeltnisse",
    "Diagramme",
    "Zwei- und Dreisatz",
    "Ebene Figuren",
    "Koerper und Raum",
]

DISPLAY_CATEGORIES = [
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


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("DejaVu", FONT))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_BOLD))


def wrap_text(text: str, font: str, size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        test = word if not line else f"{line} {word}"
        if pdfmetrics.stringWidth(test, font, size) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, width: float,
                 size: float = 10.5, leading: float = 13, max_lines: int = 3,
                 font: str = "DejaVu") -> None:
    lines = wrap_text(text, font, size, width)[:max_lines]
    c.setFont(font, size)
    c.setFillColor(INK)
    for index, line in enumerate(lines):
        c.drawString(x, y - index * leading, line)


def draw_header(c: canvas.Canvas, category_no: int, sheet_no: int, page_no: int, total_pages: int) -> None:
    width, height = A4
    c.setPageSize(A4)
    c.setFillColor(NAVY)
    c.rect(0, height - 24 * mm, width, 24 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DejaVu-Bold", 11)
    c.drawString(15 * mm, height - 10 * mm, "1 BIS 10")
    c.setFont("DejaVu-Bold", 18)
    c.drawString(15 * mm, height - 19 * mm, DISPLAY_CATEGORIES[category_no - 1])
    c.setFont("DejaVu", 9)
    c.drawRightString(width - 15 * mm, height - 17 * mm, f"Übungsblatt {sheet_no} von 40")

    c.setFillColor(MUTED)
    c.setFont("DejaVu", 9)
    y = height - 32 * mm
    c.drawString(15 * mm, y, "Name:")
    c.line(29 * mm, y - 1, 102 * mm, y - 1)
    c.drawString(116 * mm, y, "Datum:")
    c.line(132 * mm, y - 1, width - 15 * mm, y - 1)
    draw_footer(c, category_no, sheet_no, page_no, total_pages)


def draw_footer(c: canvas.Canvas, category_no: int, sheet_no: int, page_no: int, total_pages: int) -> None:
    width, _ = c._pagesize
    c.setStrokeColor(GRID)
    c.setLineWidth(0.5)
    c.line(15 * mm, 14 * mm, width - 15 * mm, 14 * mm)
    c.setFillColor(MUTED)
    c.setFont("DejaVu", 7.5)
    c.drawString(15 * mm, 8.5 * mm, f"Aufgabentyp {category_no} von 10 · Blatt {sheet_no} von 40")
    c.drawRightString(width - 15 * mm, 8.5 * mm, f"Seite {page_no} von {total_pages}")


def task(text: str, answer: str, kind: str = "text", **data) -> dict:
    return {"text": text, "answer": answer, "kind": kind, **data}


def addition_task(rng: random.Random, sheet: int, index: int) -> dict:
    ceiling = 100 if sheet <= 10 else 250 if sheet <= 20 else 500 if sheet <= 30 else 1000
    start = rng.randrange(max(20, ceiling // 5), max(30, ceiling // 2))
    values = [start]
    total = start
    for _ in range(3):
        magnitude = rng.randrange(5, max(7, ceiling // 7))
        sign = -1 if rng.random() < 0.45 and total - magnitude >= 0 else 1
        values.append(sign * magnitude)
        total += sign * magnitude
    expression = str(values[0]) + " " + " ".join((f"+ {v}" if v >= 0 else f"- {abs(v)}") for v in values[1:])
    if index % 5 == 4:
        return task(f"Ein Team startet mit {start} Punkten. Danach: " + ", ".join(
            f"{v:+d}" for v in values[1:]) + ". Wie viele Punkte hat es am Ende?", str(total))
    return task(f"{expression} =", str(total))


def multiplication_task(rng: random.Random, sheet: int, index: int) -> dict:
    factor_a = rng.randint(4, 12 + sheet // 8)
    factor_b = rng.randint(2, 12)
    product = factor_a * factor_b
    if index % 4 == 3:
        return task(f"{factor_a} · □ = {product}", str(factor_b))
    return task(f"{factor_a} · {factor_b} =", str(product))


def division_task(rng: random.Random, sheet: int, index: int) -> dict:
    divisor = rng.randint(2, 12)
    quotient = rng.randint(4, 12 + sheet // 5)
    dividend = divisor * quotient
    if index % 5 == 4:
        return task(f"□ : {divisor} = {quotient}", str(dividend))
    return task(f"{dividend} : {divisor} =", str(quotient))


def unit_task(rng: random.Random, sheet: int, index: int) -> dict:
    mode = (sheet * 10 + index) % 12
    n = rng.randint(2, 12)
    if mode == 0:
        return task(f"{n} m = ____ cm", f"{n * 100} cm")
    if mode == 1:
        return task(f"{n} km = ____ m", f"{n * 1000} m")
    if mode == 2:
        return task(f"{n} kg = ____ g", f"{n * 1000} g")
    if mode == 3:
        return task(f"{n} h = ____ min", f"{n * 60} min")
    if mode == 4:
        return task(f"{n} min = ____ s", f"{n * 60} s")
    if mode == 5:
        return task(f"{n} Zentner = ____ kg", f"{n * 50} kg")
    if mode == 6:
        return task(f"{n} l = ____ ml", f"{n * 1000} ml")
    if mode == 7:
        return task(f"{n * 100} cm = ____ m", f"{n} m")
    if mode == 8:
        return task(f"{n * 60} min = ____ h", f"{n} h")
    if mode == 9:
        return task(f"{n * 60} s = ____ min", f"{n} min")
    if mode == 10:
        minutes = rng.randint(1, 8)
        seconds = rng.choice([10, 20, 30, 40, 50])
        return task(f"{minutes} min {seconds} s = ____ s", f"{minutes * 60 + seconds} s")
    hours = rng.randint(1, 5)
    minutes = rng.choice([10, 15, 20, 30, 40, 45, 50])
    return task(f"{hours} h {minutes} min = ____ min", f"{hours * 60 + minutes} min")


REAL_ESTIMATES = [
    ("Wie hoch ist ungefähr eine Zimmertür?", ["20 cm", "2 m", "20 m"], "2 m"),
    ("Wie schwer ist ungefähr ein gefüllter Schulranzen?", ["400 g", "4 kg", "40 kg"], "4 kg"),
    ("Wie lange dauert ungefähr eine Unterrichtsstunde?", ["5 min", "45 min", "4 h"], "45 min"),
    ("Wie viel Wasser passt ungefähr in eine Badewanne?", ["2 l", "20 l", "200 l"], "200 l"),
    ("Wie lang ist ungefähr ein Linienbus?", ["1 m", "12 m", "120 m"], "12 m"),
    ("Wie schwer ist ungefähr eine Büroklammer?", ["1 g", "100 g", "1 kg"], "1 g"),
    ("Wie lang ist ungefähr ein Fußballfeld?", ["10 m", "100 m", "1000 m"], "100 m"),
    ("Wie viel fasst ungefähr ein kleines Trinkglas?", ["20 ml", "200 ml", "2 l"], "200 ml"),
    ("Wie breit ist ungefähr eine Hand?", ["1 cm", "10 cm", "1 m"], "10 cm"),
    ("Wie schwer ist ungefähr ein mittelgroßer Apfel?", ["20 g", "200 g", "2 kg"], "200 g"),
    ("Wie hoch ist ungefähr ein Esstisch?", ["7 cm", "75 cm", "7 m"], "75 cm"),
    ("Wie viel Wasser passt ungefähr in einen Putzeimer?", ["1 l", "10 l", "100 l"], "10 l"),
    ("Wie schwer ist ungefähr ein Liter Wasser?", ["100 g", "1 kg", "10 kg"], "1 kg"),
    ("Wie lang ist ungefähr ein Bleistift?", ["2 cm", "20 cm", "2 m"], "20 cm"),
    ("Wie hoch ist ungefähr eine Treppenstufe?", ["2 cm", "20 cm", "2 m"], "20 cm"),
    ("Wie warm ist ein Klassenzimmer ungefähr?", ["2 °C", "20 °C", "200 °C"], "20 °C"),
]


def estimate_task(rng: random.Random, sheet: int, index: int) -> dict:
    if index % 2 == 0:
        prompt, choices, answer = REAL_ESTIMATES[(sheet * 5 + index // 2) % len(REAL_ESTIMATES)]
        return task(f"{prompt}   {'  |  '.join(choices)}", answer)
    a = rng.randrange(20, 950)
    b = rng.randrange(12, 550)
    if index % 4 == 1:
        exact = a + b
        rounded = round(exact, -max(1, len(str(exact)) - 2))
        choices = [max(10, rounded // 10), rounded, rounded * 10]
        return task(f"Welches Ergebnis liegt {a} + {b} am nächsten?   " + "  |  ".join(map(str, choices)), str(rounded))
    a = rng.randint(18, 99)
    b = rng.randint(6, 51)
    exact = a * b
    magnitude = 10 ** max(1, len(str(exact)) - 1)
    answer = round(exact / magnitude) * magnitude
    choices = sorted({max(10, answer // 10), answer, answer * 10})
    while len(choices) < 3:
        choices.append(choices[-1] + magnitude)
    return task(f"Welches Ergebnis liegt {a} · {b} am nächsten?   " + "  |  ".join(map(str, choices)), str(answer))


def ratio_task(rng: random.Random, sheet: int, index: int) -> dict:
    total = rng.randint(3, 12)
    filled = rng.randint(1, total - 1)
    divisor = math.gcd(filled, total)
    if index % 2 == 0:
        answer = f"{filled // divisor}/{total // divisor}"
        return task("Welcher Anteil der Felder ist blau? Gib den Bruch gekürzt an.", answer,
                    kind="ratio", filled=filled, total=total)
    left = filled * rng.choice([2, 3, 4])
    right = total * (left // filled)
    divisor = math.gcd(left, right)
    return task(f"Kürze das Verhältnis {left} : {right}.", f"{left // divisor} : {right // divisor}")


def chart_task(rng: random.Random, sheet: int, index: int) -> dict:
    labels = ["Mo", "Di", "Mi"]
    operation = ["max", "min", "sum", "difference"][index % 4]
    values = [rng.randint(2, 9) for _ in range(3)]
    if sheet % 5 == 0 and operation in {"max", "min"}:
        values[1] = values[0]
        values[2] = rng.randint(2, values[0]) if operation == "max" else rng.randint(values[0], 9)
    if operation == "max":
        target = max(values)
        answer = " und ".join(label for label, value in zip(labels, values) if value == target)
        prompt = "An welchem Tag ist der Wert am größten?"
    elif operation == "min":
        target = min(values)
        answer = " und ".join(label for label, value in zip(labels, values) if value == target)
        prompt = "An welchem Tag ist der Wert am kleinsten?"
    elif operation == "sum":
        answer = str(sum(values))
        prompt = "Wie groß ist die Summe der drei Werte?"
    else:
        answer = str(max(values) - min(values))
        prompt = "Wie groß ist der Unterschied zwischen größtem und kleinstem Wert?"
    return task(prompt, answer, kind="chart", labels=labels, values=values,
                show_values=operation in {"sum", "difference"})


PROPORTIONAL_CONTEXTS = [
    ("cost", "Brezeln", "€"), ("cost", "Hefte", "€"), ("need", "Personen", "Eier"),
    ("cost", "Kinokarten", "€"), ("time", "Kilometer", "min"), ("cost", "Äpfel", "€"),
    ("weight", "Pakete", "kg"), ("contain", "Kisten", "Flaschen"),
    ("read", "Tage", "Seiten"), ("points", "Runden", "Punkte"),
]


def proportional_task(rng: random.Random, sheet: int, index: int) -> dict:
    kind, noun, unit = PROPORTIONAL_CONTEXTS[(sheet + index) % len(PROPORTIONAL_CONTEXTS)]
    start = rng.randint(2, 6)
    target = rng.choice([value for value in range(4, 13) if value != start])
    per_item = rng.randint(2, 10)
    amount = start * per_item
    result = target * per_item
    if kind == "cost":
        prompt = f"{start} {noun} kosten {amount} €. Wie viel kosten {target} {noun}?"
    elif kind == "need":
        prompt = f"Für {start} {noun} braucht man {amount} {unit}. Wie viele {unit} braucht man für {target} {noun}?"
    elif kind == "time":
        prompt = f"Für {start} {noun} braucht man {amount} Minuten. Wie viele Minuten braucht man für {target} {noun}?"
    elif kind == "weight":
        prompt = f"{start} {noun} wiegen zusammen {amount} kg. Wie viel wiegen {target} {noun}?"
    elif kind == "contain":
        prompt = f"{start} {noun} enthalten {amount} {unit}. Wie viele {unit} sind in {target} {noun}?"
    elif kind == "read":
        prompt = f"In {start} Tagen liest man {amount} Seiten. Wie viele Seiten liest man in {target} Tagen?"
    else:
        prompt = f"In {start} Runden erreicht man {amount} Punkte. Wie viele Punkte sind es in {target} Runden?"
    return task(prompt, f"{result} {unit}")


POLYGON_NAMES = {3: "Dreieck", 4: "Viereck", 5: "Fünfeck", 6: "Sechseck", 7: "Siebeneck",
                 8: "Achteck", 9: "Neuneck", 10: "Zehneck", 12: "Zwölfeck"}

PLANE_FACTS = [
    ("Wie heißt ein Viereck mit vier gleich langen Seiten und vier rechten Winkeln?", "Quadrat", "square"),
    ("Wie viele Spiegelachsen hat ein Rechteck, das kein Quadrat ist?", "2", "rectangle"),
    ("Wie heißt ein Dreieck mit drei gleich langen Seiten?", "gleichseitiges Dreieck", "triangle"),
    ("Wie heißt ein Viereck mit genau einem Paar paralleler Seiten?", "Trapez", "trapezoid"),
    ("Wie viele Spiegelachsen hat ein Quadrat?", "4", "square"),
    ("Wie heißt eine ebene Figur ohne Ecken?", "Kreis", "circle"),
    ("Wie heißt ein Viereck mit gegenüberliegenden parallelen Seiten?", "Parallelogramm", "parallelogram"),
    ("Wie viele Spiegelachsen hat ein gleichseitiges Dreieck?", "3", "triangle"),
    ("Wie heißt ein Viereck mit vier gleich langen Seiten?", "Raute", "rhombus"),
    ("Wie viele Spiegelachsen hat ein gleichschenkliges Dreieck?", "1", "triangle"),
    ("Wie viele Diagonalen hat ein Viereck?", "2", "quadrilateral"),
    ("Wie heißt die längste Seite im rechtwinkligen Dreieck?", "Hypotenuse", "right_triangle"),
    ("Wie heißt die Strecke vom Kreismittelpunkt zum Rand?", "Radius", "circle"),
    ("Wie heißt die Strecke durch den Mittelpunkt von Kreisrand zu Kreisrand?", "Durchmesser", "circle"),
    ("Wie viele Spiegelachsen hat ein ungleichseitiges Dreieck?", "0", "triangle"),
]


def plane_task(rng: random.Random, sheet: int, index: int) -> dict:
    mode = (sheet + index) % 3
    if mode == 0:
        sides = rng.choice(sorted(POLYGON_NAMES))
        return task(f"Wie viele Seiten hat ein {POLYGON_NAMES[sides]}?", str(sides), kind="shape", shape=f"poly{sides}")
    if mode == 1:
        sides = rng.choice(sorted(POLYGON_NAMES))
        return task(f"Wie heißt ein Vieleck mit {sides} Seiten?", POLYGON_NAMES[sides], kind="shape", shape=f"poly{sides}")
    text, answer, shape = PLANE_FACTS[(sheet * 10 + index) % len(PLANE_FACTS)]
    return task(text, answer, kind="shape", shape=shape)


SOLID_FACTS = [
    ("Wie viele Ecken hat ein Würfel?", "8", "cube"),
    ("Wie viele Kanten hat ein Würfel?", "12", "cube"),
    ("Wie viele Flächen hat ein Würfel?", "6", "cube"),
    ("Wie viele Ecken hat eine quadratische Pyramide?", "5", "pyramid"),
    ("Wie viele Kanten hat eine quadratische Pyramide?", "8", "pyramid"),
    ("Wie viele Flächen hat eine quadratische Pyramide?", "5", "pyramid"),
    ("Welcher Körper hat keine Ecken und keine Kanten?", "Kugel", "sphere"),
    ("Wie viele Ecken hat ein Quader?", "8", "cuboid"),
    ("Wie viele Kanten hat ein Quader?", "12", "cuboid"),
    ("Wie viele Flächen hat ein Quader?", "6", "cuboid"),
    ("Welcher Körper hat zwei Kreisflächen und eine gekrümmte Fläche?", "Zylinder", "cylinder"),
    ("Welcher Körper hat eine Kreisfläche und eine Spitze?", "Kegel", "cone"),
    ("Wie viele Ecken hat eine dreieckige Pyramide?", "4", "tetra"),
    ("Wie viele Kanten hat eine dreieckige Pyramide?", "6", "tetra"),
    ("Wie viele Flächen hat eine dreieckige Pyramide?", "4", "tetra"),
]


def solid_task(rng: random.Random, sheet: int, index: int) -> dict:
    mode = (sheet * 10 + index) % 5
    if mode == 0:
        count = rng.randint(2, 7)
        return task(f"{count} Würfel stehen getrennt. Wie viele Ecken haben sie zusammen?", str(count * 8), kind="solid", shape="")
    if mode == 1:
        count = rng.randint(2, 7)
        return task(f"{count} Würfel stehen in einer geraden Reihe. Wie viele Flächen sind außen sichtbar?", str(4 * count + 2), kind="solid", shape="")
    text, answer, shape = SOLID_FACTS[(sheet * 10 + index) % len(SOLID_FACTS)]
    return task(text, answer, kind="solid", shape=shape)


GENERATORS = [addition_task, multiplication_task, division_task, unit_task, estimate_task,
              ratio_task, chart_task, proportional_task, plane_task, solid_task]


def make_tasks(category: int, sheet: int) -> list[dict]:
    rng = random.Random(100_000 + category * 10_000 + sheet)
    generator = GENERATORS[category - 1]
    tasks: list[dict] = []
    seen: set[str] = set()
    for index in range(10):
        for attempt in range(50):
            item = generator(rng, sheet, index + attempt * 13)
            if item["kind"] == "chart":
                unique_key = f'{item["text"]}|{item["values"]}'
            elif item["kind"] == "ratio":
                unique_key = f'{item["text"]}|{item["filled"]}/{item["total"]}'
            else:
                unique_key = item["text"]
            if unique_key not in seen:
                tasks.append(item)
                seen.add(unique_key)
                break
        else:
            raise RuntimeError(f"Keine eindeutige Aufgabe für Typ {category}, Blatt {sheet}, Nr. {index + 1}")
    return tasks


def draw_number(c: canvas.Canvas, number: int, x: float, y: float) -> None:
    c.setFillColor(NAVY)
    c.circle(x, y, 3.7 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DejaVu-Bold", 8)
    c.drawCentredString(x, y - 2.7, str(number))


def draw_ratio(c: canvas.Canvas, item: dict, x: float, y: float, width: float) -> None:
    total = item["total"]
    filled = item["filled"]
    gap = 1.1 * mm
    cell = min(6 * mm, (width - (total - 1) * gap) / total)
    start = x + max(0, (width - (cell * total + gap * (total - 1))) / 2)
    for i in range(total):
        c.setFillColor(BLUE if i < filled else white)
        c.setStrokeColor(BLUE if i < filled else MUTED)
        c.roundRect(start + i * (cell + gap), y, cell, cell, 1.2 * mm, fill=1, stroke=1)


def draw_chart(c: canvas.Canvas, item: dict, x: float, y: float, width: float, height: float) -> None:
    labels = item["labels"]
    values = item["values"]
    maximum = max(values)
    left = x + 7 * mm
    base = y + 5 * mm
    chart_w = width - 12 * mm
    chart_h = height - 8 * mm
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.7)
    c.line(left, base, left, base + chart_h)
    c.line(left, base, left + chart_w, base)
    bar_w = 9 * mm
    gap = (chart_w - 3 * bar_w) / 4
    for i, (label, value) in enumerate(zip(labels, values)):
        bx = left + gap + i * (bar_w + gap)
        bh = max(3 * mm, chart_h * value / maximum)
        c.setFillColor(BLUE)
        c.roundRect(bx, base, bar_w, bh, 1.4 * mm, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("DejaVu-Bold", 6.8)
        c.drawCentredString(bx + bar_w / 2, base - 3.2 * mm, label)
        if item["show_values"]:
            c.drawCentredString(bx + bar_w / 2, base + bh + 1.2 * mm, str(value))


def draw_polygon(c: canvas.Canvas, shape: str, x: float, y: float, size: float) -> None:
    c.setStrokeColor(BLUE)
    c.setFillColor(Color(BLUE.red, BLUE.green, BLUE.blue, alpha=0.08))
    c.setLineWidth(1.5)
    cx, cy = x + size / 2, y + size / 2
    if shape == "circle":
        c.circle(cx, cy, size * 0.38, fill=1, stroke=1)
        return
    sides = 4
    if shape.startswith("poly"):
        sides = int(shape[4:])
    elif shape in {"triangle", "right_triangle"}:
        sides = 3
    elif shape in {"square", "rectangle", "trapezoid", "parallelogram", "rhombus", "quadrilateral"}:
        sides = 4
    points = []
    for i in range(sides):
        angle = math.pi / 2 + i * 2 * math.pi / sides
        points.extend([cx + math.cos(angle) * size * 0.38, cy + math.sin(angle) * size * 0.38])
    path = c.beginPath()
    path.moveTo(points[0], points[1])
    for i in range(2, len(points), 2):
        path.lineTo(points[i], points[i + 1])
    path.close()
    c.drawPath(path, fill=1, stroke=1)


def draw_solid(c: canvas.Canvas, shape: str, x: float, y: float, size: float) -> None:
    if not shape:
        return
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.4)
    c.setFillColor(Color(BLUE.red, BLUE.green, BLUE.blue, alpha=0.06))
    if shape == "sphere":
        c.circle(x + size / 2, y + size / 2, size * 0.38, fill=1, stroke=1)
        c.ellipse(x + size * .12, y + size * .40, x + size * .88, y + size * .60, fill=0, stroke=1)
    elif shape in {"cylinder", "cone"}:
        c.ellipse(x + size * .15, y + size * .12, x + size * .85, y + size * .35, fill=1, stroke=1)
        if shape == "cylinder":
            c.ellipse(x + size * .15, y + size * .65, x + size * .85, y + size * .88, fill=1, stroke=1)
            c.line(x + size * .15, y + size * .235, x + size * .15, y + size * .765)
            c.line(x + size * .85, y + size * .235, x + size * .85, y + size * .765)
        else:
            c.line(x + size * .15, y + size * .235, x + size * .50, y + size * .90)
            c.line(x + size * .85, y + size * .235, x + size * .50, y + size * .90)
    elif shape in {"pyramid", "tetra"}:
        c.line(x + size * .15, y + size * .18, x + size * .85, y + size * .18)
        c.line(x + size * .15, y + size * .18, x + size * .50, y + size * .88)
        c.line(x + size * .85, y + size * .18, x + size * .50, y + size * .88)
        c.line(x + size * .50, y + size * .88, x + size * .50, y + size * .40)
    else:
        offset = size * .20
        c.rect(x + size * .10, y + size * .10, size * .58, size * .58, fill=1, stroke=1)
        c.rect(x + size * .28, y + size * .28, size * .58, size * .58, fill=0, stroke=1)
        for px, py in [(x + size * .10, y + size * .10), (x + size * .68, y + size * .10),
                       (x + size * .68, y + size * .68), (x + size * .10, y + size * .68)]:
            c.line(px, py, px + offset * .9, py + offset * .9)


def draw_standard_page(c: canvas.Canvas, tasks: list[dict], category: int) -> None:
    width, height = A4
    top = height - 43 * mm
    row_h = 22.6 * mm
    for i, item in enumerate(tasks):
        row_top = top - i * row_h
        draw_number(c, i + 1, 20 * mm, row_top - 5 * mm)
        text_width = 145 * mm if item["kind"] in {"shape", "solid"} else 166 * mm
        draw_wrapped(c, item["text"], 29 * mm, row_top - 2.5 * mm, text_width,
                     size=10.4 if len(item["text"]) < 95 else 9.5, leading=12, max_lines=2)
        if item["kind"] == "ratio":
            draw_ratio(c, item, 67 * mm, row_top - 17.5 * mm, 92 * mm)
        elif item["kind"] == "shape":
            draw_polygon(c, item["shape"], width - 31 * mm, row_top - 19 * mm, 16 * mm)
        elif item["kind"] == "solid":
            draw_solid(c, item["shape"], width - 31 * mm, row_top - 19 * mm, 16 * mm)
        c.setStrokeColor(GRID)
        c.setDash(1.5, 2.5)
        c.line(29 * mm, row_top - 19.2 * mm, width - 15 * mm, row_top - 19.2 * mm)
        c.setDash()


def draw_chart_page(c: canvas.Canvas, tasks: list[dict]) -> None:
    width, height = A4
    cell_w = 88 * mm
    cell_h = 43.5 * mm
    top = height - 42 * mm
    for i, item in enumerate(tasks):
        col = i % 2
        row = i // 2
        x = 13 * mm + col * 96 * mm
        y_top = top - row * cell_h
        c.setStrokeColor(GRID)
        c.roundRect(x, y_top - 39.5 * mm, cell_w, 39 * mm, 2.5 * mm, fill=0, stroke=1)
        draw_number(c, i + 1, x + 6 * mm, y_top - 6 * mm)
        draw_wrapped(c, item["text"], x + 12 * mm, y_top - 3.8 * mm, cell_w - 15 * mm,
                     size=7.9, leading=9.2, max_lines=2)
        draw_chart(c, item, x + 3 * mm, y_top - 37 * mm, cell_w - 6 * mm, 24 * mm)


def draw_solution_page(c: canvas.Canvas, category: int, start_sheet: int,
                       answers: list[list[str]], page_no: int, total_pages: int) -> None:
    page_size = landscape(A4)
    c.setPageSize(page_size)
    width, height = page_size
    c.setFillColor(NAVY)
    c.rect(0, height - 23 * mm, width, 23 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DejaVu-Bold", 10)
    c.drawString(14 * mm, height - 9 * mm, "LÖSUNGEN · 1 BIS 10")
    c.setFont("DejaVu-Bold", 16)
    c.drawString(14 * mm, height - 17 * mm, DISPLAY_CATEGORIES[category - 1])
    c.setFont("DejaVu", 8)
    c.drawRightString(width - 14 * mm, height - 16 * mm, f"Übungsblätter {start_sheet}-{start_sheet + 9}")

    left = 12 * mm
    table_top = height - 34 * mm
    table_width = width - 24 * mm
    first_w = 18 * mm
    cell_w = (table_width - first_w) / 10
    row_h = 13.2 * mm
    header_h = 9 * mm
    c.setFillColor(SKY)
    c.rect(left, table_top - header_h, table_width, header_h, fill=1, stroke=0)
    c.setStrokeColor(GRID)
    c.setLineWidth(0.5)
    c.setFont("DejaVu-Bold", 7.5)
    c.setFillColor(NAVY)
    c.drawCentredString(left + first_w / 2, table_top - 6 * mm, "Blatt")
    for col in range(10):
        c.drawCentredString(left + first_w + col * cell_w + cell_w / 2, table_top - 6 * mm, str(col + 1))

    for row in range(10):
        y_top = table_top - header_h - row * row_h
        if row % 2 == 1:
            c.setFillColor(HexColor("#f5f8fb"))
            c.rect(left, y_top - row_h, table_width, row_h, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("DejaVu-Bold", 7.2)
        c.drawCentredString(left + first_w / 2, y_top - 7.5 * mm, str(start_sheet + row))
        row_answers = answers[start_sheet - 1 + row]
        for col, answer in enumerate(row_answers):
            cx = left + first_w + col * cell_w
            lines = wrap_text(str(answer), "DejaVu", 5.7, cell_w - 2.2 * mm)[:2]
            c.setFont("DejaVu", 5.7)
            c.setFillColor(INK)
            for line_no, line in enumerate(lines):
                c.drawCentredString(cx + cell_w / 2, y_top - 5.8 * mm - line_no * 2.7 * mm, line)

    total_h = header_h + 10 * row_h
    x_positions = [left, left + first_w] + [left + first_w + i * cell_w for i in range(1, 11)]
    for x in x_positions:
        c.line(x, table_top, x, table_top - total_h)
    c.line(left + table_width, table_top, left + table_width, table_top - total_h)
    c.line(left, table_top, left + table_width, table_top)
    c.line(left, table_top - header_h, left + table_width, table_top - header_h)
    for row in range(1, 11):
        y = table_top - header_h - row * row_h
        c.line(left, y, left + table_width, y)

    c.setFillColor(MUTED)
    c.setFont("DejaVu", 7.5)
    c.drawString(12 * mm, 8 * mm, f"Lösungen · Aufgabentyp {category} von 10")
    c.drawRightString(width - 12 * mm, 8 * mm, f"Seite {page_no} von {total_pages}")


def build_pdf() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    total_pages = 440
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle("1 bis 10 - Übungsheft Klasse 6")
    c.setAuthor("1 bis 10")
    c.setSubject("4.000 Kopfrechen- und Mathematikaufgaben für Klasse 6")
    all_answers: list[list[list[str]]] = []
    page_no = 0

    for category in range(1, 11):
        category_answers: list[list[str]] = []
        for sheet in range(1, 41):
            page_no += 1
            tasks = make_tasks(category, sheet)
            category_answers.append([item["answer"] for item in tasks])
            draw_header(c, category, sheet, page_no, total_pages)
            if category == 7:
                draw_chart_page(c, tasks)
            else:
                draw_standard_page(c, tasks, category)
            c.showPage()
        all_answers.append(category_answers)

    for category in range(1, 11):
        for start_sheet in (1, 11, 21, 31):
            page_no += 1
            draw_solution_page(c, category, start_sheet, all_answers[category - 1], page_no, total_pages)
            c.showPage()

    if page_no != total_pages:
        raise RuntimeError(f"Erwartet: {total_pages} Seiten, erzeugt: {page_no}")
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
