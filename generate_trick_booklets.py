#!/usr/bin/env python3
"""Erzeugt zehn kurze Rechentricks-Heftchen im A5-Format."""

from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "pdf" / "rechentricks"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = HexColor("#17324d")
BLUE = HexColor("#2e6f9e")
SKY = HexColor("#dcecf5")
PALE = HexColor("#f5f8fb")
INK = HexColor("#17212b")
MUTED = HexColor("#667482")
GRID = HexColor("#d7e0e7")
RED = HexColor("#d94b45")


def st(title, explain, steps, example, mini):
    return {"title": title, "explain": explain, "steps": steps, "example": example, "mini": mini}


BOOKLETS = [
    {
        "title": "Addition und Subtraktion", "slug": "01-addition-subtraktion",
        "subtitle": "Zahlen geschickt zerlegen und ausgleichen",
        "strategies": [
            st("Zehner zuerst", "Zerlege die zweite Zahl in Zehner und Einer. So bleibt jeder Schritt klein.",
               ["Addiere oder subtrahiere zuerst die Zehner.", "Rechne danach mit den Einern."],
               ["47 + 26", "47 + 20 = 67", "67 + 6 = 73"], [("56 + 23", "79"), ("84 - 32", "52")]),
            st("Zum vollen Zehner", "Runde eine Zahl kurz auf einen vollen Zehner. Gleiche die Änderung danach aus.",
               ["38 + 27: Mache aus 38 eine 40.", "Nimm dafür bei 27 die 2 weg."],
               ["38 + 27", "40 + 25 = 65"], [("49 + 36", "85"), ("63 - 28", "35")]),
            st("Passende Paare", "Suche Zahlen, die zusammen 10, 100 oder 1000 ergeben.",
               ["Du darfst Summanden vertauschen.", "Fasse zuerst das passende Paar zusammen."],
               ["25 + 17 + 75", "25 + 75 + 17", "100 + 17 = 117"], [("36 + 64 + 19", "119"), ("125 + 38 + 75", "238")]),
            st("Beide Zahlen verschieben", "Bei einer Subtraktion bleibt der Abstand gleich, wenn du beide Zahlen gleich veränderst.",
               ["Verschiebe beide Zahlen zum leichteren Nachbarn.", "Rechne die neue, gleich große Differenz."],
               ["84 - 29", "85 - 30 = 55"], [("73 - 19", "54"), ("142 - 98", "44")]),
            st("Überschlag als Kontrolle", "Runde grob. Dein genaues Ergebnis muss in der Nähe liegen.",
               ["Runde auf Zehner oder Hunderter.", "Vergleiche Überschlag und genaues Ergebnis."],
               ["198 + 304 ist ungefähr", "200 + 300 = 500", "Genau: 502"], [("397 + 205 ungefähr", "600"), ("612 - 289 ungefähr", "300")]),
        ],
        "practice": [("68 + 27", "95"), ("94 - 38", "56"), ("125 + 75 + 46", "246"),
                     ("73 - 29", "44"), ("240 + 185", "425"), ("502 - 198", "304"),
                     ("36 + 64 + 28", "128"), ("315 - 97", "218"),
                     ("Wie groß ist der Überschlag für 398 + 204?", "600"),
                     ("Ein Team hat 75 Punkte, gewinnt 28 und verliert 19. Endstand?", "84 Punkte")],
    },
    {
        "title": "Multiplikation", "slug": "02-multiplikation",
        "subtitle": "Malaufgaben auf bekannte Aufgaben zurückführen",
        "strategies": [
            st("Tauschaufgaben", "Beim Multiplizieren darfst du die Faktoren vertauschen.",
               ["Wähle die Reihenfolge, die leichter ist.", "Das Ergebnis bleibt gleich."],
               ["4 · 18 = 18 · 4", "18 · 2 = 36", "36 · 2 = 72"], [("25 · 4", "100"), ("6 · 17", "102")]),
            st("Zerlegen", "Zerlege einen Faktor in einfache Teile und addiere die Teilprodukte.",
               ["Zerlege zum Beispiel 14 in 10 + 4.", "Multipliziere beide Teile."],
               ["7 · 14", "7 · 10 + 7 · 4", "70 + 28 = 98"], [("6 · 13", "78"), ("8 · 16", "128")]),
            st("Mal 5", "Mal 5 ist die Hälfte von mal 10.",
               ["Multipliziere zuerst mit 10.", "Halbiere danach das Ergebnis."],
               ["18 · 5", "18 · 10 = 180", "180 : 2 = 90"], [("24 · 5", "120"), ("36 · 5", "180")]),
            st("Mal 9", "Mal 9 ist einmal die Zahl weniger als mal 10.",
               ["Rechne zuerst mal 10.", "Ziehe den ursprünglichen Faktor einmal ab."],
               ["13 · 9", "13 · 10 - 13", "130 - 13 = 117"], [("16 · 9", "144"), ("27 · 9", "243")]),
            st("Verdoppeln und halbieren", "Halbiere einen geraden Faktor und verdopple den anderen. Das Produkt bleibt gleich.",
               ["Suche einen geraden Faktor.", "Wiederhole den Trick, wenn es noch leichter wird."],
               ["16 · 5", "8 · 10 = 80"], [("14 · 5", "70"), ("25 · 12", "300")]),
        ],
        "practice": [("7 · 16", "112"), ("18 · 5", "90"), ("14 · 9", "126"), ("25 · 8", "200"),
                     ("6 · 17", "102"), ("12 · 15", "180"), ("□ · 8 = 136", "17"),
                     ("19 · 7", "133"), ("24 · 5", "120"), ("16 · 14", "224")],
    },
    {
        "title": "Division", "slug": "03-division",
        "subtitle": "Geteiltaufgaben mit Malaufgaben und Zerlegen lösen",
        "strategies": [
            st("Die Umkehraufgabe", "Frage dich: Welche Zahl mal dem Teiler ergibt die erste Zahl?",
               ["Verwandle die Geteiltaufgabe in eine Malaufgabe.", "Nutze das Einmaleins."],
               ["84 : 7 = ?", "7 · ? = 84", "7 · 12 = 84"], [("96 : 8", "12"), ("132 : 11", "12")]),
            st("Passend zerlegen", "Zerlege die erste Zahl in Teile, die sich leicht teilen lassen.",
               ["Beide Teile müssen durch den Teiler teilbar sein.", "Addiere die Teilergebnisse."],
               ["156 : 12", "120 : 12 + 36 : 12", "10 + 3 = 13"], [("144 : 8", "18"), ("175 : 7", "25")]),
            st("Nullen nutzen", "Teile zuerst die Zahl ohne die angehängten Nullen und hänge passende Nullen wieder an.",
               ["Achte darauf, wie viele Nullen übrig bleiben.", "Mache die Malprobe."],
               ["240 : 6", "24 : 6 = 4", "also 240 : 6 = 40"], [("350 : 7", "50"), ("480 : 12", "40")]),
            st("Beide Zahlen halbieren", "Du darfst Dividend und Divisor durch dieselbe Zahl teilen.",
               ["Halbiere beide Zahlen.", "Wiederhole, wenn es noch leichter wird."],
               ["84 : 6", "42 : 3 = 14"], [("144 : 12", "12"), ("160 : 8", "20")]),
            st("Mit der Malprobe prüfen", "Multipliziere Ergebnis und Teiler. Du musst wieder die erste Zahl erhalten.",
               ["Ergebnis · Teiler = Dividend.", "Passt es nicht, suche den Rechenfehler."],
               ["168 : 8 = 21", "Probe: 21 · 8 = 168"], [("225 : 9", "25"), ("288 : 12", "24")]),
        ],
        "practice": [("126 : 9", "14"), ("144 : 12", "12"), ("175 : 7", "25"), ("216 : 12", "18"),
                     ("240 : 6", "40"), ("256 : 8", "32"), ("□ : 7 = 28", "196"),
                     ("396 : 11", "36"), ("450 : 9", "50"), ("525 : 7", "75")],
    },
    {
        "title": "Einheiten", "slug": "04-einheiten",
        "subtitle": "Länge, Gewicht, Inhalt und Zeit sicher umrechnen",
        "strategies": [
            st("Erst die Richtung", "Prüfe zuerst: Wird die Einheit kleiner oder größer?",
               ["Kleinere Einheit: Die Zahl wird größer.", "Größere Einheit: Die Zahl wird kleiner."],
               ["3 m = 300 cm", "Die Einheit cm ist kleiner.", "Darum wird die Zahl größer."], [("5 km in m", "5000 m"), ("800 cm in m", "8 m")]),
            st("Längenleiter", "Bei mm, cm, dm und m ist jeder Nachbarschritt mal 10 oder geteilt durch 10.",
               ["mm - cm - dm - m", "km und m unterscheiden sich um den Faktor 1000."],
               ["4,5 m = 45 dm", "4,5 m = 450 cm"], [("7 dm in cm", "70 cm"), ("3200 mm in m", "3,2 m")]),
            st("Gewichte merken", "1 kg sind 1000 g. Ein Zentner sind 50 kg. Eine Tonne sind 1000 kg.",
               ["Schreibe den passenden Faktor auf.", "Prüfe die Richtung."],
               ["3 Zentner", "3 · 50 kg = 150 kg"], [("6 kg in g", "6000 g"), ("8 Zentner in kg", "400 kg")]),
            st("Liter und Milliliter", "1 Liter sind 1000 Milliliter. 100 Zentiliter sind 1 Liter.",
               ["l zu ml: mal 1000.", "ml zu l: geteilt durch 1000."],
               ["2,5 l = 2500 ml", "4500 ml = 4,5 l"], [("7 l in ml", "7000 ml"), ("1250 ml in l", "1,25 l")]),
            st("Zeit rechnet mit 60", "Zeit ist anders: 1 Stunde sind 60 Minuten und 1 Minute sind 60 Sekunden.",
               ["h zu min: mal 60.", "min zu s: mal 60."],
               ["2 h 15 min", "120 min + 15 min", "= 135 min"], [("3 min 20 s in s", "200 s"), ("1 h 40 min in min", "100 min")]),
        ],
        "practice": [("4 km = ____ m", "4000 m"), ("650 cm = ____ m", "6,5 m"),
                     ("3,2 m = ____ cm", "320 cm"), ("5 kg = ____ g", "5000 g"),
                     ("6 Zentner = ____ kg", "300 kg"), ("2 l = ____ ml", "2000 ml"),
                     ("7500 ml = ____ l", "7,5 l"), ("4 h = ____ min", "240 min"),
                     ("5 min 30 s = ____ s", "330 s"), ("2 h 25 min = ____ min", "145 min")],
    },
    {
        "title": "Schätzen", "slug": "05-schaetzen",
        "subtitle": "Schnell erkennen, was ungefähr stimmen kann",
        "strategies": [
            st("Auf einfache Zahlen runden", "Runde auf Zehner oder Hunderter, mit denen du leicht rechnen kannst.",
               ["Schau auf die nächste Stelle.", "0 bis 4: abrunden. 5 bis 9: aufrunden."],
               ["198 + 305", "200 + 300", "ungefähr 500"], [("397 + 202", "ungefähr 600"), ("603 - 298", "ungefähr 300")]),
            st("Passende Nachbarzahlen", "Manchmal sind nahe Zahlen besser als normales Runden.",
               ["Suche eine leichte Mal- oder Geteiltaufgabe.", "Das Ergebnis ist ein Näherungswert."],
               ["49 · 21", "50 · 20", "ungefähr 1000"], [("79 · 11", "ungefähr 900"), ("24 · 39", "ungefähr 1000")]),
            st("Alltagsanker", "Merke dir einige Größen aus deinem Alltag.",
               ["Tür: etwa 2 m.", "Schulranzen: etwa 4 kg.", "Unterrichtsstunde: 45 min."],
               ["Eine Badewanne fasst", "ungefähr 200 Liter."], [("Höhe eines Esstischs", "etwa 75 cm"), ("Länge eines Bleistifts", "etwa 20 cm")]),
            st("Viel zu klein oder zu groß?", "Streiche zuerst unmögliche Antworten. Oft bleibt nur eine sinnvolle übrig.",
               ["Vergleiche mit einem bekannten Gegenstand.", "Achte besonders auf die Einheit."],
               ["Ein Bus ist nicht 1 m lang", "und nicht 120 m lang.", "12 m passt."], [("Gewicht einer Büroklammer", "etwa 1 g"), ("Länge eines Fußballfelds", "etwa 100 m")]),
            st("Mit Grenzen prüfen", "Überlege, zwischen welchen zwei Zahlen das Ergebnis liegen muss.",
               ["Runde einmal nach unten.", "Runde einmal nach oben."],
               ["39 · 51 liegt zwischen", "30 · 50 und 40 · 60", "also nahe bei 2000"], [("151 · 6 ungefähr", "900"), ("498 + 503 ungefähr", "1000")]),
        ],
        "practice": [("49 · 21 liegt näher bei 100, 1000 oder 10000?", "1000"),
                     ("198 + 305 liegt näher bei 50, 500 oder 5000?", "500"),
                     ("Wie hoch ist ungefähr eine Zimmertür?", "2 m"),
                     ("Wie schwer ist ungefähr ein Apfel?", "200 g"),
                     ("603 - 298 liegt näher bei 30, 300 oder 3000?", "300"),
                     ("Wie viel fasst ungefähr ein Trinkglas?", "200 ml"),
                     ("39 · 51 liegt näher bei 200, 2000 oder 20000?", "2000"),
                     ("Wie lang ist ungefähr ein Linienbus?", "12 m"),
                     ("1002 - 497 liegt näher bei 50, 500 oder 5000?", "500"),
                     ("Wie schwer ist ungefähr ein erwachsener Mensch?", "70 kg")],
    },
    {
        "title": "Verhältnisse", "slug": "06-verhaeltnisse",
        "subtitle": "Anteile sehen, kürzen und vergleichen",
        "strategies": [
            st("Teil und Ganzes", "Beim Bruch zählt oben der markierte Teil und unten die Zahl aller gleich großen Teile.",
               ["Zähle zuerst alle Teile.", "Zähle danach die markierten Teile."],
               ["3 von 5 Feldern sind blau", "Anteil: 3/5"], [("2 von 7 Feldern", "2/7"), ("6 von 10 Feldern", "6/10")]),
            st("Reihenfolge beachten", "Bei 2 : 5 steht zuerst der erste Anteil und danach der zweite.",
               ["Lies von links nach rechts.", "Vertauschen verändert das Verhältnis."],
               ["2 rote zu 5 blauen Kugeln", "2 : 5"], [("4 Äpfel zu 3 Birnen", "4 : 3"), ("1 blau zu 6 rot", "1 : 6")]),
            st("Beide Zahlen kürzen", "Teile beide Zahlen durch dieselbe Zahl. Das Verhältnis bleibt gleich.",
               ["Suche einen gemeinsamen Teiler.", "Teile links und rechts."],
               ["6 : 9", "beide durch 3", "2 : 3"], [("8 : 12", "2 : 3"), ("15 : 20", "3 : 4")]),
            st("Beide Zahlen erweitern", "Multipliziere beide Zahlen mit derselben Zahl.",
               ["Der Zusammenhang bleibt gleich.", "Nutze den Trick zum Vergleichen."],
               ["2 : 3", "beide mal 4", "8 : 12"], [("3 : 5 mit 3 erweitern", "9 : 15"), ("1 : 4 mit 5 erweitern", "5 : 20")]),
            st("Gleiche Verhältnisse erkennen", "Kürze beide Verhältnisse vollständig. Sind die Ergebnisse gleich, passen sie zusammen.",
               ["Kürze die linke Seite.", "Kürze die rechte Seite.", "Vergleiche."],
               ["4 : 6 und 10 : 15", "2 : 3 und 2 : 3", "also gleich"], [("6 : 8 und 9 : 12", "gleich"), ("4 : 10 und 6 : 15", "gleich")]),
        ],
        "practice": [("Kürze 6 : 8.", "3 : 4"), ("Kürze 12 : 18.", "2 : 3"),
                     ("Welcher Bruch beschreibt 4 von 10 Feldern, vollständig gekürzt?", "2/5"),
                     ("Erweitere 2 : 5 mit 4.", "8 : 20"), ("Kürze 14 : 21.", "2 : 3"),
                     ("Sind 8 : 12 und 10 : 15 gleich?", "ja"),
                     ("5 rote zu 3 blauen Kugeln. Verhältnis rot : blau?", "5 : 3"),
                     ("Kürze 18 : 24.", "3 : 4"), ("Erweitere 3 : 4 mit 5.", "15 : 20"),
                     ("Welcher gekürzte Bruch beschreibt 6 von 9 Feldern?", "2/3")],
    },
    {
        "title": "Diagramme", "slug": "07-diagramme",
        "subtitle": "Werte sicher lesen und richtig vergleichen",
        "strategies": [
            st("Erst Überschrift und Achsen", "Bevor du rechnest, kläre: Was wird gezeigt und welche Einheit wird benutzt?",
               ["Lies die Überschrift.", "Lies beide Achsen und ihre Einheiten."],
               ["Tage stehen unten.", "Anzahl steht links.", "Dann erst liest du Werte ab."], [("Wo stehen meist die Gruppen?", "auf der waagerechten Achse"), ("Wo stehen meist die Werte?", "auf der senkrechten Achse")]),
            st("Die Schrittweite finden", "Nicht jeder Strich bedeutet 1. Prüfe die Zahlen an der Achse.",
               ["Nimm zwei beschriftete Striche.", "Bestimme den Abstand."],
               ["0, 5, 10, 15", "Ein Schritt bedeutet 5."], [("0, 10, 20: Schrittweite?", "10"), ("0, 2, 4, 6: Schrittweite?", "2")]),
            st("Höchste und tiefste Werte", "Vergleiche die Höhe der Balken oder Punkte. Es kann mehrere gleiche Maxima geben.",
               ["Suche den höchsten Wert.", "Prüfe, ob noch ein Wert gleich hoch ist."],
               ["Mo: 7, Di: 4, Mi: 7", "Maximum: Mo und Mi"], [("3, 8, 5: größter Wert", "8"), ("6, 2, 2: kleinste Stellen", "2. und 3. Stelle")]),
            st("Summe und Unterschied", "Bei der Summe addierst du alle gefragten Werte. Beim Unterschied rechnest du groß minus klein.",
               ["Schreibe die benötigten Werte auf.", "Achte auf das Rechenwort."],
               ["4, 7 und 3", "Summe: 14", "Unterschied: 7 - 3 = 4"], [("2, 6, 5: Summe", "13"), ("9, 4, 7: Unterschied", "5")]),
            st("Am Ende prüfen", "Deine Antwort braucht oft einen Namen, einen Tag oder eine Einheit, nicht nur eine Zahl.",
               ["Lies die Frage noch einmal.", "Formuliere die Antwort passend."],
               ["Nicht nur: 8", "Sondern: Am Dienstag sind es 8."], [("Gefragt ist ein Tag. Was muss in die Antwort?", "der Tag"), ("Gefragt sind Liter. Was muss dazu?", "die Einheit Liter")]),
        ],
        "practice": [("Mo 3, Di 8, Mi 5: An welchem Tag ist der Wert am größten?", "Di"),
                     ("Mo 6, Di 6, Mi 2: An welchen Tagen ist der Wert am größten?", "Mo und Di"),
                     ("Werte 4, 7, 3: Summe?", "14"), ("Werte 9, 4, 7: Unterschied?", "5"),
                     ("Achse: 0, 5, 10, 15. Schrittweite?", "5"),
                     ("Werte 8, 3, 6: kleinster Wert?", "3"),
                     ("Werte 5, 5, 5: Summe?", "15"),
                     ("Werte 7, 4, 7: Wie viele Maxima gibt es?", "2"),
                     ("Werte 2, 8, 5: Unterschied?", "6"),
                     ("Welche Achse zeigt meist die Werte?", "die senkrechte Achse")],
    },
    {
        "title": "Zwei- und Dreisatz", "slug": "08-zwei-dreisatz",
        "subtitle": "Erst auf 1, dann auf die gesuchte Menge",
        "strategies": [
            st("Der sichere Weg über 1", "Finde zuerst den Wert für eine Einheit. Rechne danach zur gesuchten Menge.",
               ["Teile durch die bekannte Anzahl.", "Multipliziere mit der gesuchten Anzahl."],
               ["3 Brezeln kosten 6 €", "1 Brezel kostet 2 €", "5 Brezeln kosten 10 €"], [("4 Hefte kosten 8 €. 7 Hefte?", "14 €"), ("5 Äpfel kosten 15 €. 8 Äpfel?", "24 €")]),
            st("Beide Seiten gleich verändern", "Wenn du links teilst oder malnimmst, musst du rechts genau dasselbe tun.",
               ["Schreibe beide Größen nebeneinander.", "Nutze auf beiden Seiten denselben Rechenschritt."],
               ["4 Stück - 12 €", "2 Stück - 6 €", "6 Stück - 18 €"], [("3 kg kosten 12 €. 6 kg?", "24 €"), ("8 Flaschen kosten 24 €. 4 Flaschen?", "12 €")]),
            st("Verdoppeln", "Ist die gesuchte Menge doppelt so groß, verdopple auch den Wert.",
               ["Vergleiche bekannte und gesuchte Menge.", "Nutze den direkten Faktor."],
               ["4 Karten kosten 20 €", "8 Karten kosten 40 €"], [("3 Kisten enthalten 18 Flaschen. 6 Kisten?", "36 Flaschen"), ("5 m kosten 25 €. 10 m?", "50 €")]),
            st("Halbieren", "Ist die gesuchte Menge halb so groß, halbiere auch den Wert.",
               ["Prüfe, ob genau halbiert wird.", "Halbiere auf beiden Seiten."],
               ["8 Pakete wiegen 32 kg", "4 Pakete wiegen 16 kg"], [("10 Hefte kosten 30 €. 5 Hefte?", "15 €"), ("12 Brötchen kosten 24 €. 6 Brötchen?", "12 €")]),
            st("Einheit und Sinn prüfen", "Schreibe die richtige Einheit dazu und prüfe, ob die Richtung stimmt.",
               ["Mehr Stück müssen bei gleichem Preis pro Stück mehr kosten.", "Mache einen groben Überschlag."],
               ["2 Pakete wiegen 10 kg", "6 Pakete: mehr als 10 kg", "Ergebnis 30 kg passt."], [("3 km dauern 12 min. 6 km?", "24 min"), ("4 Tage: 20 Seiten. 8 Tage?", "40 Seiten")]),
        ],
        "practice": [("3 Brezeln kosten 6 €. Wie viel kosten 7?", "14 €"),
                     ("4 Hefte kosten 12 €. Wie viel kosten 9?", "27 €"),
                     ("2 Pakete wiegen 10 kg. Wie viel wiegen 7?", "35 kg"),
                     ("5 Kisten enthalten 40 Flaschen. Wie viele enthalten 8?", "64 Flaschen"),
                     ("3 km dauern 15 min. Wie lange dauern 7 km?", "35 min"),
                     ("4 Äpfel kosten 8 €. Wie viel kosten 6?", "12 €"),
                     ("6 Bücher kosten 24 €. Wie viel kosten 5?", "20 €"),
                     ("3 Portionen brauchen 18 Kartoffeln. 7 Portionen?", "42 Kartoffeln"),
                     ("5 Runden bringen 30 Punkte. 9 Runden?", "54 Punkte"),
                     ("4 Minuten: 20 Seiten. Wie viele Seiten in 9 Minuten?", "45 Seiten")],
    },
    {
        "title": "Ebene Figuren", "slug": "09-ebene-figuren",
        "subtitle": "Eigenschaften nutzen statt nur abzählen",
        "strategies": [
            st("Seiten und Ecken", "Bei einem Vieleck ist die Zahl der Seiten genauso groß wie die Zahl der Ecken.",
               ["Der Name verrät oft die Zahl.", "Sechseck: 6 Seiten und 6 Ecken."],
               ["Achteck", "8 Seiten", "8 Ecken"], [("Zehneck: Seiten", "10"), ("Fünfeck: Ecken", "5")]),
            st("Vierecke an Eigenschaften erkennen", "Frage nach rechten Winkeln, gleich langen und parallelen Seiten.",
               ["Quadrat: 4 gleiche Seiten, 4 rechte Winkel.", "Rechteck: 4 rechte Winkel.", "Raute: 4 gleiche Seiten."],
               ["Vier gleiche Seiten", "und vier rechte Winkel", "= Quadrat"], [("Vier rechte Winkel", "Rechteck"), ("Genau ein Paar paralleler Seiten", "Trapez")]),
            st("Spiegelachsen denken", "Stelle dir vor, du faltest die Figur. Beide Hälften müssen genau aufeinanderliegen.",
               ["Quadrat: 4 Spiegelachsen.", "Rechteck ohne Quadrat: 2.", "Gleichseitiges Dreieck: 3."],
               ["Ungleichseitiges Dreieck", "keine passende Faltung", "0 Spiegelachsen"], [("Raute ohne Quadrat", "2"), ("gleichschenkliges Dreieck", "1")]),
            st("Dreiecke sortieren", "Achte auf gleiche Seiten und auf rechte Winkel.",
               ["3 gleiche Seiten: gleichseitig.", "2 gleiche Seiten: gleichschenklig.", "1 rechter Winkel: rechtwinklig."],
               ["Rechtwinkliges Dreieck", "längste Seite: Hypotenuse"], [("Drei gleich lange Seiten", "gleichseitiges Dreieck"), ("Zwei gleich lange Seiten", "gleichschenkliges Dreieck")]),
            st("Kreis: Radius und Durchmesser", "Der Radius geht vom Mittelpunkt zum Rand. Der Durchmesser geht durch den Mittelpunkt von Rand zu Rand.",
               ["Der Durchmesser besteht aus zwei Radien.", "Durchmesser = 2 · Radius."],
               ["Radius 4 cm", "Durchmesser 8 cm"], [("Radius 6 cm: Durchmesser", "12 cm"), ("Durchmesser 10 cm: Radius", "5 cm")]),
        ],
        "practice": [("Wie viele Seiten hat ein Achteck?", "8"), ("Wie heißt ein Vieleck mit 6 Seiten?", "Sechseck"),
                     ("Wie viele Spiegelachsen hat ein Quadrat?", "4"),
                     ("Wie heißt ein Viereck mit vier rechten Winkeln?", "Rechteck"),
                     ("Wie heißt ein Dreieck mit drei gleich langen Seiten?", "gleichseitiges Dreieck"),
                     ("Wie viele Spiegelachsen hat ein gleichschenkliges Dreieck?", "1"),
                     ("Wie heißt die Strecke vom Kreismittelpunkt zum Rand?", "Radius"),
                     ("Wie viele Ecken hat ein Zehneck?", "10"),
                     ("Radius 7 cm: Wie groß ist der Durchmesser?", "14 cm"),
                     ("Wie heißt die längste Seite im rechtwinkligen Dreieck?", "Hypotenuse")],
    },
    {
        "title": "Körper und Raum", "slug": "10-koerper-raum",
        "subtitle": "Flächen, Kanten und Ecken systematisch bestimmen",
        "strategies": [
            st("Systematisch zählen", "Zähle immer in derselben Reihenfolge: zuerst Flächen, dann Kanten, dann Ecken.",
               ["Markiere gedanklich, wo du begonnen hast.", "Zähle verdeckte Teile mit."],
               ["Würfel", "6 Flächen - 12 Kanten - 8 Ecken"], [("Quader: Flächen", "6"), ("Quader: Ecken", "8")]),
            st("Würfel und Quader", "Beide haben 6 Flächen, 12 Kanten und 8 Ecken. Beim Würfel sind alle Flächen Quadrate.",
               ["Würfel: 6 Quadrate.", "Quader: 6 Rechtecke."],
               ["Die Anzahlen sind gleich.", "Die Form der Flächen ist verschieden."], [("Würfel: Kanten", "12"), ("Quader: Flächenform", "Rechtecke")]),
            st("Runde Körper", "Kugel, Zylinder und Kegel haben gekrümmte Flächen. Nutze ihre besonderen Merkmale.",
               ["Kugel: keine Ecken, keine Kanten.", "Zylinder: zwei Kreisflächen.", "Kegel: eine Kreisfläche und eine Spitze."],
               ["Zwei Kreisflächen", "und eine gekrümmte Fläche", "= Zylinder"], [("Körper ohne Ecken und Kanten", "Kugel"), ("Körper mit einer Spitze und Kreisfläche", "Kegel")]),
            st("Pyramiden", "Eine Pyramide hat eine Grundfläche. Von deren Ecken führen Kanten zur Spitze.",
               ["Quadratische Grundfläche: 4 Ecken plus Spitze.", "Dreieckige Grundfläche: 3 Ecken plus Spitze."],
               ["Quadratische Pyramide", "5 Ecken - 8 Kanten - 5 Flächen"], [("Dreieckige Pyramide: Ecken", "4"), ("Quadratische Pyramide: Kanten", "8")]),
            st("Zusammengeklebte Würfel", "Bei jeder Klebestelle verschwinden zwei Flächen außen: eine von jedem Würfel.",
               ["Zähle zuerst 6 Flächen je Würfel.", "Ziehe für jede Klebestelle 2 ab."],
               ["3 Würfel in einer Reihe", "3 · 6 - 2 · 2", "= 14 Außenflächen"], [("2 Würfel in einer Reihe", "10 Außenflächen"), ("4 Würfel in einer Reihe", "18 Außenflächen")]),
        ],
        "practice": [("Wie viele Ecken hat ein Würfel?", "8"), ("Wie viele Kanten hat ein Quader?", "12"),
                     ("Wie viele Flächen hat ein Würfel?", "6"),
                     ("Welcher Körper hat keine Ecken und Kanten?", "Kugel"),
                     ("Welcher Körper hat zwei Kreisflächen?", "Zylinder"),
                     ("Wie viele Ecken hat eine quadratische Pyramide?", "5"),
                     ("Wie viele Kanten hat eine dreieckige Pyramide?", "6"),
                     ("Zwei Würfel in einer Reihe: sichtbare Außenflächen?", "10"),
                     ("Vier Würfel in einer Reihe: sichtbare Außenflächen?", "18"),
                     ("Aus welchen Flächen besteht ein Würfel?", "6 Quadrate")],
    },
]


def register_fonts():
    pdfmetrics.registerFont(TTFont("DV", FONT))
    pdfmetrics.registerFont(TTFont("DV-Bold", BOLD))


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


def text_block(c, text, x, y, width, size=10, leading=13, font="DV", color=INK, max_lines=20):
    c.setFont(font, size)
    c.setFillColor(color)
    lines = wrap(text, font, size, width)[:max_lines]
    for i, line in enumerate(lines):
        c.drawString(x, y - i * leading, line)
    return y - len(lines) * leading


def number_circle(c, x, y, radius, label, font_size):
    """Zeichnet eine Ziffer optisch exakt mittig in einen Kreis."""
    c.setFillColor(BLUE)
    c.circle(x, y, radius, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DV-Bold", font_size)
    ascent = pdfmetrics.getAscent("DV-Bold", font_size)
    descent = pdfmetrics.getDescent("DV-Bold", font_size)
    baseline = y - (ascent + descent) / 2
    c.drawCentredString(x, baseline, str(label))


def page_footer(c, page, total=8):
    w, _ = A5
    c.setStrokeColor(GRID)
    c.line(12 * mm, 12 * mm, w - 12 * mm, 12 * mm)
    c.setFont("DV", 7)
    c.setFillColor(MUTED)
    c.drawString(12 * mm, 7.5 * mm, "1 bis 10 · Rechentricks · Klasse 5")
    c.drawRightString(w - 12 * mm, 7.5 * mm, f"Seite {page} von {total}")


def cover(c, number, book):
    w, h = A5
    c.setFillColor(NAVY)
    c.rect(0, h * .46, w, h * .54, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DV-Bold", 9)
    c.drawString(14 * mm, h - 17 * mm, "1 BIS 10 · RECHENTRICKS")
    number_circle(c, w - 25 * mm, h - 28 * mm, 12 * mm, number, 24)
    y = h - 54 * mm
    for line in wrap(book["title"], "DV-Bold", 23, w - 28 * mm):
        c.setFont("DV-Bold", 23)
        c.drawString(14 * mm, y, line)
        y -= 9 * mm
    text_block(c, book["subtitle"], 14 * mm, y - 2 * mm, w - 28 * mm, 10.5, 14, color=white)

    c.setFillColor(INK)
    c.setFont("DV-Bold", 11)
    c.drawString(14 * mm, h * .40, "In diesem Heft")
    y = h * .35
    for i, strategy in enumerate(book["strategies"], 1):
        number_circle(c, 18 * mm, y + 0.9 * mm, 3.2 * mm, i, 7)
        c.setFillColor(INK)
        c.setFont("DV-Bold", 9.3)
        c.drawString(25 * mm, y, strategy["title"])
        y -= 8.5 * mm
    c.setFillColor(SKY)
    c.roundRect(14 * mm, 18 * mm, w - 28 * mm, 18 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("DV-Bold", 9)
    c.drawString(20 * mm, 29 * mm, "Lesen · Nachmachen · Selbst probieren")
    c.setFont("DV", 8)
    c.drawString(20 * mm, 23 * mm, "Danach warten zehn Aufgaben und alle Lösungen.")


def strategy_page(c, number, book, index, strategy):
    w, h = A5
    c.setFillColor(NAVY)
    c.rect(0, h - 23 * mm, w, 23 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DV-Bold", 8)
    c.drawString(12 * mm, h - 9 * mm, f"RECHENTRICK {index} VON 5")
    c.setFont("DV-Bold", 15)
    c.drawString(12 * mm, h - 17 * mm, strategy["title"])
    number_circle(c, w - 18 * mm, h - 11.5 * mm, 7 * mm, number, 14)

    y = h - 34 * mm
    c.setFillColor(SKY)
    c.roundRect(12 * mm, y - 26 * mm, w - 24 * mm, 28 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("DV-Bold", 9)
    c.drawString(17 * mm, y - 5 * mm, "Der Trick")
    text_block(c, strategy["explain"], 17 * mm, y - 11 * mm, w - 34 * mm, 9.2, 12, max_lines=3)

    y -= 35 * mm
    c.setFillColor(NAVY)
    c.setFont("DV-Bold", 10)
    c.drawString(12 * mm, y, "So geht's")
    y -= 8 * mm
    for step_no, step in enumerate(strategy["steps"], 1):
        step_lines = wrap(step, "DV", 8.8, w - 35 * mm)[:2]
        number_circle(c, 16 * mm, y + 0.9 * mm, 2.5 * mm, step_no, 6.2)
        text_block(c, step, 22 * mm, y, w - 35 * mm, 8.8, 11, max_lines=2)
        row_height = max(8 * mm, len(step_lines) * 11 + 3 * mm)
        y -= row_height

    example_h = 35 * mm
    # Der Beispielkasten beginnt mit festem Abstand unter der letzten
    # nummerierten Zeile. So kann er keinen Nummerierungskreis überdecken.
    example_y = max(64 * mm, y - example_h - 3 * mm)
    c.setFillColor(PALE)
    c.setStrokeColor(GRID)
    c.roundRect(12 * mm, example_y, w - 24 * mm, example_h, 3 * mm, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("DV-Bold", 9)
    c.drawString(17 * mm, example_y + example_h - 7 * mm, "Beispiel")
    line_y = example_y + example_h - 15 * mm
    for line in strategy["example"]:
        c.setFillColor(INK)
        c.setFont("DV-Bold" if line == strategy["example"][-1] else "DV", 10)
        c.drawString(19 * mm, line_y, line)
        line_y -= 6.5 * mm

    mini_y = 48 * mm
    c.setFillColor(NAVY)
    c.setFont("DV-Bold", 9.5)
    c.drawString(12 * mm, mini_y + 7 * mm, "Jetzt du")
    for i, (question, _) in enumerate(strategy["mini"], 1):
        yy = mini_y - (i - 1) * 13 * mm
        text_block(c, f"{i}. {question}", 15 * mm, yy, w - 45 * mm, 8.6, 10, max_lines=2)
        c.setStrokeColor(GRID)
        c.setDash(1.5, 2)
        c.line(w - 42 * mm, yy - 1 * mm, w - 13 * mm, yy - 1 * mm)
        c.setDash()
    page_footer(c, index + 1)


def practice_page(c, number, book):
    w, h = A5
    c.setFillColor(NAVY)
    c.rect(0, h - 25 * mm, w, 25 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DV-Bold", 8)
    c.drawString(12 * mm, h - 9 * mm, f"HEFT {number} · ÜBEN")
    c.setFont("DV-Bold", 17)
    c.drawString(12 * mm, h - 18 * mm, "Zehn Aufgaben")
    c.setFillColor(MUTED)
    c.setFont("DV", 8)
    c.drawString(12 * mm, h - 31 * mm, "Nutze den Trick, der am besten zur Aufgabe passt.")
    top = h - 42 * mm
    row_h = 14.7 * mm
    for i, (question, _) in enumerate(book["practice"], 1):
        y = top - (i - 1) * row_h
        number_circle(c, 16 * mm, y + 0.9 * mm, 3.2 * mm, i, 7)
        text_block(c, question, 23 * mm, y, w - 36 * mm, 8.3, 9.5, max_lines=2)
        c.setStrokeColor(GRID)
        c.setDash(1.5, 2)
        c.line(23 * mm, y - 7 * mm, w - 13 * mm, y - 7 * mm)
        c.setDash()
    page_footer(c, 7)


def solutions_page(c, number, book):
    w, h = A5
    c.setFillColor(NAVY)
    c.rect(0, h - 25 * mm, w, 25 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DV-Bold", 8)
    c.drawString(12 * mm, h - 9 * mm, f"HEFT {number} · KONTROLLIEREN")
    c.setFont("DV-Bold", 17)
    c.drawString(12 * mm, h - 18 * mm, "Lösungen")

    c.setFillColor(NAVY)
    c.setFont("DV-Bold", 9.5)
    c.drawString(12 * mm, h - 35 * mm, "Die kleinen Aufgaben")
    y = h - 43 * mm
    for i, strategy in enumerate(book["strategies"], 1):
        answers = " · ".join(f"{j}: {answer}" for j, (_, answer) in enumerate(strategy["mini"], 1))
        text_block(c, f"Trick {i}: {answers}", 14 * mm, y, w - 28 * mm, 7.8, 9.5, max_lines=2)
        y -= 12 * mm

    c.setFillColor(SKY)
    c.roundRect(12 * mm, 20 * mm, w - 24 * mm, 79 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("DV-Bold", 9.5)
    c.drawString(17 * mm, 91 * mm, "Die zehn Übungsaufgaben")
    for i, (_, answer) in enumerate(book["practice"], 1):
        col = 0 if i <= 5 else 1
        row = (i - 1) % 5
        x = 18 * mm + col * 59 * mm
        yy = 81 * mm - row * 12 * mm
        text_block(c, f"{i}. {answer}", x, yy, 52 * mm, 8.2, 9.5, font="DV-Bold", max_lines=2)
    page_footer(c, 8)


def build_booklet(number, book):
    path = OUT / f"{book['slug']}.pdf"
    c = canvas.Canvas(str(path), pagesize=A5, pageCompression=1)
    c.setTitle(f"Rechentricks {number}: {book['title']}")
    c.setAuthor("1 bis 10")
    c.setSubject(f"Rechentricks für Klasse 5: {book['title']}")
    cover(c, number, book)
    c.showPage()
    for index, strategy in enumerate(book["strategies"], 1):
        strategy_page(c, number, book, index, strategy)
        c.showPage()
    practice_page(c, number, book)
    c.showPage()
    solutions_page(c, number, book)
    c.showPage()
    c.save()
    reader = PdfReader(path)
    if len(reader.pages) != 8:
        raise RuntimeError(f"{path.name}: {len(reader.pages)} statt 8 Seiten")
    return path


def main():
    register_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [build_booklet(i, book) for i, book in enumerate(BOOKLETS, 1)]
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
