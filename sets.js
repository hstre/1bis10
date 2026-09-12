/*
 * Die 40 Sets werden ausschließlich aus diesen fest eingetragenen Reihen erzeugt.
 * Es gibt keine Zufallszahlen zur Laufzeit. Setnummer und Aufgabe ergeben daher
 * bei jedem Aufruf exakt dieselbe Aufgabe und Lösung.
 */

const CATEGORIES = [
  "Addition und Subtraktion",
  "Multiplikation",
  "Division",
  "Einheiten",
  "Schätzen",
  "Verhältnisse",
  "Diagramme",
  "Zwei- und Dreisatz",
  "Ebene Figuren",
  "Körper und Raum"
];

const addData = [
  [45, 18, -9, 26, -20], [72, -18, 35, -9], [120, 35, -48, 13], [64, 29, -17, -26],
  [250, -80, 45, -65], [38, 27, -19, 44], [500, -125, 75, -90], [96, -38, 17, 25],
  [180, 45, -70, 25], [350, -90, -60, 125], [84, 36, -27, 18], [620, -180, 75, -115],
  [205, 95, -140, 60], [76, -29, 54, -21], [440, 85, -125, -100], [128, 72, -45, 35],
  [900, -250, 175, -125], [57, 68, -39, 14], [315, -95, 48, -68], [700, -240, -160, 90],
  [146, 54, -75, 29], [82, -37, 65, -20], [525, -175, 90, -140], [260, 85, -105, -40],
  [99, 46, -28, 33], [480, -135, 65, -110], [175, 125, -80, 45], [63, 49, -32, 20],
  [840, -290, 150, -200], [230, -75, 95, -50], [118, 82, -67, 24], [390, 110, -175, -85],
  [74, 58, -39, -17], [650, -225, 85, -110], [285, 65, -120, 40], [92, -44, 73, -21],
  [760, -180, -230, 95], [135, 65, -48, 22], [420, -95, 130, -155], [1000, -275, -125, 85]
];

const multiplication = [
  [6,8,"direct"],[7,9,"direct"],[4,16,"missing"],[8,12,"direct"],[5,18,"missing"],
  [9,7,"missing"],[6,14,"direct"],[4,25,"direct"],[8,15,"missing"],[12,7,"direct"],
  [9,13,"direct"],[6,18,"missing"],[14,5,"direct"],[8,16,"direct"],[7,15,"missing"],
  [12,9,"missing"],[4,32,"direct"],[11,8,"direct"],[6,25,"missing"],[15,7,"direct"],
  [9,18,"direct"],[12,12,"missing"],[16,6,"direct"],[14,8,"direct"],[7,24,"missing"],
  [18,5,"direct"],[9,16,"missing"],[13,7,"direct"],[12,15,"direct"],[8,24,"missing"],
  [17,6,"direct"],[14,9,"missing"],[11,14,"direct"],[16,8,"direct"],[12,18,"missing"],
  [15,9,"direct"],[13,12,"direct"],[8,35,"missing"],[19,7,"direct"],[16,15,"direct"]
];

const divisions = [
  [48,6],[63,7],[96,8],[84,7],[90,5],[126,9],[144,12],[100,4],[120,8],[132,11],
  [156,12],[108,6],[175,7],[160,8],[135,9],[216,12],[128,4],[200,5],[225,9],[168,8],
  [198,11],[240,12],[182,7],[256,8],[270,9],[300,6],[288,12],[224,7],[320,8],[330,11],
  [360,9],[350,7],[384,12],[400,8],[450,9],[420,12],[396,11],[480,12],[432,8],[525,7]
];

const units = [
  ["2 m", "cm", "200 cm"], ["3 km", "m", "3000 m"], ["4 kg", "g", "4000 g"], ["2 h", "min", "120 min"],
  ["5 min", "s", "300 s"], ["3 Zentner", "kg", "150 kg"], ["7 l", "ml", "7000 ml"], ["450 cm", "m", "4,5 m"],
  ["180 min", "h", "3 h"], ["6000 g", "kg", "6 kg"], ["8 dm", "cm", "80 cm"], ["240 s", "min", "4 min"],
  ["4 Zentner", "kg", "200 kg"], ["2,5 l", "ml", "2500 ml"], ["3500 m", "km", "3,5 km"], ["2 min 30 s", "s", "150 s"],
  ["7500 g", "kg", "7,5 kg"], ["6 h", "min", "360 min"], ["1250 ml", "l", "1,25 l"], ["5 Zentner", "kg", "250 kg"],
  ["90 min", "h", "1,5 h"], ["1,8 m", "dm", "18 dm"], ["540 s", "min", "9 min"], ["2 t", "Zentner", "40 Zentner"],
  ["3200 mm", "m", "3,2 m"], ["3 min 20 s", "s", "200 s"], ["1,5 kg", "g", "1500 g"], ["750 cl", "l", "7,5 l"],
  ["8 Zentner", "kg", "400 kg"], ["2 h 15 min", "min", "135 min"], ["0,75 km", "m", "750 m"], ["480 min", "h", "8 h"],
  ["2750 g", "kg", "2,75 kg"], ["12 min", "s", "720 s"], ["6,5 m", "cm", "650 cm"], ["500 kg", "Zentner", "10 Zentner"],
  ["1 h 40 min", "min", "100 min"], ["4500 ml", "l", "4,5 l"], ["9 km", "m", "9000 m"], ["900 s", "min", "15 min"]
];

const estimates = [
  ["Wie hoch ist ungefähr eine Zimmertür?", ["20 cm","2 m","20 m"], "2 m"],
  ["Wie schwer ist ungefähr ein Schulranzen?", ["400 g","4 kg","40 kg"], "4 kg"],
  ["Wie lang dauert ungefähr eine Unterrichtsstunde?", ["5 min","45 min","4 h"], "45 min"],
  ["Welches Ergebnis liegt 49 · 21 am nächsten?", ["100","1000","10 000"], "1000"],
  ["Wie viel Wasser passt ungefähr in eine Badewanne?", ["2 l","20 l","200 l"], "200 l"],
  ["Wie groß ist ungefähr ein rechter Winkel?", ["45°","90°","180°"], "90°"],
  ["Wie lang ist ungefähr ein Linienbus?", ["1 m","12 m","120 m"], "12 m"],
  ["Welches Ergebnis liegt 198 + 305 am nächsten?", ["50","500","5000"], "500"],
  ["Wie schwer ist ungefähr eine Büroklammer?", ["1 g","100 g","1 kg"], "1 g"],
  ["Wie hoch ist ungefähr ein fünfstöckiges Haus?", ["2 m","15 m","150 m"], "15 m"],
  ["Welches Ergebnis liegt 79 · 11 am nächsten?", ["90","900","9000"], "900"],
  ["Wie viel fasst ungefähr ein Trinkglas?", ["20 ml","200 ml","2 l"], "200 ml"],
  ["Wie lang ist ungefähr ein Fußballfeld?", ["10 m","100 m","1000 m"], "100 m"],
  ["Wie schwer ist ungefähr ein Fahrrad?", ["1,5 kg","15 kg","150 kg"], "15 kg"],
  ["Welches Ergebnis liegt 603 − 298 am nächsten?", ["30","300","3000"], "300"],
  ["Wie breit ist ungefähr eine Hand?", ["1 cm","10 cm","1 m"], "10 cm"],
  ["Wie lange dauert ungefähr ein Kinofilm?", ["10 min","100 min","1000 min"], "100 min"],
  ["Wie viel wiegt ungefähr ein Apfel?", ["20 g","200 g","2 kg"], "200 g"],
  ["Welches Ergebnis liegt 39 · 51 am nächsten?", ["200","2000","20 000"], "2000"],
  ["Wie hoch ist ungefähr ein Esstisch?", ["7 cm","75 cm","7 m"], "75 cm"],
  ["Wie viel Wasser passt ungefähr in einen Putzeimer?", ["1 l","10 l","100 l"], "10 l"],
  ["Wie schnell geht ein Mensch ungefähr?", ["5 km/h","50 km/h","500 km/h"], "5 km/h"],
  ["Welches Ergebnis liegt 1002 − 497 am nächsten?", ["50","500","5000"], "500"],
  ["Wie schwer ist ungefähr ein erwachsener Mensch?", ["7 kg","70 kg","700 kg"], "70 kg"],
  ["Wie lang ist ungefähr ein Bleistift?", ["2 cm","20 cm","2 m"], "20 cm"],
  ["Wie viel fasst ungefähr eine Getränkedose?", ["33 ml","330 ml","3,3 l"], "330 ml"],
  ["Welches Ergebnis liegt 24 · 39 am nächsten?", ["100","1000","10 000"], "1000"],
  ["Wie hoch ist ungefähr eine Treppenstufe?", ["2 cm","20 cm","2 m"], "20 cm"],
  ["Wie lang dauert ungefähr ein Schultag?", ["6 min","6 h","60 h"], "6 h"],
  ["Wie schwer ist ungefähr ein Kleinwagen?", ["100 kg","1000 kg","10 000 kg"], "1000 kg"],
  ["Welches Ergebnis liegt 151 · 6 am nächsten?", ["90","900","9000"], "900"],
  ["Wie weit ist ein großer Schritt ungefähr?", ["8 cm","80 cm","8 m"], "80 cm"],
  ["Wie viel fasst ein Milchkarton ungefähr?", ["10 ml","1 l","100 l"], "1 l"],
  ["Wie warm ist ein beheiztes Klassenzimmer ungefähr?", ["2 °C","20 °C","200 °C"], "20 °C"],
  ["Welches Ergebnis liegt 197 · 5 am nächsten?", ["100","1000","10 000"], "1000"],
  ["Wie lang ist ungefähr ein Pkw?", ["40 cm","4 m","40 m"], "4 m"],
  ["Wie schwer ist ungefähr ein Laib Brot?", ["10 g","1 kg","100 kg"], "1 kg"],
  ["Wie viel Wasser verbraucht eine Dusche ungefähr?", ["1 l","50 l","5000 l"], "50 l"],
  ["Welches Ergebnis liegt 498 + 503 am nächsten?", ["100","1000","10 000"], "1000"],
  ["Wie hoch ist ungefähr ein Basketballkorb?", ["30 cm","3 m","30 m"], "3 m"]
];

const ratios = [
  [2,5,"Welcher Anteil der 5 Felder ist blau?","2/5"], [3,4,"Welcher Anteil der 4 Felder ist blau?","3/4"],
  [4,10,"Welcher Anteil der 10 Felder ist blau?","4/10 = 2/5"], [1,3,"Welcher Anteil der 3 Felder ist blau?","1/3"],
  [3,5,"Welcher Anteil der 5 Felder ist blau?","3/5"], [6,8,"Welcher Anteil der 8 Felder ist blau?","6/8 = 3/4"],
  [2,6,"Kürze das Verhältnis 2 : 6.","1 : 3"], [4,6,"Kürze das Verhältnis 4 : 6.","2 : 3"],
  [5,10,"Welcher Anteil der 10 Felder ist blau?","5/10 = 1/2"], [3,9,"Kürze das Verhältnis 3 : 9.","1 : 3"],
  [7,10,"Welcher Anteil der 10 Felder ist blau?","7/10"], [2,8,"Kürze das Verhältnis 2 : 8.","1 : 4"],
  [5,8,"Welcher Anteil der 8 Felder ist blau?","5/8"], [6,9,"Kürze das Verhältnis 6 : 9.","2 : 3"],
  [4,5,"Welcher Anteil der 5 Felder ist blau?","4/5"], [3,12,"Kürze das Verhältnis 3 : 12.","1 : 4"],
  [8,10,"Kürze das Verhältnis 8 : 10.","4 : 5"], [2,3,"Welcher Anteil der 3 Felder ist blau?","2/3"],
  [6,10,"Kürze das Verhältnis 6 : 10.","3 : 5"], [1,4,"Welcher Anteil der 4 Felder ist blau?","1/4"],
  [9,12,"Kürze das Verhältnis 9 : 12.","3 : 4"], [3,8,"Welcher Anteil der 8 Felder ist blau?","3/8"],
  [4,12,"Kürze das Verhältnis 4 : 12.","1 : 3"], [7,8,"Welcher Anteil der 8 Felder ist blau?","7/8"],
  [10,15,"Kürze das Verhältnis 10 : 15.","2 : 3"], [5,6,"Welcher Anteil der 6 Felder ist blau?","5/6"],
  [8,12,"Kürze das Verhältnis 8 : 12.","2 : 3"], [3,10,"Welcher Anteil der 10 Felder ist blau?","3/10"],
  [12,16,"Kürze das Verhältnis 12 : 16.","3 : 4"], [4,8,"Welcher Anteil der 8 Felder ist blau?","4/8 = 1/2"],
  [6,15,"Kürze das Verhältnis 6 : 15.","2 : 5"], [9,10,"Welcher Anteil der 10 Felder ist blau?","9/10"],
  [14,21,"Kürze das Verhältnis 14 : 21.","2 : 3"], [2,10,"Welcher Anteil der 10 Felder ist blau?","2/10 = 1/5"],
  [15,20,"Kürze das Verhältnis 15 : 20.","3 : 4"], [5,12,"Welcher Anteil der 12 Felder ist blau?","5/12"],
  [12,18,"Kürze das Verhältnis 12 : 18.","2 : 3"], [7,12,"Welcher Anteil der 12 Felder ist blau?","7/12"],
  [18,24,"Kürze das Verhältnis 18 : 24.","3 : 4"], [8,20,"Kürze das Verhältnis 8 : 20.","2 : 5"]
];

const proportionals = [
  [3,6,5,"Brezeln","€"],[4,8,7,"Hefte","€"],[2,6,5,"Personen","Eier"],[5,10,8,"Flaschen","€"],
  [3,12,7,"Kilometer","min"],[4,12,6,"Äpfel","€"],[2,8,5,"Kinokarten","€"],[6,18,4,"Brötchen","€"],
  [5,15,8,"Stifte","€"],[3,9,10,"Liter Saft","€"],[4,20,7,"Tage","Seiten"],[2,10,6,"Pakete","kg"],
  [5,20,9,"Muffins","€"],[3,15,8,"Meter Stoff","€"],[4,16,9,"Fahrten","km"],[2,12,7,"Kisten","Flaschen"],
  [6,24,5,"Bücher","€"],[4,28,9,"Stunden","€"],[3,18,7,"Portionen","Kartoffeln"],[5,25,12,"Tickets","€"],
  [2,14,9,"Bro­te","€"],[4,24,7,"Becher","€"],[3,21,8,"Kilogramm Äpfel","€"],[5,30,9,"Runden","Punkte"],
  [6,30,11,"Bananen","€"],[4,32,7,"Kartons","Flaschen"],[3,24,10,"Meter Band","€"],[2,18,5,"Hefte","€"],
  [5,35,8,"Stunden","km"],[4,36,7,"Portionen","€"],[3,27,11,"Pakete","kg"],[6,42,5,"Flaschen","€"],
  [4,40,9,"Minuten","Seiten"],[5,45,8,"Karten","€"],[3,30,7,"Kilogramm","€"],[2,22,6,"Fahrten","km"],
  [5,50,7,"Tage","Seiten"],[4,44,9,"Tüten","Bonbons"],[3,33,8,"Stifte","€"],[6,60,7,"Kisten","Flaschen"]
];

const planeTasks = [
  ["Wie heißt ein Viereck mit vier gleich langen Seiten und vier rechten Winkeln?","Quadrat"],
  ["Wie viele Spiegelachsen hat ein Rechteck, das kein Quadrat ist?","2"],
  ["Wie heißt ein Dreieck mit drei gleich langen Seiten?","gleichseitiges Dreieck"],
  ["Wie viele Seiten hat ein Sechseck?","6"],
  ["Wie heißt ein Viereck mit genau einem Paar paralleler Seiten?","Trapez"],
  ["Wie viele Spiegelachsen hat ein Quadrat?","4"],
  ["Wie heißt eine ebene Figur ohne Ecken?","Kreis"],
  ["Wie viele Ecken hat ein Achteck?","8"],
  ["Wie heißt ein Viereck mit gegenüberliegenden parallelen Seiten?","Parallelogramm"],
  ["Wie viele Spiegelachsen hat ein gleichseitiges Dreieck?","3"],
  ["Wie heißt ein Viereck mit vier gleich langen Seiten?","Raute"],
  ["Wie viele Seiten hat ein Fünfeck?","5"],
  ["Wie viele Spiegelachsen hat ein gleichschenkliges Dreieck?","1"],
  ["Wie heißt ein Viereck mit vier rechten Winkeln?","Rechteck"],
  ["Wie viele Diagonalen hat ein Viereck?","2"],
  ["Welche Figur hat mehr Ecken: Sechseck oder Achteck?","Achteck"],
  ["Wie viele Spiegelachsen hat ein Kreis?","unendlich viele"],
  ["Wie heißt ein Dreieck mit einem rechten Winkel?","rechtwinkliges Dreieck"],
  ["Wie viele Seiten haben zwei Dreiecke zusammen?","6"],
  ["Wie heißt ein Vieleck mit acht Seiten?","Achteck"],
  ["Wie viele rechte Winkel hat ein Quadrat?","4"],
  ["Wie viele Spiegelachsen hat eine Raute, die kein Quadrat ist?","2"],
  ["Wie heißt die längste Seite im rechtwinkligen Dreieck?","Hypotenuse"],
  ["Wie viele Ecken haben drei Vierecke zusammen?","12"],
  ["Wie heißt ein Dreieck mit zwei gleich langen Seiten?","gleichschenkliges Dreieck"],
  ["Hat jedes Quadrat auch die Eigenschaften eines Rechtecks?","ja"],
  ["Wie viele Seiten hat ein Zehneck?","10"],
  ["Wie viele Spiegelachsen hat ein regelmäßiges Sechseck?","6"],
  ["Wie heißt die Strecke vom Kreismittelpunkt zum Rand?","Radius"],
  ["Wie viele Endpunkte hat eine Strecke?","2"],
  ["Wie heißt eine Gerade, die eine andere im rechten Winkel schneidet?","senkrecht"],
  ["Wie viele Paare paralleler Seiten hat ein Rechteck?","2 Paare"],
  ["Wie heißt die Strecke durch den Mittelpunkt von Kreisrand zu Kreisrand?","Durchmesser"],
  ["Wie viele Spiegelachsen hat ein regelmäßiges Fünfeck?","5"],
  ["Ein Rechteck wird entlang einer Diagonalen geteilt. Welche Figuren entstehen?","zwei rechtwinklige Dreiecke"],
  ["Wie viele Ecken hat ein regelmäßiges Zwölfeck?","12"],
  ["Wie heißt ein Dreieck ohne gleich lange Seiten?","ungleichseitiges Dreieck"],
  ["Wie viele rechte Winkel hat ein Rechteck?","4"],
  ["Wie viele Spiegelachsen hat ein ungleichseitiges Dreieck?","0"],
  ["Wie heißt ein halber Kreis?","Halbkreis"]
];

const solidTasks = [
  ["Wie viele Ecken hat ein Würfel?","8"],["Wie viele Kanten hat ein Würfel?","12"],
  ["Wie viele Flächen hat ein Würfel?","6"],["Wie viele Ecken hat eine quadratische Pyramide?","5"],
  ["Wie viele Kanten hat eine quadratische Pyramide?","8"],["Wie viele Flächen hat eine quadratische Pyramide?","5"],
  ["Welcher Körper hat keine Ecken und keine Kanten?","Kugel"],["Wie viele Ecken hat ein Quader?","8"],
  ["Wie viele Kanten hat ein Quader?","12"],["Wie viele Flächen hat ein Quader?","6"],
  ["Wie heißt ein Körper mit zwei Kreisflächen und einer gekrümmten Fläche?","Zylinder"],
  ["Wie viele Ecken hat ein Zylinder?","0"],["Wie viele Kanten hat ein Zylinder?","2 Kreislinien"],
  ["Wie heißt ein Körper mit einer Kreisfläche und einer Spitze?","Kegel"],
  ["Wie viele Ecken hat ein Kegel?","1"],["Wie viele Kanten hat ein Kegel?","1 Kreislinie"],
  ["Wie viele Ecken hat eine dreieckige Pyramide?","4"],["Wie viele Kanten hat eine dreieckige Pyramide?","6"],
  ["Wie viele Flächen hat eine dreieckige Pyramide?","4"],["Aus welchen Flächen besteht ein Würfel?","6 Quadrate"],
  ["Aus welchen Flächen besteht ein Quader?","6 Rechtecke"],["Welcher Körper kann in alle Richtungen rollen?","Kugel"],
  ["Welcher Körper hat genau eine Spitze und eine Kreisfläche?","Kegel"],["Welcher Körper hat zwei gleich große Kreisflächen?","Zylinder"],
  ["Wie viele Würfel braucht man mindestens für einen Turm der Höhe 5?","5"],
  ["Wie viele sichtbare Flächen hat ein einzelner Würfel?","6"],
  ["Zwei Würfel werden an einer Fläche zusammengeklebt. Wie viele Flächen bleiben außen sichtbar?","10"],
  ["Drei Würfel stehen in einer geraden Reihe. Wie viele Flächen sind außen sichtbar?","14"],
  ["Wie heißt die Ansicht eines Körpers direkt von oben?","Draufsicht"],
  ["Wie heißt die Ansicht eines Körpers direkt von vorn?","Vorderansicht"],
  ["Kann ein Würfelnetz aus fünf Quadraten bestehen?","nein, es braucht sechs"],
  ["Wie viele Quadrate enthält jedes Würfelnetz?","6"],
  ["Wie viele Flächen treffen sich an einer Würfelecke?","3"],
  ["Wie viele Kanten treffen sich an einer Würfelecke?","3"],
  ["Welche Form hat die Grundfläche einer quadratischen Pyramide?","Quadrat"],
  ["Welche Form haben die Seitenflächen einer quadratischen Pyramide?","Dreiecke"],
  ["Wie viele Seitenflächen hat eine quadratische Pyramide?","4"],
  ["Wie viele Ecken haben zwei getrennte Würfel zusammen?","16"],
  ["Wie viele Kanten haben zwei getrennte Quader zusammen?","24"],
  ["Wie viele Flächen haben drei getrennte Würfel zusammen?","18"]
];

function sum(values) { return values.reduce((total, value) => total + value, 0); }
function signed(value) { return value >= 0 ? `+ ${value}` : `− ${Math.abs(value)}`; }

function additionTask(i) {
  const values = addData[i];
  const modes = ["sequence", "receipt", "score", "stock"];
  const mode = modes[i % modes.length];
  const total = sum(values);
  if (mode === "receipt") {
    const positives = values.filter(v => v > 0);
    const paid = Math.ceil(sum(positives) / 10) * 10 + 20;
    return {
      prompt: `Diese Rechnung wird mit ${paid} € bezahlt. Wie viel Rückgeld gibt es?`,
      answer: `${paid - sum(positives)} €`, seconds: 35, kind: "receipt",
      detail: positives.map((v,j) => [`Posten ${j+1}`, `${v} €`])
    };
  }
  if (mode === "score") return {
    prompt: `Ein Team startet mit ${values[0]} Punkten. Danach: ${values.slice(1).map(signed).join(", ")}. Wie ist der Endstand?`,
    answer: `${total} Punkte`, seconds: 30, kind: "score", values
  };
  if (mode === "stock") return {
    prompt: `Im Lager sind ${values[0]} Kisten. Danach werden ${values.slice(1).map(v => `${Math.abs(v)} ${v > 0 ? "geliefert" : "abgeholt"}`).join(", dann ")}. Wie viele sind es jetzt?`,
    answer: `${total} Kisten`, seconds: 35, kind: "story"
  };
  return {
    prompt: "Rechne die Zahlen der Reihe nach.", answer: String(total), seconds: 30,
    kind: "sequence", values
  };
}

function multiplicationTask(i) {
  const [a,b,mode] = multiplication[i];
  return mode === "missing"
    ? { prompt: `Welche Zahl fehlt?`, display: `${a} · □ = ${a*b}`, answer: String(b), seconds: 25, kind: "equation" }
    : { prompt: "Berechne im Kopf.", display: `${a} · ${b} =`, answer: String(a*b), seconds: 20, kind: "equation" };
}

function divisionTask(i) {
  const [a,b] = divisions[i];
  return { prompt: "Berechne im Kopf.", display: `${a} : ${b} =`, answer: String(a/b), seconds: 20, kind: "equation" };
}

function unitTask(i) {
  const [from,to,answer] = units[i];
  return { prompt: "Rechne in die angegebene Einheit um.", display: `${from} = ____ ${to}`, answer, seconds: i > 14 ? 30 : 25, kind: "equation" };
}

function estimateTask(i) {
  const [prompt, choices, answer] = estimates[i];
  return { prompt, choices, answer, seconds: 25, kind: "choices" };
}

function ratioTask(i) {
  const [filled,total,prompt,answer] = ratios[i];
  return { prompt, answer, seconds: 30, kind: "ratio", filled, total };
}

function chartTask(i) {
  const a = 2 + (i % 5), b = a + 2 + (i % 3), c = b + 1 + ((i * 2) % 4);
  const labels = ["Mo", "Di", "Mi"];
  const questions = [
    `An welchem Tag ist der Wert am größten?`,
    `Um wie viel ist der Wert von ${labels[0]} bis ${labels[2]} gestiegen?`,
    `Wie groß ist die Summe aller drei Werte?`
  ];
  const q = questions[i % 3];
  const answer = i % 3 === 0 ? labels[2] : i % 3 === 1 ? String(c-a) : String(a+b+c);
  return { prompt: q, answer, seconds: 35, kind: "chart", chartMode: ["bars", "line", "table"][i % 3], labels, values: [a,b,c] };
}

function proportionalTask(i) {
  const [from,amount,to,noun,unit] = proportionals[i];
  const one = amount / from;
  return {
    prompt: `${from} ${noun} entsprechen ${amount} ${unit}. Wie viel entsprechen ${to} ${noun}?`,
    answer: `${one * to} ${unit}`, detail: `${amount} : ${from} = ${one}; ${one} · ${to} = ${one*to}`,
    seconds: 40, kind: "story"
  };
}

function planeVisual(prompt, answer) {
  const text = `${prompt} ${answer}`.toLowerCase();
  if (text.includes("zwölfeck")) return "dodecagon";
  if (text.includes("zehneck")) return "decagon";
  if (text.includes("achteck")) return "octagon";
  if (text.includes("sechseck")) return "hexagon";
  if (text.includes("fünfeck")) return "pentagon";
  if (text.includes("quadrat")) return "square";
  if (text.includes("rechteck")) return "rectangle";
  if (text.includes("parallelogramm")) return "parallelogram";
  if (text.includes("trapez")) return "trapezoid";
  if (text.includes("raute")) return "rhombus";
  if (text.includes("kreis")) return "circle";
  if (text.includes("rechtwinklig") && text.includes("dreieck")) return "right-triangle";
  if (text.includes("gleichseitig") && text.includes("dreieck")) return "equilateral-triangle";
  if (text.includes("gleichschenklig") && text.includes("dreieck")) return "isosceles-triangle";
  if (text.includes("dreieck")) return "triangle";
  if (text.includes("viereck")) return "quadrilateral";
  if (text.includes("strecke") || text.includes("gerade")) return "line";
  return null;
}

function solidVisual(prompt, answer) {
  const text = `${prompt} ${answer}`.toLowerCase();
  if (text.includes("würfelnetz")) return "cube-net";
  if (text.includes("quadratisch") && text.includes("pyramide")) return "square-pyramid";
  if (text.includes("dreieckig") && text.includes("pyramide")) return "tetrahedron";
  if (text.includes("zylinder")) return "cylinder";
  if (text.includes("kegel")) return "cone";
  if (text.includes("kugel")) return "sphere";
  if (text.includes("quader")) return "cuboid";
  if (text.includes("würfel")) return "cube";
  if (text.includes("ansicht")) return "cube";
  return null;
}

function planeTask(i) {
  const [prompt,answer] = planeTasks[i];
  return { prompt, answer, seconds: 30, kind: "geometry", visual: planeVisual(prompt, answer) };
}

function solidTask(i) {
  const [prompt,answer] = solidTasks[i];
  return { prompt, answer, seconds: 30, kind: "solid", visual: solidVisual(prompt, answer) };
}

window.KOPFRECHEN_SETS = Array.from({ length: 40 }, (_, i) => ({
  id: i + 1,
  title: `Set ${String(i + 1).padStart(2, "0")}`,
  tasks: [
    additionTask(i), multiplicationTask(i), divisionTask(i), unitTask(i), estimateTask(i),
    ratioTask(i), chartTask(i), proportionalTask(i), planeTask(i), solidTask(i)
  ].map((task, index) => ({ ...task, number: index + 1, category: CATEGORIES[index] }))
}));

window.KOPFRECHEN_CATEGORIES = CATEGORIES;
