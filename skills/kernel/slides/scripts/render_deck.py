#!/usr/bin/env python3
"""Check a lecture deck and screenshot every slide at every step.

Usage:
  render_deck.py DECK.html [--out DIR] [--last] [--checks-only]
                 [--size 1280x1000] [--chrome PATH]
  render_deck.py --page PAGE.html [--out DIR]

--page screenshots an ordinary page (a lab, a reference sheet) instead of a
deck, in overlapping 900x1400 chunks from top to bottom, as
DIR/page-<name>-NN.png. No checks.

1. Static checks (no browser): every slide is a <section class="slide"> with a
   unique id, a .canvas and a non-empty .transcript; every relative href/src
   resolves on disk; data-step and data-hl values are integers.
2. Layout checks (headless Chrome): opens DECK.html?check, which makes deck.js
   lay the deck out and report canvas overflow, too many words on a canvas,
   gaps in the step sequence, transcript steps with nothing on the canvas, and
   SVG labels that overlap each other or run outside their figure.
3. Screenshots: DIR/sNN-kK.png for slide NN at step K (every step, or only the
   last with --last). Open them and look; the checks catch collisions, not
   ugliness or a wrong picture.

Finding Chrome: --chrome, then $CHROME, then Google Chrome or Chromium on the
system, then a Playwright install ($PLAYWRIGHT_BROWSERS_PATH,
~/.cache/ms-playwright, ~/Library/Caches/ms-playwright, /opt/pw-browsers).
Running as root adds --no-sandbox.

Exit codes: 0 clean, 1 problems found, 2 no browser (static checks still ran).
Python 3 standard library only.
"""

import argparse
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

MAC_CHROMES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]
PATH_CHROMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"]
PW_GLOBS = [
    "chromium-*/chrome-linux*/chrome",
    "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
    "chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
    "chromium-*/chrome-win*/chrome.exe",
]


def find_chrome(explicit=None):
    for c in [explicit, os.environ.get("CHROME")]:
        if c and Path(c).exists():
            return c
    for c in MAC_CHROMES:
        if Path(c).exists():
            return c
    for name in PATH_CHROMES:
        p = shutil.which(name)
        if p:
            return p
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH"), "~/.cache/ms-playwright",
             "~/Library/Caches/ms-playwright", "/opt/pw-browsers"]
    for root in roots:
        if not root:
            continue
        root = os.path.expanduser(root)
        for pattern in PW_GLOBS:
            hits = sorted(glob.glob(os.path.join(root, pattern)))
            if hits:
                return hits[-1]
    return None


class DeckParser(HTMLParser):
    """Collect slides, their parts, step values and relative links."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.slides = []          # dicts: id, canvas, transcript_text, steps
        self.links = []
        self.bad_steps = []
        self._stack = []          # tag names
        self._slide_depth = None
        self._transcript_depth = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if tag not in ("br", "img", "link", "meta", "input", "hr", "source", "path", "rect", "circle",
                       "line", "polyline", "polygon", "ellipse", "use", "stop"):
            self._stack.append(tag)
        if tag == "section" and "slide" in classes:
            self.slides.append({"id": a.get("id"), "canvas": False, "transcript": "", "steps": set()})
            self._slide_depth = len(self._stack)
        if self.slides and self._slide_depth:
            s = self.slides[-1]
            if "canvas" in classes:
                s["canvas"] = True
            if tag == "aside" and "transcript" in classes:
                self._transcript_depth = len(self._stack)
            for key in ("data-step", "data-hl"):
                if key in a:
                    if re.fullmatch(r"\d+", a[key] or ""):
                        s["steps"].add(int(a[key]))
                    else:
                        self.bad_steps.append((s["id"], key, a[key]))
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])

    def handle_endtag(self, tag):
        if tag in self._stack:
            while self._stack:
                t = self._stack.pop()
                if t == tag:
                    break
        if self._transcript_depth and len(self._stack) < self._transcript_depth:
            self._transcript_depth = None
        if self._slide_depth and len(self._stack) < self._slide_depth:
            self._slide_depth = None

    def handle_data(self, data):
        if self._transcript_depth and self.slides:
            self.slides[-1]["transcript"] += data


def static_checks(deck):
    p = DeckParser()
    p.feed(deck.read_text(encoding="utf-8"))
    problems = []
    if not p.slides:
        problems.append("no <section class=\"slide\"> found")
    seen = {}
    for i, s in enumerate(p.slides, 1):
        if not s["id"]:
            problems.append(f"slide {i}: no id")
        elif s["id"] in seen:
            problems.append(f"slide {i}: id '{s['id']}' repeats slide {seen[s['id']]}")
        else:
            seen[s["id"]] = i
        if not s["canvas"]:
            problems.append(f"slide {i}: no .canvas")
        if not s["transcript"].strip():
            problems.append(f"slide {i}: empty or missing .transcript")
    for sid, key, val in p.bad_steps:
        problems.append(f"slide '{sid}': {key}=\"{val}\" is not an integer")
    for link in p.links:
        u = urlparse(link)
        if u.scheme or link.startswith(("#", "//", "data:", "mailto:")):
            continue
        target = (deck.parent / u.path).resolve()
        if not target.exists():
            problems.append(f"link does not resolve: {link}")
    return p.slides, problems


def chrome_cmd(chrome, size):
    cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
           f"--window-size={size[0]},{size[1]}"]
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        cmd.append("--no-sandbox")
    return cmd


def layout_checks(chrome, deck, size):
    url = deck.resolve().as_uri() + "?check"
    out = subprocess.run(chrome_cmd(chrome, size) + ["--virtual-time-budget=4000", "--dump-dom", url],
                         capture_output=True, text=True, timeout=120)
    m = re.search(r'<pre id="deck-check"[^>]*>(.*?)</pre>', out.stdout, re.S)
    if not m:
        return None, ["layout check produced no report: is deck.js linked and loading?"]
    return json.loads(html.unescape(m.group(1))), []


def screenshots(chrome, deck, slides, out_dir, size, last_only):
    out_dir.mkdir(parents=True, exist_ok=True)
    shots = []
    base = deck.resolve().as_uri()
    failed = []
    for i, s in enumerate(slides, 1):
        top = max(s["steps"]) if s["steps"] else 0
        for k in ([top] if last_only else range(top + 1)):
            png = out_dir / f"s{i:02d}-k{k}.png"
            if shoot(chrome, size, f"{base}#/{i}/{k}", png):
                shots.append(png)
            else:
                failed.append(f"screenshot failed: slide {i} step {k}")
    return shots, failed


def shoot(chrome, size, url, png):
    try:
        subprocess.run(chrome_cmd(chrome, size) + ["--virtual-time-budget=1500", f"--screenshot={png}", url],
                       capture_output=True, timeout=120, check=True)
        return png.exists()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False


def page_shots(chrome, page, out_dir):
    """Screenshot a long page in overlapping 900x1400 chunks. Fragment scrolling
    does not repaint in headless screenshots, so a temporary copy beside the
    page (relative links still resolve) shifts the body up by chunk."""
    out_dir.mkdir(parents=True, exist_ok=True)
    step = 1300
    shift = ("<script>(function(){var k=+(new URLSearchParams(location.search).get('shot')||0);"
             "document.body.setAttribute('data-h',document.documentElement.scrollHeight);"
             f"document.body.style.transform='translateY(-'+(k*{step})+'px)';}})();</script>")
    text = page.read_text(encoding="utf-8")
    tmp = page.with_name(f".{page.stem}.shot.html")
    tmp.write_text(text.replace("</body>", shift + "</body>") if "</body>" in text else text + shift,
                   encoding="utf-8")
    shots, failed = [], []
    try:
        dom = subprocess.run(chrome_cmd(chrome, (900, 1400)) + ["--virtual-time-budget=1500", "--dump-dom",
                                                               tmp.resolve().as_uri()],
                             capture_output=True, text=True, timeout=120).stdout
        m = re.search(r'data-h="(\d+)"', dom)
        height = int(m.group(1)) if m else 1400
        for k in range(max(1, -(-(height - 100) // step))):
            png = out_dir / f"page-{page.stem}-{k + 1:02d}.png"
            (shots if shoot(chrome, (900, 1400), tmp.resolve().as_uri() + f"?shot={k}", png) else failed).append(png)
    finally:
        tmp.unlink(missing_ok=True)
    return shots, failed


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("deck", type=Path, nargs="?")
    ap.add_argument("--page", type=Path, help="screenshot an ordinary page in sections instead")
    ap.add_argument("--out", type=Path, default=None, help="screenshot folder (default: <deck dir>/build/shots)")
    ap.add_argument("--last", action="store_true", help="screenshot only the final step of each slide")
    ap.add_argument("--checks-only", action="store_true", help="no screenshots")
    ap.add_argument("--size", default="1280x1000")
    ap.add_argument("--chrome")
    opts = ap.parse_args()
    size = tuple(int(x) for x in opts.size.lower().split("x"))
    if opts.page:
        chrome = find_chrome(opts.chrome)
        if not chrome:
            print("No Chrome or Chromium found. Pass --chrome or set $CHROME.")
            return 2
        out = opts.out or opts.page.parent / "build" / "shots"
        shots, failed = page_shots(chrome, opts.page, out)
        for f in failed:
            print(f"  FAIL  screenshot failed: {f.name}")
        print(f"{len(shots)} screenshots in {out}/ — open every one and look.")
        return 1 if failed else 0
    deck = opts.deck
    if deck is None:
        ap.error("give a deck, or --page PAGE")
    if not deck.exists():
        print(f"no such file: {deck}")
        return 1

    slides, problems = static_checks(deck)
    print(f"{deck}: {len(slides)} slides, {sum((max(s['steps']) if s['steps'] else 0) + 1 for s in slides)} steps")

    chrome = find_chrome(opts.chrome)
    if not chrome:
        for p in problems:
            print(f"  FAIL  {p}")
        print("No Chrome or Chromium found; static checks only. Pass --chrome or set $CHROME.")
        return 2

    report, more = layout_checks(chrome, deck, size)
    problems += more
    if report:
        for it in report["issues"]:
            where = f"slide {it['slide']}" + (f" ({it['id']})" if it.get("id") else "")
            problems.append(f"{where}: {it['kind']}: {it['detail']}")

    for p in problems:
        print(f"  FAIL  {p}")
    if not opts.checks_only:
        out = opts.out or deck.parent / "build" / "shots"
        shots, failed = screenshots(chrome, deck, slides, out, size, opts.last)
        for f in failed:
            print(f"  FAIL  {f}")
        problems += failed
        print(f"{len(shots)} screenshots in {out}/ — open every one and look.")
    print("Clean." if not problems else f"{len(problems)} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
