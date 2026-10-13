#!/usr/bin/env python3
"""Local docs viewer: renders markdown and Mermaid, records choices and comments.

Usage:
  docs_viewer.py [--root .] [--port 4178] [--open]

Binds 127.0.0.1 only. Lists markdown under docs/ plus root CONTEXT.md,
GLOSSARY.md, README.md and CLAUDE.md. Renders in the browser with marked and
Mermaid from jsDelivr, reloads the open file when it changes, shows options
blocks as cards with a Choose button, previews mockups in a frame, and lets the
user click a diagram node to comment. Choices and comments append JSON lines
to <root>/.viewer/events.jsonl for the agent to read.

Python 3 standard library only.
"""

import argparse
import datetime
import json
import os
import re
import sys
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT_FILES = ("CONTEXT.md", "GLOSSARY.md", "README.md", "CLAUDE.md")
SKIP_DIRS = {".git", "node_modules", ".viewer"}
DEFAULT_PORT = 4178
MAX_EVENT_BYTES = 64 * 1024
EVENT_LOCK = threading.Lock()


def profile_port(root):
    path = os.path.join(root, "docs", "agents", "profile.md")
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None
    m = re.search(r"^\s*Viewer port:\s*(\d+)", text, re.MULTILINE | re.IGNORECASE)
    return int(m.group(1)) if m else None


def list_files(root):
    out = []
    for name in ROOT_FILES:
        p = os.path.join(root, name)
        if os.path.isfile(p):
            out.append(name)
    docs = os.path.join(root, "docs")
    for dirpath, dirs, files in os.walk(docs):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for f in sorted(files):
            if f.endswith(".md"):
                out.append(os.path.relpath(os.path.join(dirpath, f), root).replace(os.sep, "/"))
    result = []
    for rel in out:
        try:
            mtime = os.path.getmtime(os.path.join(root, rel))
        except OSError:
            continue
        result.append({"path": rel, "mtime": mtime})
    return result


def safe_path(root, rel, exts):
    """Resolve rel inside root, or return None."""
    if not rel or "\x00" in rel:
        return None
    rel = rel.replace("\\", "/").lstrip("/")
    full = os.path.realpath(os.path.join(root, rel))
    if os.path.commonpath([full, root]) != root:
        return None
    parts = os.path.relpath(full, root).split(os.sep)
    if any(p in SKIP_DIRS for p in parts):
        return None
    if not full.lower().endswith(exts):
        return None
    if not os.path.isfile(full):
        return None
    return full


class Handler(BaseHTTPRequestHandler):
    server_version = "docs-viewer/1"

    def log_message(self, fmt, *args):
        if self.server.verbose:
            sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))

    def send(self, code, body, ctype="text/plain; charset=utf-8", extra=None):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, code, obj):
        self.send(code, json.dumps(obj), "application/json; charset=utf-8")

    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        q = urllib.parse.parse_qs(url.query)
        root = self.server.root
        if url.path == "/":
            self.send(200, PAGE, "text/html; charset=utf-8")
        elif url.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        elif url.path == "/api/files":
            self.send_json(200, {"root": os.path.basename(root), "files": list_files(root)})
        elif url.path == "/api/file":
            full = safe_path(root, q.get("path", [""])[0], (".md", ".html"))
            if not full:
                return self.send_json(404, {"error": "not found or not allowed"})
            with open(full, "rb") as fh:
                data = fh.read()
            self.send(200, data, "text/plain; charset=utf-8",
                      {"X-Mtime": str(os.path.getmtime(full))})
        elif url.path == "/mockup":
            full = safe_path(root, q.get("path", [""])[0], (".html",))
            if not full:
                return self.send(404, "not found or not allowed")
            with open(full, "rb") as fh:
                data = fh.read()
            self.send(200, data, "text/html; charset=utf-8",
                      {"Content-Security-Policy": "script-src 'none'; frame-ancestors 'self'"})
        else:
            self.send(404, "not found")

    def do_POST(self):
        url = urllib.parse.urlsplit(self.path)
        if url.path != "/api/event":
            return self.send(404, "not found")
        # Only accept same-origin posts from the page.
        origin = self.headers.get("Origin")
        host = self.headers.get("Host", "")
        if origin and urllib.parse.urlsplit(origin).netloc != host:
            return self.send_json(403, {"error": "cross-origin"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_EVENT_BYTES:
            return self.send_json(400, {"error": "bad length"})
        try:
            event = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return self.send_json(400, {"error": "bad json"})
        if not isinstance(event, dict) or event.get("type") not in ("choice", "comment"):
            return self.send_json(400, {"error": "type must be choice or comment"})
        allowed = ("type", "file", "block", "choice", "node", "text")
        record = {"ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        for k in allowed:
            if k in event and event[k] is not None:
                record[k] = str(event[k])[:4000]
        vdir = os.path.join(self.server.root, ".viewer")
        with EVENT_LOCK:
            os.makedirs(vdir, exist_ok=True)
            with open(os.path.join(vdir, "events.jsonl"), "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")
        self.send_json(200, {"ok": True, "event": record})


def main():
    ap = argparse.ArgumentParser(description="Local docs viewer with Mermaid and option cards.")
    ap.add_argument("--root", default=".", help="repo root (default: current directory)")
    ap.add_argument("--port", type=int, help=f"port (default: profile Viewer port or {DEFAULT_PORT})")
    ap.add_argument("--open", action="store_true", help="open in the default browser")
    ap.add_argument("--verbose", action="store_true", help="log requests")
    opts = ap.parse_args()

    root = os.path.realpath(opts.root)
    port = opts.port or profile_port(root) or DEFAULT_PORT
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.root = root
    server.verbose = opts.verbose
    url = f"http://127.0.0.1:{port}/"
    print(f"docs viewer: {url}  (root {root}; events in .viewer/events.jsonl; Ctrl-C to stop)", flush=True)
    if opts.open:
        threading.Timer(0.3, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Docs viewer</title>
<style>
:root {
  --bg: #fbfbfa; --panel: #f1f0ed; --ink: #1d1d1b; --muted: #6b6a66;
  --line: #dcdad4; --accent: #1168bd; --accent-ink: #fff; --card: #fff;
  --code: #f3f2ef; --toast: #1d1d1b; --toast-ink: #fff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #17181a; --panel: #1f2023; --ink: #e7e6e3; --muted: #9a9893;
    --line: #34353a; --accent: #5aa2e8; --accent-ink: #0d1117; --card: #222327;
    --code: #2a2b2f; --toast: #e7e6e3; --toast-ink: #17181a;
  }
}
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; background: var(--bg); color: var(--ink);
  font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif; }
#app { display: grid; grid-template-columns: 280px 1fr; height: 100vh; }
#app.with-frame { grid-template-columns: 280px 1fr 44%; }
nav { background: var(--panel); border-right: 1px solid var(--line); overflow: auto; padding: 16px 0; }
nav h1 { font-size: 13px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted);
  margin: 0 16px 12px; }
nav .group { font-size: 12px; color: var(--muted); margin: 14px 16px 4px; }
nav a { display: block; padding: 4px 16px 4px 20px; color: var(--ink); text-decoration: none;
  font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
nav a:hover { background: var(--line); }
nav a.active { background: var(--accent); color: var(--accent-ink); }
main { overflow: auto; padding: 32px 48px 96px; }
article { max-width: 860px; margin: 0 auto; }
article h1, article h2, article h3 { line-height: 1.25; }
article h1 { font-size: 30px; margin-top: 0; }
article h2 { margin-top: 2em; padding-bottom: 4px; border-bottom: 1px solid var(--line); }
article a { color: var(--accent); }
article code { background: var(--code); padding: 1px 5px; border-radius: 4px; font-size: .9em; }
article pre { background: var(--code); padding: 14px 16px; border-radius: 8px; overflow: auto; }
article pre code { background: none; padding: 0; }
article table { border-collapse: collapse; width: 100%; font-size: 14px; margin: 1em 0; }
article th, article td { border: 1px solid var(--line); padding: 6px 10px; text-align: left; vertical-align: top; }
article th { background: var(--panel); }
article blockquote { margin: 1em 0; padding: 4px 16px; border-left: 4px solid var(--line); color: var(--muted); }
.crumb { color: var(--muted); font-size: 13px; margin-bottom: 16px; font-family: ui-monospace, monospace; }
.mermaid { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 16px;
  margin: 1em 0; overflow: auto; text-align: center; }
.mermaid svg { max-width: 100%; height: auto; }
.mermaid g.node { cursor: pointer; }
.mermaid g.node:hover { filter: drop-shadow(0 0 4px var(--accent)); }
.merr { color: #c62828; white-space: pre-wrap; font-family: ui-monospace, monospace; font-size: 13px; text-align: left; }
.options { border: 1px dashed var(--accent); border-radius: 10px; padding: 12px; margin: 1.5em 0; }
.options > .label { font-size: 12px; text-transform: uppercase; letter-spacing: .06em; color: var(--accent); margin: 0 4px 8px; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 12px 16px;
  display: flex; flex-direction: column; }
.card h3 { margin: 4px 0 8px; font-size: 17px; }
.card .body { flex: 1; }
.card.chosen { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent); }
button { font: inherit; font-size: 14px; border-radius: 6px; padding: 6px 14px; cursor: pointer;
  border: 1px solid var(--accent); background: var(--accent); color: var(--accent-ink); }
button.ghost { background: transparent; color: var(--ink); border-color: var(--line); }
#frame { border-left: 1px solid var(--line); display: none; flex-direction: column; background: var(--panel); }
#app.with-frame #frame { display: flex; }
#frame header { display: flex; align-items: center; gap: 8px; padding: 8px 12px; border-bottom: 1px solid var(--line);
  font-size: 13px; font-family: ui-monospace, monospace; }
#frame header span { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
#frame iframe { flex: 1; border: 0; background: #fff; }
#comment { position: fixed; z-index: 10; display: none; width: 320px; background: var(--card);
  border: 1px solid var(--line); border-radius: 8px; padding: 12px; box-shadow: 0 8px 24px rgba(0,0,0,.2); }
#comment .node { font-weight: 600; margin-bottom: 6px; font-size: 14px; }
#comment textarea { width: 100%; min-height: 80px; font: inherit; font-size: 14px; color: var(--ink);
  background: var(--bg); border: 1px solid var(--line); border-radius: 6px; padding: 6px; }
#comment .row { display: flex; justify-content: flex-end; gap: 8px; margin-top: 8px; }
#toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%) translateY(20px); opacity: 0;
  background: var(--toast); color: var(--toast-ink); padding: 8px 16px; border-radius: 6px; font-size: 14px;
  transition: all .2s; pointer-events: none; }
#toast.show { opacity: 1; transform: translateX(-50%); }
.empty { color: var(--muted); margin-top: 20vh; text-align: center; }
@media (max-width: 820px) {
  #app, #app.with-frame { grid-template-columns: 1fr; grid-template-rows: auto 1fr; }
  nav { max-height: 30vh; border-right: 0; border-bottom: 1px solid var(--line); }
  main { padding: 20px 16px 80px; }
  #frame { position: fixed; inset: 10vh 0 0 0; }
}
</style>
</head>
<body>
<div id="app">
  <nav><h1 id="rootname">Docs</h1><div id="files"></div></nav>
  <main><article id="doc"><p class="empty">Pick a document.</p></article></main>
  <aside id="frame"><header><span id="framepath"></span><button class="ghost" id="frameclose">Close</button></header>
    <iframe id="frameview" sandbox="allow-same-origin"></iframe></aside>
</div>
<div id="comment"><div class="node"></div><textarea placeholder="What is wrong here?"></textarea>
  <div class="row"><button class="ghost" data-act="cancel">Cancel</button><button data-act="send">Comment</button></div></div>
<div id="toast"></div>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
mermaid.initialize({ startOnLoad: false, securityLevel: "loose", theme: "default" });

const $ = (s, el = document) => el.querySelector(s);
const state = { files: [], current: null, mtime: 0, chosen: {} };
let renderSeq = 0;

function toast(msg) {
  const t = $("#toast"); t.textContent = msg; t.classList.add("show");
  clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("show"), 1800);
}

async function postEvent(ev) {
  const r = await fetch("/api/event", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(ev) });
  if (r.ok) toast(ev.type === "choice" ? `Recorded: ${ev.choice}` : `Comment recorded on ${ev.node}`);
  else toast("Could not record event");
}

function dirname(p) { const i = p.lastIndexOf("/"); return i < 0 ? "" : p.slice(0, i); }
function resolve(base, rel) {
  const parts = (dirname(base) ? dirname(base).split("/") : []);
  for (const seg of rel.split("/")) {
    if (seg === "" || seg === ".") continue;
    if (seg === "..") parts.pop(); else parts.push(seg);
  }
  return parts.join("/");
}

function renderNav() {
  const box = $("#files"); box.innerHTML = "";
  let group = null;
  for (const f of state.files) {
    const g = f.path.includes("/") ? dirname(f.path) : "root";
    if (g !== group) { group = g; const d = document.createElement("div"); d.className = "group"; d.textContent = g; box.appendChild(d); }
    const a = document.createElement("a");
    a.href = "#" + encodeURIComponent(f.path); a.textContent = f.path.split("/").pop(); a.title = f.path;
    if (f.path === state.current) a.className = "active";
    box.appendChild(a);
  }
}

async function loadFiles() {
  try {
    const r = await fetch("/api/files"); const data = await r.json();
    $("#rootname").textContent = data.root || "Docs";
    const before = JSON.stringify(state.files.map(f => f.path));
    state.files = data.files;
    if (JSON.stringify(state.files.map(f => f.path)) !== before) renderNav();
    const cur = state.files.find(f => f.path === state.current);
    if (cur && cur.mtime !== state.mtime) await openFile(state.current, true);
  } catch (e) { /* server gone; keep polling */ }
}

// Split markdown into plain segments and options blocks.
const OPT_RE = /<!--\s*options:\s*([\w.-]+)\s*-->([\s\S]*?)<!--\s*\/options\s*-->/g;

function mdToHtml(md) {
  return marked.parse(md, { gfm: true });
}

function buildOptions(id, inner, file) {
  const wrap = document.createElement("section"); wrap.className = "options";
  wrap.innerHTML = `<div class="label">Options: ${id}</div><div class="cards"></div>`;
  const cards = $(".cards", wrap);
  const parts = inner.split(/^(?=###\s+Option\b)/m).filter(s => /^###\s+Option\b/.test(s.trim()) ? true : s.trim() !== "");
  for (const part of parts) {
    const m = part.trim().match(/^###\s+(.+)\n?([\s\S]*)$/);
    if (!m) { const d = document.createElement("div"); d.innerHTML = mdToHtml(part); wrap.insertBefore(d, cards); continue; }
    const title = m[1].trim();
    const card = document.createElement("div"); card.className = "card";
    if (state.chosen[file + "#" + id] === title) card.classList.add("chosen");
    card.innerHTML = `<h3></h3><div class="body">${mdToHtml(m[2])}</div><div><button>Choose</button></div>`;
    $("h3", card).textContent = title;
    $("button", card).onclick = async () => {
      await postEvent({ type: "choice", file, block: id, choice: title });
      state.chosen[file + "#" + id] = title;
      cards.querySelectorAll(".card").forEach(c => c.classList.remove("chosen"));
      card.classList.add("chosen");
    };
    cards.appendChild(card);
  }
  return wrap;
}

async function openFile(path, keepScroll) {
  const seq = ++renderSeq;
  const r = await fetch("/api/file?path=" + encodeURIComponent(path));
  if (!r.ok) { $("#doc").innerHTML = `<p class="empty">Cannot open ${path}</p>`; return; }
  const md = await r.text();
  if (seq !== renderSeq) return;
  const main = $("main"); const scroll = main.scrollTop;
  state.current = path; state.mtime = parseFloat(r.headers.get("X-Mtime")) || 0;
  const doc = $("#doc"); const frag = document.createElement("div");
  const crumb = document.createElement("div"); crumb.className = "crumb"; crumb.textContent = path; frag.appendChild(crumb);
  let last = 0; let m; OPT_RE.lastIndex = 0;
  while ((m = OPT_RE.exec(md))) {
    const d = document.createElement("div"); d.innerHTML = mdToHtml(md.slice(last, m.index)); frag.appendChild(d);
    frag.appendChild(buildOptions(m[1], m[2], path));
    last = OPT_RE.lastIndex;
  }
  const tail = document.createElement("div"); tail.innerHTML = mdToHtml(md.slice(last)); frag.appendChild(tail);
  // Mermaid code blocks become diagram divs.
  frag.querySelectorAll("pre > code.language-mermaid").forEach(code => {
    const div = document.createElement("div"); div.className = "mermaid-src mermaid"; div.dataset.src = code.textContent;
    code.parentElement.replaceWith(div);
  });
  // Links: .md navigates in-app, mockups open in the frame.
  frag.querySelectorAll("a[href]").forEach(a => {
    const href = a.getAttribute("href");
    if (/^[a-z]+:|^\/\/|^#/i.test(href)) return;
    const [target] = href.split("#");
    const full = resolve(path, decodeURIComponent(target));
    if (/\.md$/i.test(target)) { a.href = "#" + encodeURIComponent(full); }
    else if (/\.html?$/i.test(target)) {
      a.href = "#"; a.onclick = e => { e.preventDefault(); openFrame(full); };
    }
  });
  doc.replaceChildren(...frag.childNodes);
  renderNav();
  await renderMermaid(doc, path, seq);
  if (keepScroll) main.scrollTop = scroll; else main.scrollTop = 0;
}

async function renderMermaid(doc, path, seq) {
  let i = 0;
  for (const div of doc.querySelectorAll(".mermaid-src")) {
    const src = div.dataset.src; const id = `m${seq}_${i++}`;
    try {
      const { svg, bindFunctions } = await mermaid.render(id, src);
      if (seq !== renderSeq) return;
      div.innerHTML = svg; if (bindFunctions) bindFunctions(div);
      wireDiagram(div, path);
    } catch (e) {
      document.getElementById("d" + id)?.remove();
      div.innerHTML = `<div class="merr"></div>`; $(".merr", div).textContent = "Mermaid error:\n" + (e.message || e);
    }
  }
}

function nodeText(g) {
  const t = (g.querySelector(".nodeLabel, foreignObject, text") || g).textContent || "";
  return t.replace(/\s+/g, " ").trim() || g.id;
}

function wireDiagram(div, path) {
  // Mockup links from `click node "mockups/x.html"` open in the frame.
  div.querySelectorAll("a").forEach(a => {
    const href = a.getAttribute("href") || a.getAttribute("xlink:href") || "";
    if (/\.html?$/i.test(href) && !/^[a-z]+:/i.test(href)) {
      a.addEventListener("click", e => { e.preventDefault(); e.stopPropagation(); openFrame(resolve(path, href)); });
    }
  });
  div.querySelectorAll("g.node").forEach(g => {
    if (g.closest("a")) return;
    g.addEventListener("click", e => { e.stopPropagation(); openComment(e, path, nodeText(g)); });
  });
}

function openComment(e, file, node) {
  const box = $("#comment"); $(".node", box).textContent = node;
  const ta = $("textarea", box); ta.value = "";
  box.style.display = "block";
  const x = Math.min(e.clientX + 8, window.innerWidth - 336), y = Math.min(e.clientY + 8, window.innerHeight - 180);
  box.style.left = Math.max(8, x) + "px"; box.style.top = Math.max(8, y) + "px";
  ta.focus();
  box.onclick = async ev => {
    const act = ev.target.dataset && ev.target.dataset.act;
    if (act === "cancel") box.style.display = "none";
    if (act === "send" && ta.value.trim()) {
      await postEvent({ type: "comment", file, node, text: ta.value.trim() });
      box.style.display = "none";
    }
  };
}
document.addEventListener("click", e => { if (!e.target.closest("#comment")) $("#comment").style.display = "none"; });
document.addEventListener("keydown", e => { if (e.key === "Escape") { $("#comment").style.display = "none"; } });

function openFrame(path) {
  $("#app").classList.add("with-frame");
  $("#framepath").textContent = path;
  $("#frameview").src = "/mockup?path=" + encodeURIComponent(path);
}
$("#frameclose").onclick = () => { $("#app").classList.remove("with-frame"); $("#frameview").src = "about:blank"; };

function route() {
  const p = decodeURIComponent(location.hash.slice(1));
  if (p && p !== state.current) openFile(p, false);
}
window.addEventListener("hashchange", route);

await loadFiles();
if (!location.hash) {
  const first = state.files.find(f => f.path === "CONTEXT.md") || state.files.find(f => f.path.startsWith("docs/")) || state.files[0];
  if (first) location.hash = encodeURIComponent(first.path);
} else route();
setInterval(loadFiles, 1000);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
