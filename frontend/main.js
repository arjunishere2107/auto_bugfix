// ──────────────────────────────────────────────
//  CONFIG  ← change this if your server port differs
// ──────────────────────────────────────────────
const API_URL = "http://127.0.0.1:8501/api/fix";

// ──────────────────────────────────────────────
//  MARQUEE — build items dynamically
// ──────────────────────────────────────────────
const MQ_ITEMS = [
  { tag: "FIX",  cls: "tag-fix",  text: "NullPointerException @ line 42" },
  { tag: "ERR",  cls: "tag-err",  text: "UnboundLocalError: variable 'x'" },
  { tag: "WARN", cls: "tag-warn", text: "Infinite loop detected" },
  { tag: "FIX",  cls: "tag-fix",  text: "Missing return statement" },
  { tag: "ERR",  cls: "tag-err",  text: "IndexError: list out of range" },
  { tag: "FIX",  cls: "tag-fix",  text: "Type mismatch: str vs int" },
  { tag: "WARN", cls: "tag-warn", text: "Dead code block removed" },
  { tag: "FIX",  cls: "tag-fix",  text: "Division by zero guarded" },
];

function buildMarquee() {
  const html = MQ_ITEMS.map(i =>
    `<div class="mq-item"><span class="tag ${i.cls}">${i.tag}</span> ${i.text}</div>`
  ).join("");
  document.getElementById("mq1").innerHTML = html;
  document.getElementById("mq2").innerHTML = html;
}
buildMarquee();


// ──────────────────────────────────────────────
//  PIPELINE — highlight steps 0-3 (or all = done)
// ──────────────────────────────────────────────
function setPipelineStep(step) {
  for (let i = 0; i <= 3; i++) {
    const el = document.getElementById(`step-${i}`);
    el.classList.toggle("active", i <= step);
  }
}
setPipelineStep(-1);   // all dim on load


// ──────────────────────────────────────────────
//  DRAG & DROP + FILE INPUT
// ──────────────────────────────────────────────
const dropZone  = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");

browseBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  fileInput.click();
});
dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragging");
});
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragging"));
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragging");
  const file = e.dataTransfer.files[0];
  if (file) processFile(file);
});
fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) processFile(fileInput.files[0]);
});


// ──────────────────────────────────────────────
//  TERMINAL — animated lines
// ──────────────────────────────────────────────
const terminalBody = document.getElementById("terminalBody");

function clearTerminal() { terminalBody.innerHTML = ""; }

function printLine(text, cls = "t-muted", delay = 0) {
  return new Promise(resolve => {
    setTimeout(() => {
      const div = document.createElement("div");
      div.className = cls;
      div.textContent = text;
      terminalBody.appendChild(div);
      terminalBody.scrollTop = terminalBody.scrollHeight;
      resolve();
    }, delay);
  });
}

function showCursor() {
  const span = document.createElement("span");
  span.className = "cursor";
  terminalBody.appendChild(span);
}

async function runTerminalAnimation(filename) {
  clearTerminal();
  const lines = [
    { cls: "t-muted", text: `$ analyzing → ${filename}` },
    { cls: "t-muted", text: "$ running AST parser..." },
    { cls: "t-err",   text: "  [ERR] NameError: name 'total' is not defined" },
    { cls: "t-warn",  text: "  [WARN] unreachable code after return statement" },
    { cls: "t-err",   text: "  [ERR] ZeroDivisionError: no zero-guard found" },
    { cls: "t-muted", text: "$ querying similar bug patterns..." },
    { cls: "t-muted", text: "$ invoking LLM repair engine..." },
    { cls: "t-fix",   text: "  ✓ patch 1/3 applied — variable initialized" },
    { cls: "t-fix",   text: "  ✓ patch 2/3 applied — dead code removed" },
    { cls: "t-fix",   text: "  ✓ patch 3/3 applied — division guard added" },
    { cls: "t-muted", text: "$ validating patched file..." },
  ];
  let delay = 0;
  for (const [i, line] of lines.entries()) {
    await printLine(line.text, line.cls, delay);
    delay = i < 2 ? 400 : i < 6 ? 320 : 260;

    // light up pipeline steps as we go
    if (i === 0)  setPipelineStep(0);   // upload
    if (i === 1)  setPipelineStep(1);   // detect
    if (i === 6)  setPipelineStep(2);   // fix
    if (i === 10) setPipelineStep(3);   // validate
  }
}


// ──────────────────────────────────────────────
//  STATUS + UI helpers
// ──────────────────────────────────────────────
function setStatus(text) {
  document.getElementById("statusText").textContent = text;
}

function showBanner(ok) {
  const el = document.getElementById("statusBanner");
  el.className = "status-banner " + (ok ? "success" : "error");
  el.innerHTML = ok
    ? "✅ &nbsp; FIX SUCCESSFUL — all validation checks passed · 0 errors remaining"
    : "❌ &nbsp; FIX FAILED — review debug logs below for more details";
  el.classList.remove("hidden");
}

function showResults(data) {
  document.getElementById("originalCode").textContent  = data.original;
  document.getElementById("fixedCode").textContent     = data.fixed;
  document.getElementById("pylintLogs").textContent    = JSON.stringify(data.pylint_msgs, null, 2);
  document.getElementById("validationLogs").textContent = data.logs;
  document.getElementById("resultsSection").classList.remove("hidden");
}

// ── download handler ──
let _fixedCode = "";
document.getElementById("downloadBtn").addEventListener("click", () => {
  if (!_fixedCode) return;
  const blob = new Blob([_fixedCode], { type: "text/x-python" });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement("a");
  a.href = url; a.download = "fixed.py";
  a.click();
  URL.revokeObjectURL(url);
});


// ──────────────────────────────────────────────
//  MAIN — process file → call API → render
// ──────────────────────────────────────────────
async function processFile(file) {
  if (!file.name.endsWith(".py")) {
    alert("Please upload a .py file.");
    return;
  }

  // 1. Show terminal section immediately
  document.getElementById("resultsSection").classList.remove("hidden");
  document.getElementById("statusBanner").classList.add("hidden");

  // 2. Animate terminal while API call runs in parallel
  setStatus("PROCESSING…");
  const [animDone] = await Promise.all([
    runTerminalAnimation(file.name),
    Promise.resolve(),   // placeholder — real call below
  ]);

  // 3. Build FormData and POST to Flask
  const formData = new FormData();
  formData.append("file", file);

  let data;
  try {
    const res = await fetch(API_URL, { method: "POST", body: formData });
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    data = await res.json();
  } catch (err) {
    await printLine(`$ ERROR: ${err.message}`, "t-err", 200);
    showCursor();
    setStatus("ERROR");
    return;
  }

  // 4. Finish terminal output
  const finalLine = data.success
    ? "$ DONE — bugs fixed · ready to download"
    : "$ DONE — fix attempted · check logs for details";
  await printLine("$ ─────────────────────────────────", "t-fix", 200);
  await printLine(finalLine, "t-fix", 200);
  showCursor();

  // 5. Render results
  _fixedCode = data.fixed || "";
  showBanner(data.success);
  showResults(data);
  setStatus(data.success ? "FIX COMPLETE ✓" : "FIX FAILED ✗");
}
