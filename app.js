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
  sequenceTimer: null
};

const esc = value => String(value).replace(/[&<>'"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[char]));
const currentSet = () => sets[state.setIndex];
const currentTask = () => currentSet().tasks[state.taskIndex];

function header(title, meta = "") {
  return `<header class="topbar"><button class="ghost home-button" data-action="home" aria-label="Zur Startseite">1 bis 10</button><div class="top-title">${esc(title)}</div><div class="top-meta">${esc(meta)}</div></header>`;
}

function renderHome() {
  state.screen = "home";
  stopClock();
  const buttons = sets.map((set, i) => `<button class="set-button ${i === state.setIndex ? "selected" : ""}" data-set="${i}">${String(set.id).padStart(2,"0")}</button>`).join("");
  app.innerHTML = `
    <section class="home-shell">
      <div class="brand"><span class="brand-number">1–10</span><div><h1>Kopfrechnen</h1><p>Klasse 5 · 40 feste Durchgänge</p></div></div>
      <div class="set-picker" aria-label="Set auswählen">${buttons}</div>
      <div class="home-actions">
        <button class="primary" data-action="start">${esc(currentSet().title)} starten</button>
        <button class="secondary" data-action="review">Kontrollansicht</button>
      </div>
      <label class="toggle"><input type="checkbox" id="autoAdvance" ${state.autoAdvance ? "checked" : ""}><span>Nach Ablauf der Zeit automatisch weiter</span></label>
      <p class="key-help">Leertaste: Pause · Pfeiltasten: weiter/zurück · F: Vollbild</p>
    </section>`;
}

function taskBody(task) {
  if (task.kind === "equation") return `<div class="equation">${esc(task.display)}</div>`;
  if (task.kind === "sequence") {
    const shown = task.values.slice(0, state.sequenceShown).map((v,i) => `<span class="number-chip ${v < 0 ? "negative" : "positive"}">${i === 0 ? esc(v) : esc(signed(v))}</span>`).join("");
    return `<div class="sequence">${shown}</div>`;
  }
  if (task.kind === "receipt") return `<div class="receipt">${task.detail.map(([a,b]) => `<div><span>${esc(a)}</span><strong>${esc(b)}</strong></div>`).join("")}</div>`;
  if (task.kind === "choices") return `<div class="choices">${task.choices.map(c => `<div>${esc(c)}</div>`).join("")}</div>`;
  if (task.kind === "ratio") return `<div class="ratio-grid" style="--cols:${Math.min(task.total,6)}">${Array.from({length: task.total}, (_,i) => `<span class="${i < task.filled ? "filled" : ""}"></span>`).join("")}</div>`;
  if (task.kind === "chart") {
    const max = Math.max(...task.values);
    if (task.chartMode === "table") return `<table class="mini-table"><thead><tr>${task.labels.map(label => `<th>${esc(label)}</th>`).join("")}</tr></thead><tbody><tr>${task.values.map(value => `<td>${value}</td>`).join("")}</tr></tbody></table>`;
    if (task.chartMode === "line") {
      const points = task.values.map((v,i) => `${50 + i*140},${220 - (v/max)*170}`).join(" ");
      return `<div class="line-chart"><svg viewBox="0 0 380 250" role="img" aria-label="Liniendiagramm"><path d="M35 25 V220 H360"/><polyline points="${points}"/>${task.values.map((v,i) => `<circle cx="${50+i*140}" cy="${220-(v/max)*170}" r="7"/><text x="${50+i*140}" y="242">${esc(task.labels[i])}</text><text x="${50+i*140}" y="${205-(v/max)*170}">${v}</text>`).join("")}</svg></div>`;
    }
    return `<div class="chart" aria-label="Säulendiagramm">${task.values.map((v,i) => `<div class="bar-column"><span>${v}</span><div class="bar" style="height:${Math.round(v/max*190)}px"></div><strong>${esc(task.labels[i])}</strong></div>`).join("")}</div>`;
  }
  if (task.kind === "geometry" || task.kind === "solid") return `<div class="geometry-symbol" aria-hidden="true">${esc(task.symbol)}</div>`;
  return "";
}

function signed(value) { return value >= 0 ? `+ ${value}` : `− ${Math.abs(value)}`; }

function renderTask(reset = true) {
  state.screen = "task";
  if (reset) {
    stopClock();
    state.elapsed = 0;
    state.sequenceShown = 1;
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
    if (box) box.innerHTML = task.values.slice(0, state.sequenceShown).map((v,i) => `<span class="number-chip ${v < 0 ? "negative" : "positive"}">${i === 0 ? esc(v) : esc(signed(v))}</span>`).join("");
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

if ("serviceWorker" in navigator) window.addEventListener("load", () => navigator.serviceWorker.register("./sw.js"));
renderHome();
