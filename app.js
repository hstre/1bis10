const app = document.querySelector("#app");
const sets = window.KOPFRECHEN_SETS;

const state = {
  screen: "home",
  setIndex: Number(localStorage.getItem("lastSet") || 0),
  taskIndex: 0,
  running: false,
  elapsed: 0,
  startedAt: 0,
  raf: null,
  autoAdvance: localStorage.getItem("autoAdvance") !== "false",
  sequenceShown: 1,
  sequenceTimer: null,
  visualHidden: false,
  visualTimer: null
};

const esc = value => String(value).replace(/[&<>'"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[char]));
const currentSet = () => sets[state.setIndex];
const currentTask = () => currentSet().tasks[state.taskIndex];

function header(title, meta = "") {
  return `<header class="topbar"><button class="ghost home-button" data-action="home" aria-label="Zur Startseite">1 bis 10</button><div class="top-title">${esc(title)}</div><div class="top-meta">${esc(meta)}</div></header>`;
}

function taskVisual(type) {
  const shapes = {
    square: `<rect x="70" y="35" width="150" height="150"/>`,
    rectangle: `<rect x="45" y="60" width="200" height="120"/>`,
    quadrilateral: `<polygon points="55,45 245,65 215,200 75,180"/>`,
    triangle: `<polygon points="145,30 245,190 45,190"/>`,
    "equilateral-triangle": `<polygon points="145,25 245,195 45,195"/>`,
    "isosceles-triangle": `<polygon points="145,25 235,195 55,195"/>`,
    "right-triangle": `<polygon points="55,35 55,195 245,195"/><path d="M55 170 H80 V195"/>`,
    pentagon: `<polygon points="145,22 245,95 205,205 85,205 45,95"/>`,
    hexagon: `<polygon points="80,30 210,30 270,115 210,200 80,200 20,115"/>`,
    octagon: `<polygon points="90,25 200,25 265,90 265,155 200,220 90,220 25,155 25,90"/>`,
    decagon: `<polygon points="145,18 215,40 258,98 258,160 215,210 145,226 75,210 32,160 32,98 75,40"/>`,
    dodecagon: `<polygon points="100,20 190,20 235,45 270,90 270,155 235,200 190,225 100,225 55,200 20,155 20,90 55,45"/>`,
    trapezoid: `<polygon points="85,45 205,45 260,195 30,195"/>`,
    parallelogram: `<polygon points="85,45 250,45 205,195 40,195"/>`,
    rhombus: `<polygon points="145,20 250,120 145,220 40,120"/>`,
    circle: `<circle cx="145" cy="120" r="95"/><circle class="point" cx="145" cy="120" r="5"/>`,
    line: `<path d="M35 185 L255 45"/><circle class="point" cx="70" cy="163" r="6"/><circle class="point" cx="220" cy="67" r="6"/>`,
    cube: `<rect x="45" y="75" width="130" height="130"/><rect x="105" y="30" width="130" height="130"/><path d="M45 75 L105 30 M175 75 L235 30 M175 205 L235 160 M45 205 L105 160"/>`,
    cuboid: `<rect x="35" y="90" width="165" height="105"/><rect x="90" y="45" width="165" height="105"/><path d="M35 90 L90 45 M200 90 L255 45 M200 195 L255 150 M35 195 L90 150"/>`,
    "square-pyramid": `<polygon points="45,165 145,210 245,165 145,125"/><path d="M145 25 L45 165 M145 25 L145 210 M145 25 L245 165 M145 25 L145 125"/>`,
    tetrahedron: `<polygon points="145,25 45,205 245,205"/><path d="M145 25 L145 145 M45 205 L145 145 L245 205"/>`,
    sphere: `<circle cx="145" cy="120" r="95"/><ellipse cx="145" cy="120" rx="95" ry="34"/><path class="soft" d="M145 25 C95 70 95 170 145 215 M145 25 C195 70 195 170 145 215"/>`,
    cylinder: `<ellipse cx="145" cy="45" rx="90" ry="28"/><path d="M55 45 V195 M235 45 V195"/><ellipse cx="145" cy="195" rx="90" ry="28"/><path class="soft" d="M55 195 C70 225 220 225 235 195"/>`,
    cone: `<ellipse cx="145" cy="195" rx="95" ry="28"/><path d="M145 25 L50 195 M145 25 L240 195"/><path class="soft" d="M50 195 C70 225 220 225 240 195"/>`,
    "cube-net": `<g transform="translate(25 10)"><rect x="80" y="0" width="55" height="55"/><rect x="0" y="55" width="55" height="55"/><rect x="55" y="55" width="55" height="55"/><rect x="110" y="55" width="55" height="55"/><rect x="165" y="55" width="55" height="55"/><rect x="80" y="110" width="55" height="55"/></g>`
  };
  if (!type || !shapes[type]) return "";
  return `<svg class="task-diagram" viewBox="0 0 290 240" role="img" aria-label="Passende geometrische Darstellung">${shapes[type]}</svg>`;
}

function renderHome() {
  state.screen = "home";
  clearVisualFlash();
  stopClock();
  const buttons = sets.map((set, i) => `<button class="set-button ${i === state.setIndex ? "selected" : ""}" data-set="${i}">${String(set.id).padStart(2,"0")}</button>`).join("");
  app.innerHTML = `
    <section class="home-shell">
      <div class="brand"><span class="brand-number">1–10</span><div><h1>Kopfrechnen</h1><p>Klasse 6 · 40 feste Durchgänge</p></div></div>
      <div class="set-picker" aria-label="Set auswählen">${buttons}</div>
      <div class="home-actions">
        <button class="primary" data-action="start">${esc(currentSet().title)} starten</button>
        <button class="secondary" data-action="review">Kontrollansicht</button>
      </div>
      <a class="download-card" href="output/pdf/1bis10-uebungsheft-klasse6.pdf?v=3" download>
        <span><strong>Übungsheft als PDF</strong><small>400 Übungsseiten · 4.000 Aufgaben · mit Lösungen</small></span>
        <b>Herunterladen ↓</b>
      </a>
      <a class="download-card evaluation-card" href="output/pdf/auswerteblatt-1bis10.pdf?v=2" download>
        <span><strong>Auswerteblatt für Schüler</strong><small>40 Sets × 10 Aufgabentypen · A4 quer</small></span>
        <b>Herunterladen ↓</b>
      </a>
      <a class="download-card evaluation-card" href="output/pdf/kopfrechen-kartenspiel.pdf?v=4" download>
        <span><strong>Kopfrechen-Duell als Kartenspiel</strong><small>Spielanleitung · 120 Karten · 10 Ausschneidebögen</small></span>
        <b>Herunterladen ↓</b>
      </a>
      <details class="trick-downloads">
        <summary>
          <span><strong>10 Rechentricks-Heftchen</strong><small>Je 8 Seiten · Erklären · Üben · Lösungen</small></span>
          <b>Auswählen ↓</b>
        </summary>
        <div class="trick-grid">
          <a href="output/pdf/rechentricks/01-addition-subtraktion.pdf?v=5" download><span>01</span>Addition und Subtraktion</a>
          <a href="output/pdf/rechentricks/02-multiplikation.pdf?v=5" download><span>02</span>Multiplikation</a>
          <a href="output/pdf/rechentricks/03-division.pdf?v=5" download><span>03</span>Division</a>
          <a href="output/pdf/rechentricks/04-einheiten.pdf?v=5" download><span>04</span>Einheiten</a>
          <a href="output/pdf/rechentricks/05-schaetzen.pdf?v=5" download><span>05</span>Schätzen</a>
          <a href="output/pdf/rechentricks/06-verhaeltnisse.pdf?v=5" download><span>06</span>Verhältnisse</a>
          <a href="output/pdf/rechentricks/07-diagramme.pdf?v=5" download><span>07</span>Diagramme</a>
          <a href="output/pdf/rechentricks/08-zwei-dreisatz.pdf?v=5" download><span>08</span>Zwei- und Dreisatz</a>
          <a href="output/pdf/rechentricks/09-ebene-figuren.pdf?v=5" download><span>09</span>Ebene Figuren</a>
          <a href="output/pdf/rechentricks/10-koerper-raum.pdf?v=5" download><span>10</span>Körper und Raum</a>
        </div>
      </details>
      <label class="toggle"><input type="checkbox" id="autoAdvance" ${state.autoAdvance ? "checked" : ""}><span>Nach Ablauf der Zeit automatisch weiter</span></label>
      <p class="key-help">Leertaste: Pause · Pfeiltasten: weiter/zurück · F: Vollbild</p>
    </section>`;
}

function taskBody(task) {
  if (task.kind === "equation") return `<div class="equation">${esc(task.display)}</div>`;
  if (task.kind === "sequence") {
    const index = Math.min(state.sequenceShown - 1, task.values.length - 1);
    const value = task.values[index];
    const label = index === 0 ? value : signed(value);
    return `<div class="sequence"><span class="number-chip ${value < 0 ? "negative" : "positive"}">${esc(label)}</span></div>`;
  }
  if (task.kind === "receipt") return `<div class="receipt">${task.detail.map(([a,b]) => `<div><span>${esc(a)}</span><strong>${esc(b)}</strong></div>`).join("")}</div>`;
  if (task.kind === "choices") return `<div class="choices">${task.choices.map(c => `<div>${esc(c)}</div>`).join("")}</div>`;
  if (task.kind === "ratio") return `<div class="ratio-grid" style="--cols:${Math.min(task.total,6)}">${Array.from({length: task.total}, (_,i) => `<span class="${i < task.filled ? "filled" : ""}"></span>`).join("")}</div>`;
  if (task.kind === "chart") {
    const max = Math.max(...task.values);
    if (task.chartMode === "table") return `<table class="mini-table"><thead><tr>${task.labels.map(label => `<th>${esc(label)}</th>`).join("")}</tr></thead><tbody><tr>${task.values.map(value => `<td>${value}</td>`).join("")}</tr></tbody></table>`;
    if (task.chartMode === "line") {
      const points = task.values.map((v,i) => `${50 + i*140},${220 - (v/max)*170}`).join(" ");
      return `<div class="line-chart"><svg viewBox="0 0 380 250" role="img" aria-label="Liniendiagramm"><path d="M35 25 V220 H360"/><polyline points="${points}"/>${task.values.map((v,i) => `<circle cx="${50+i*140}" cy="${220-(v/max)*170}" r="7"/><text x="${50+i*140}" y="242">${esc(task.labels[i])}</text>${task.showValues ? `<text x="${50+i*140}" y="${205-(v/max)*170}">${v}</text>` : ""}`).join("")}</svg></div>`;
    }
    return `<div class="chart" aria-label="Säulendiagramm">${task.values.map((v,i) => `<div class="bar-column">${task.showValues ? `<span>${v}</span>` : ""}<div class="bar" style="height:${Math.round(v/max*190)}px"></div><strong>${esc(task.labels[i])}</strong></div>`).join("")}</div>`;
  }
  if (task.kind === "geometry" || task.kind === "solid") {
    return state.visualHidden
      ? `<div class="diagram-placeholder" aria-hidden="true"></div>`
      : taskVisual(task.visual);
  }
  return "";
}

function signed(value) { return value >= 0 ? `+ ${value}` : `− ${Math.abs(value)}`; }

function renderTask(reset = true) {
  state.screen = "task";
  if (reset) {
    clearVisualFlash();
    stopClock();
    state.elapsed = 0;
    state.sequenceShown = 1;
    state.visualHidden = false;
  }
  const task = currentTask();
  app.innerHTML = `
    <section class="task-screen">
      ${header(`Aufgabe ${task.number}`, `${task.seconds} Sekunden`)}
      <div class="task-category">${esc(task.category)}</div>
      <div class="task-content">
        <h2>${esc(task.prompt)}</h2>
        ${taskBody(task)}
      </div>
      <div class="controls">
        <button class="ghost" data-action="prev" aria-label="Vorherige Aufgabe">‹</button>
        <button class="pause" data-action="toggle">${state.running ? "Pause" : state.elapsed ? "Weiter" : "Start"}</button>
        <button class="ghost" data-action="next" aria-label="Nächste Aufgabe">›</button>
      </div>
      <div class="timer" aria-label="Verbleibende Zeit">
        <div class="timer-blue"></div><div class="timer-red"></div>
      </div>
    </section>`;
  updateProgress();
  scheduleVisualFlash();
}

function clearVisualFlash() {
  if (state.visualTimer) clearTimeout(state.visualTimer);
  state.visualTimer = null;
}

function scheduleVisualFlash() {
  const task = currentTask();
  if ((task.kind !== "geometry" && task.kind !== "solid") || state.visualHidden || state.visualTimer) return;
  state.visualTimer = setTimeout(() => {
    state.visualTimer = null;
    state.visualHidden = true;
    document.querySelector(".task-diagram")?.classList.add("flash-hidden");
  }, 2500);
}

function startClock() {
  if (state.running) return;
  state.running = true;
  state.startedAt = performance.now() - state.elapsed;
  if (currentTask().kind === "sequence") scheduleSequence();
  renderTask(false);
  state.startedAt = performance.now() - state.elapsed;
  state.running = true;
  state.raf = requestAnimationFrame(tick);
}

function stopClock() {
  if (state.running) state.elapsed = performance.now() - state.startedAt;
  state.running = false;
  if (state.raf) cancelAnimationFrame(state.raf);
  if (state.sequenceTimer) clearTimeout(state.sequenceTimer);
  state.raf = null;
  state.sequenceTimer = null;
}

function tick(now) {
  if (!state.running) return;
  state.elapsed = now - state.startedAt;
  const limit = currentTask().seconds * 1000;
  if (state.elapsed >= limit) {
    state.elapsed = limit;
    updateProgress();
    stopClock();
    if (state.autoAdvance) setTimeout(nextTask, 650);
    else renderTask(false);
    return;
  }
  updateProgress();
  state.raf = requestAnimationFrame(tick);
}

function updateProgress() {
  const task = currentTask();
  const p = Math.min(1, state.elapsed / (task.seconds * 1000));
  const blue = document.querySelector(".timer-blue");
  const red = document.querySelector(".timer-red");
  if (!blue || !red) return;
  blue.style.width = `${Math.min(p, .8) * 100}%`;
  red.style.width = `${Math.max(0, p - .8) * 100}%`;
}

function scheduleSequence() {
  const task = currentTask();
  if (task.kind !== "sequence" || state.sequenceShown >= task.values.length) return;
  const interval = Math.min(3500, (task.seconds * 1000 * .55) / task.values.length);
  state.sequenceTimer = setTimeout(() => {
    state.sequenceShown++;
    const box = document.querySelector(".sequence");
    const index = state.sequenceShown - 1;
    const value = task.values[index];
    const label = index === 0 ? value : signed(value);
    if (box) box.innerHTML = `<span class="number-chip ${value < 0 ? "negative" : "positive"}">${esc(label)}</span>`;
    scheduleSequence();
  }, interval);
}

function nextTask() {
  stopClock();
  if (state.taskIndex < 9) {
    state.taskIndex++;
    renderTask();
    startClock();
  } else renderPensDown();
}

function previousTask() {
  stopClock();
  state.taskIndex = Math.max(0, state.taskIndex - 1);
  renderTask();
}

function renderPensDown() {
  state.screen = "pens";
  stopClock();
  app.innerHTML = `<section class="message-screen">${header("Geschafft", currentSet().title)}<div class="message-mark">✕</div><h1>Stifte weg!</h1><button class="primary" data-action="solutions">Lösungen anzeigen</button></section>`;
}

function renderSolutions() {
  state.screen = "solutions";
  const rows = currentSet().tasks.map(t => `<div class="solution-row"><span>${t.number}</span><div><small>${esc(t.category)}</small><strong>${esc(t.answer)}</strong></div></div>`).join("");
  app.innerHTML = `<section class="solutions-screen">${header("Lösungen", currentSet().title)}<div class="solutions-grid">${rows}</div><div class="solution-actions"><button class="secondary" data-action="home">Zur Auswahl</button><button class="primary" data-action="restart">Noch einmal</button></div></section>`;
}

function renderReview() {
  state.screen = "review";
  const rows = currentSet().tasks.map(t => `<tr><td>${t.number}</td><td>${esc(t.category)}</td><td>${esc(t.prompt)}${t.display ? `<br><strong>${esc(t.display)}</strong>` : ""}</td><td>${esc(t.answer)}${t.detail && typeof t.detail === "string" ? `<br><small>${esc(t.detail)}</small>` : ""}</td><td>${t.seconds} s</td></tr>`).join("");
  app.innerHTML = `<section class="review-screen">${header("Kontrollansicht", currentSet().title)}<div class="review-actions"><button class="secondary" data-action="home">Zurück</button><button class="primary" data-action="print">Drucken</button></div><table><thead><tr><th>Nr.</th><th>Klasse</th><th>Aufgabe</th><th>Lösung</th><th>Zeit</th></tr></thead><tbody>${rows}</tbody></table></section>`;
}

function chooseSet(index) {
  state.setIndex = index;
  localStorage.setItem("lastSet", index);
  renderHome();
}

function begin() {
  state.taskIndex = 0;
  state.elapsed = 0;
  renderTask();
}

app.addEventListener("click", event => {
  const setButton = event.target.closest("[data-set]");
  if (setButton) return chooseSet(Number(setButton.dataset.set));
  const action = event.target.closest("[data-action]")?.dataset.action;
  if (!action) return;
  if (action === "home") renderHome();
  if (action === "start" || action === "restart") begin();
  if (action === "review") renderReview();
  if (action === "toggle") state.running ? (stopClock(), renderTask(false)) : startClock();
  if (action === "next") nextTask();
  if (action === "prev") previousTask();
  if (action === "solutions") renderSolutions();
  if (action === "print") window.print();
});

app.addEventListener("change", event => {
  if (event.target.id === "autoAdvance") {
    state.autoAdvance = event.target.checked;
    localStorage.setItem("autoAdvance", String(state.autoAdvance));
  }
});

document.addEventListener("keydown", event => {
  if (event.key.toLowerCase() === "f") document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
  if (state.screen !== "task") return;
  if (event.code === "Space") { event.preventDefault(); state.running ? (stopClock(), renderTask(false)) : startClock(); }
  if (event.key === "ArrowRight") nextTask();
  if (event.key === "ArrowLeft") previousTask();
});

if ("serviceWorker" in navigator) window.addEventListener("load", () => navigator.serviceWorker.register("./sw.js?v=18"));
renderHome();
