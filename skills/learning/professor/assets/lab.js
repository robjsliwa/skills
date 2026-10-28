// lab.js: a "done" tick on every lab step, remembered in this browser, and a
// progress bar. Optional: the page reads correctly without it.
(function () {
  "use strict";
  const steps = Array.from(document.querySelectorAll(".lab-step[id]"));
  if (!steps.length) return;
  const key = "lab-done:" + location.pathname;
  let done = {};
  try { done = JSON.parse(localStorage.getItem(key) || "{}"); } catch (e) { done = {}; }
  const bar = document.createElement("div");
  bar.className = "lab-progress";
  document.body.appendChild(bar);
  const save = () => { try { localStorage.setItem(key, JSON.stringify(done)); } catch (e) { /* private mode */ } };
  const paint = () => {
    steps.forEach((s) => s.classList.toggle("is-done", !!done[s.id]));
    bar.style.width = `${(100 * steps.filter((s) => done[s.id]).length) / steps.length}%`;
  };
  steps.forEach((s) => {
    const h = s.querySelector("h3");
    if (!h) return;
    const label = document.createElement("label");
    const box = document.createElement("input");
    box.type = "checkbox";
    box.checked = !!done[s.id];
    box.addEventListener("change", () => { done[s.id] = box.checked; save(); paint(); });
    label.append(box, " done");
    h.appendChild(label);
  });
  paint();
})();
