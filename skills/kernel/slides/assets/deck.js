// deck.js: runs a lecture deck written per the slides skill's DECK-FORMAT.md.
//
//   <div class="deck" data-title="Lesson 2 · One Phone, Many Views">
//     <section class="slide" id="hook">
//       <div class="canvas"> ...data-step="1" reveals at step 1; data-hl="2" highlights at step 2... </div>
//       <aside class="transcript"> <p>...</p> <p data-step="1">...</p> </aside>
//     </section>
//   </div>
//   <script src="../../assets/deck.js"></script>
//
// Keys: → space j next · ← k previous · Home End · t transcript · h handout · f fullscreen
// URL:  #/3/2 opens slide 3 at step 2. ?handout shows every slide fully built.
// ?check lays the deck out as a handout and writes layout problems as JSON
// into <pre id="deck-check"> (the slides skill's render_deck.py reads it).
(function () {
  "use strict";
  const deck = document.querySelector(".deck");
  if (!deck) return;
  const slides = Array.from(deck.querySelectorAll(":scope > section.slide"));
  const params = new URLSearchParams(location.search);

  // Arrowheads and the hand-drawn wobble, once per page.
  const NS = "http://www.w3.org/2000/svg";
  const defs = document.createElementNS(NS, "svg");
  defs.setAttribute("width", "0");
  defs.setAttribute("height", "0");
  defs.setAttribute("aria-hidden", "true");
  defs.style.position = "absolute";
  const marker = (id, color) =>
    `<marker id="${id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">` +
    `<path d="M0 0 L10 5 L0 10 z" fill="${color}"/></marker>`;
  defs.innerHTML =
    "<defs>" +
    marker("arr", "#1d1b18") + marker("arr-acc", "#a3410f") +
    marker("arr-ok", "#1f6b3d") + marker("arr-bad", "#a52a1d") +
    '<filter id="deck-sketch" x="-5%" y="-5%" width="110%" height="110%">' +
    '<feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="3"/>' +
    '<feDisplacementMap in="SourceGraphic" scale="1.1"/></filter>' +
    "</defs>";
  document.body.prepend(defs);

  const stepsOf = (s) => {
    let m = 0;
    s.querySelectorAll("[data-step], [data-hl]").forEach((e) => {
      const v = parseInt(e.dataset.step || e.dataset.hl, 10);
      if (v > m) m = v;
    });
    return m;
  };
  const maxSteps = slides.map(stepsOf);
  slides.forEach((s, i) => s.setAttribute("data-n", `${i + 1} / ${slides.length}${s.id ? " · " + s.id : ""}`));

  // Bottom bar.
  const bar = document.createElement("div");
  bar.className = "deck-bar";
  bar.innerHTML =
    '<button type="button" data-act="prev" aria-label="Previous">←</button>' +
    '<span class="count"></span><div class="track"><div class="fillbar"></div></div>' +
    '<span class="keys">→ next · t transcript · h handout</span>' +
    '<button type="button" data-act="next" aria-label="Next">→</button>';
  document.body.appendChild(bar);

  let cur = 0;
  let step = 0;

  function parseHash() {
    const m = location.hash.match(/^#\/(\d+)(?:\/(\d+))?/);
    if (!m) return;
    cur = Math.min(Math.max(parseInt(m[1], 10) - 1, 0), slides.length - 1);
    step = Math.min(Math.max(parseInt(m[2] || "0", 10), 0), maxSteps[cur]);
  }

  function show() {
    slides.forEach((s, i) => s.classList.toggle("current", i === cur));
    const s = slides[cur];
    s.querySelectorAll("[data-step]").forEach((e) => {
      const v = parseInt(e.dataset.step, 10);
      e.classList.toggle("future", v > step);
      e.classList.toggle("now", v === step && step > 0);
    });
    s.querySelectorAll("[data-hl]").forEach((e) => {
      e.classList.toggle("now", parseInt(e.dataset.hl, 10) === step);
    });
    const paras = Array.from(s.querySelectorAll(".transcript > *"));
    const visible = paras.filter((p) => !p.classList.contains("future"));
    visible.forEach((p, i) => p.classList.toggle("past", i < visible.length - 1 && step > 0 && p.dataset.step !== String(step)));
    const total = maxSteps.reduce((a, b) => a + b + 1, 0);
    const done = maxSteps.slice(0, cur).reduce((a, b) => a + b + 1, 0) + step + 1;
    bar.querySelector(".fillbar").style.width = `${(100 * done) / total}%`;
    bar.querySelector(".count").textContent =
      `${cur + 1} / ${slides.length}` + (maxSteps[cur] ? ` · step ${step}/${maxSteps[cur]}` : "");
    const title = deck.dataset.title || document.title;
    document.title = `${title} · ${cur + 1}/${slides.length}`;
    history.replaceState(null, "", `${location.pathname}${location.search}#/${cur + 1}/${step}`);
    if (document.body.classList.contains("handout")) return;
    const tr = s.querySelector(".transcript");
    if (tr) {
      if (step === 0) tr.scrollTop = 0;
      else if (visible.length) {
        const p = visible[visible.length - 1];
        tr.scrollTop = Math.max(0, p.offsetTop - tr.offsetTop + p.offsetHeight - tr.clientHeight);
      }
    }
  }

  function next() {
    if (step < maxSteps[cur]) step++;
    else if (cur < slides.length - 1) { cur++; step = 0; }
    show();
  }
  function prev() {
    if (step > 0) step--;
    else if (cur > 0) { cur--; step = maxSteps[cur]; }
    show();
  }
  function handout(on) {
    document.body.classList.toggle("handout", on);
    if (!on) show();
  }

  document.addEventListener("keydown", (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
    switch (e.key) {
      case "ArrowRight": case "PageDown": case " ": case "j": e.preventDefault(); next(); break;
      case "ArrowLeft": case "PageUp": case "k": e.preventDefault(); prev(); break;
      case "Home": cur = 0; step = 0; show(); break;
      case "End": cur = slides.length - 1; step = maxSteps[cur]; show(); break;
      case "t": document.body.classList.toggle("no-transcript"); break;
      case "h": handout(!document.body.classList.contains("handout")); break;
      case "f":
        if (document.fullscreenElement) document.exitFullscreen();
        else document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
        break;
    }
  });
  bar.addEventListener("click", (e) => {
    const act = e.target.closest("button") && e.target.closest("button").dataset.act;
    if (act === "next") next();
    if (act === "prev") prev();
  });
  deck.addEventListener("click", (e) => {
    if (document.body.classList.contains("handout")) return;
    if (!e.target.closest(".canvas") || e.target.closest("a, button, details, summary")) return;
    if (String(window.getSelection())) return;
    next();
  });
  let touchX = null;
  deck.addEventListener("touchstart", (e) => { touchX = e.touches[0].clientX; }, { passive: true });
  deck.addEventListener("touchend", (e) => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) (dx < 0 ? next : prev)();
    touchX = null;
  });
  window.addEventListener("hashchange", () => { parseHash(); show(); });

  parseHash();
  show();
  if (params.has("handout") || params.has("check") || location.hash === "#handout") handout(true);
  if (params.has("check")) {
    const run = () => writeCheck(check());
    (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => setTimeout(run, 50));
  }

  // ---------------------------------------------------------------- check
  function words(el) {
    const clone = el.cloneNode(true);
    clone.querySelectorAll("pre, svg, table, .source").forEach((n) => n.remove());
    return (clone.textContent.trim().match(/\S+/g) || []).length;
  }
  function overlap(a, b) {
    const w = Math.min(a.right, b.right) - Math.max(a.left, b.left);
    const h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    return w > 1 && h > 1 ? w * h : 0;
  }
  function check() {
    const issues = [];
    const add = (i, kind, detail) => issues.push({ slide: i + 1, id: slides[i].id || null, kind, detail });
    slides.forEach((s, i) => {
      const canvas = s.querySelector(":scope > .canvas");
      const tr = s.querySelector(":scope > .transcript");
      if (!canvas) { add(i, "structure", "slide has no .canvas"); return; }
      if (!tr || !tr.textContent.trim()) add(i, "structure", "slide has no transcript");
      if (!s.id) add(i, "structure", "slide has no id");
      if (canvas.scrollHeight > canvas.clientHeight + 2 || canvas.scrollWidth > canvas.clientWidth + 2)
        add(i, "overflow", `canvas content ${canvas.scrollWidth}x${canvas.scrollHeight} exceeds ${canvas.clientWidth}x${canvas.clientHeight}`);
      const box = canvas.getBoundingClientRect();
      canvas.querySelectorAll("pre").forEach((p) => {
        if (p.scrollWidth > p.clientWidth + 2) add(i, "overflow", "a code block is wider than its box; shorten lines or cut the slice");
      });
      const n = words(canvas);
      const limit = s.classList.contains("prompt") ? 45 : 32;
      if (n > limit) add(i, "dense", `${n} words on the canvas (limit ${limit}); move prose to the transcript`);
      // steps are 1..max with no gaps, and every transcript step has a canvas step
      const canvasSteps = new Set(Array.from(canvas.querySelectorAll("[data-step], [data-hl]")).map((e) => parseInt(e.dataset.step || e.dataset.hl, 10)));
      for (let k = 1; k <= maxSteps[i]; k++) if (!canvasSteps.has(k)) add(i, "steps", `no canvas element reveals at step ${k}`);
      if (tr) tr.querySelectorAll("[data-step]").forEach((p) => {
        const k = parseInt(p.dataset.step, 10);
        if (k > 0 && !canvasSteps.has(k)) add(i, "steps", `transcript step ${k} has nothing on the canvas`);
      });
      // svg labels: overlaps and escapes
      canvas.querySelectorAll("svg").forEach((svg) => {
        const sb = svg.getBoundingClientRect();
        const texts = Array.from(svg.querySelectorAll("text")).map((t) => ({ t, r: t.getBoundingClientRect() }));
        texts.forEach(({ t, r }) => {
          if (r.left < sb.left - 1 || r.right > sb.right + 1 || r.top < sb.top - 1 || r.bottom > sb.bottom + 1)
            add(i, "label", `"${t.textContent.trim()}" runs outside its figure`);
          if (r.right > box.right + 1 || r.bottom > box.bottom + 1) add(i, "label", `"${t.textContent.trim()}" runs off the canvas`);
        });
        for (let a = 0; a < texts.length; a++)
          for (let b = a + 1; b < texts.length; b++)
            if (overlap(texts[a].r, texts[b].r) > 4)
              add(i, "label", `"${texts[a].t.textContent.trim()}" overlaps "${texts[b].t.textContent.trim()}"`);
      });
    });
    return { slides: slides.length, steps: maxSteps, issues };
  }
  function writeCheck(result) {
    let pre = document.getElementById("deck-check");
    if (!pre) {
      pre = document.createElement("pre");
      pre.id = "deck-check";
      pre.style.display = "none";
      document.body.appendChild(pre);
    }
    pre.textContent = JSON.stringify(result);
  }
})();
