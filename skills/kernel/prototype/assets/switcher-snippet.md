# In-app variant switcher

For UI prototypes inside a real app: the variants render on the real route,
gated by `?variant=`, and a floating pill switches between them. This file is
the framework-agnostic version; translate it into the app's idiom (a React
component, a Vue component, a server-rendered partial) rather than pasting
vanilla DOM code into a framework that owns the page.

## The contract

1. **Read the variant from the URL.** `?variant=a|b|c`, defaulting to the
   first. Keep every other query parameter.
2. **Swap only the rendered subtree.** Data loading, auth, and route params
   stay above the switch, exactly as the page has them now.

   ```text
   variant = query("variant") or "a"
   render the page shell and data as today
   render VariantA | VariantB | VariantC by variant
   if development: render PrototypeSwitcher
   ```

3. **Each variant is its own component** (`RemindersVariantA`, ...), free to
   throw away the page's existing layout below the shell. Name them so a
   reader sees they are prototypes.
4. **The switcher writes the URL through the app's router** (`router.replace`,
   `navigate(..., { replace: true })`, `history.replaceState` for plain pages)
   so the variant survives a reload and can be shared.
5. **Left and Right arrow keys cycle**, wrapping around, but never while focus
   is in an `input`, `textarea`, `select`, or `contenteditable`, and never
   with a modifier key held.
6. **It never ships.** Mount it only behind a development check:
   `process.env.NODE_ENV !== "production"`, `import.meta.env.DEV`,
   `Rails.env.development?`, `settings.DEBUG`, or the app's feature-flag
   system. The `prototype/<slug>` branch is never merged anyway; this is the
   second lock.
7. **Tradeoff drawer and feedback, as in every prototype.** Inside the app
   there is no docs viewer, so "Pick this" and "Add a note" copy a plain-text
   line to the clipboard for the human to paste back:
   `prototype | <route> | choice: b: Timeline | text: ...`

## Vanilla snippet

Drop into a plain page, or use as the reference when writing the framework
version. It is self-contained: it injects its own styles and markup.

```html
<script>
/* Prototype switcher. Development only. Remove with the prototype branch. */
function mountPrototypeSwitcher({ variants, tradeoffs = {}, onChange }) {
  const ids = variants.map((v) => v.id);
  const q = new URLSearchParams(location.search);
  let cur = ids.includes(q.get("variant")) ? q.get("variant") : ids[0];
  const css = `
    .pps{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:2147483000;display:flex;
      align-items:center;gap:2px;padding:5px;border-radius:999px;background:#1c1c1a;color:#f4f3ef;
      font:14px/1.3 system-ui,sans-serif;box-shadow:0 8px 28px rgba(0,0,0,.25);max-width:calc(100vw - 16px)}
    .pps button{background:none;border:0;color:inherit;font:inherit;padding:7px 9px;border-radius:999px;cursor:pointer;white-space:nowrap}
    .pps button:hover{background:rgba(128,128,128,.3)}
    .pps .l{padding:0 6px;min-width:6em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
    .pps .s{width:1px;align-self:stretch;margin:6px 4px;background:currentColor;opacity:.25}
    .ppd{position:fixed;right:14px;bottom:72px;z-index:2147483000;width:min(340px,calc(100vw - 28px));max-height:60vh;
      overflow:auto;background:#fff;color:#1c1c1a;border:1px solid #ddd;border-radius:10px;padding:10px 14px;
      font:13.5px/1.45 system-ui,sans-serif;box-shadow:0 8px 28px rgba(0,0,0,.2);display:none}
    .ppd.open{display:block}.ppd h4{margin:8px 0 2px}.ppd ul{margin:0 0 6px;padding-left:18px}
    .ppd .on{border-left:3px solid #2f5bd3;padding-left:8px;margin-left:-11px}`;
  const style = document.createElement("style"); style.textContent = css; document.head.appendChild(style);
  const bar = document.createElement("nav"); bar.className = "pps"; bar.setAttribute("aria-label", "Prototype variants");
  bar.innerHTML = '<button data-a="prev" aria-label="Previous variant">&#8249;</button><span class="l"></span>' +
    '<button data-a="next" aria-label="Next variant">&#8250;</button><span class="s"></span>' +
    '<button data-a="pick">Pick this</button><button data-a="note">Add a note</button><button data-a="trade">Tradeoffs</button>';
  const drawer = document.createElement("aside"); drawer.className = "ppd";
  document.body.append(bar, drawer);

  const name = () => variants.find((v) => v.id === cur).name;
  function render() {
    bar.querySelector(".l").textContent = cur.toUpperCase() + "  " + name();
    drawer.innerHTML = "";
    for (const v of variants) {
      const t = tradeoffs[v.id] || { gains: [], gives: [] };
      const sec = document.createElement("section"); if (v.id === cur) sec.className = "on";
      const h = document.createElement("h4"); h.textContent = v.id.toUpperCase() + ". " + v.name; sec.appendChild(h);
      for (const [label, items] of [["Gains", t.gains], ["Gives up", t.gives]]) {
        const ul = document.createElement("ul");
        for (const x of items) { const li = document.createElement("li"); li.textContent = label + ": " + x; ul.appendChild(li); }
        sec.appendChild(ul);
      }
      drawer.appendChild(sec);
    }
  }
  function go(id) {
    cur = id;
    const p = new URLSearchParams(location.search); p.set("variant", id);
    history.replaceState(history.state, "", location.pathname + "?" + p + location.hash); // or the app's router
    render(); if (onChange) onChange(id);
  }
  const step = (d) => go(ids[(ids.indexOf(cur) + d + ids.length) % ids.length]);
  async function feedback(text) {
    const line = "prototype | " + location.pathname + " | choice: " + cur + ": " + name() + " | text: " + text;
    try { await navigator.clipboard.writeText(line); alert("Copied. Paste it into the chat:\n\n" + line); }
    catch (e) { prompt("Copy this line into the chat:", line); }
  }
  bar.addEventListener("click", (e) => {
    const a = e.target.closest("button") && e.target.closest("button").dataset.a;
    if (a === "prev") step(-1);
    if (a === "next") step(1);
    if (a === "pick") feedback("picked");
    if (a === "note") { const t = prompt("Note on " + name() + ":"); if (t) feedback(t); }
    if (a === "trade") drawer.classList.toggle("open");
  });
  document.addEventListener("keydown", (e) => {
    if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
    if (e.target.closest && e.target.closest("input, textarea, select, [contenteditable]:not([contenteditable='false'])")) return;
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
  });
  render();
  return cur;
}

/* Usage. Gate it: never in production. */
if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
  mountPrototypeSwitcher({
    variants: [{ id: "a", name: "One form" }, { id: "b", name: "Timeline" }, { id: "c", name: "Inbox preview" }],
    tradeoffs: {
      a: { gains: ["Every rule in one place"], gives: ["Cannot see what the customer reads"] },
      b: { gains: ["When things happen is obvious"], gives: ["Global rules have no home"] },
      c: { gains: ["Shows the real message"], gives: ["Timing is one click deeper"] },
    },
    onChange: (id) => location.reload(), // or re-render the variant subtree in place
  });
}
</script>
```

In a framework, keep the pieces and drop the DOM building: the pill and the
drawer become one `PrototypeSwitcher` component in wherever the app keeps
shared UI, `go()` calls the router, and the development check wraps the
component's mount, not its insides.
