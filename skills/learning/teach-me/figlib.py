#!/usr/bin/env python3
"""figlib: helpers for the inline-SVG figures of a chapter.

Import from a per-lesson figsN.py:

    from figlib import *
    def fig_1():
        sh, lb, nodes = tree(5, 100, 660, 200, names=NAMES, cls=lambda lo, hi: "oktint" if hi <= 3 else "")
        return fig(760, 300, "aria text", sh, lb + T(380, 288, "caption inside the picture", "hand mid"),
                   "The figcaption sentence.")
    FIGS = {"FIG_1": fig_1(), ...}

Trees are laid out from the RFC 6962 split rule (largest power of two strictly
less than n), so a drawn tree always matches the algorithm. Change `split` if
the structure being drawn splits differently.
"""
import pathlib
import subprocess

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def split(n):
    k = 1
    while k << 1 < n:
        k <<= 1
    return k


def layout(n, x0, x1, ybase, dy):
    """Node coordinates keyed by leaf range (lo, hi): (x, y, height)."""
    xs = [x0 + (x1 - x0) * (i + 0.5) / n for i in range(n)]
    nodes = {}

    def rec(lo, hi):
        if hi - lo == 1:
            nodes[(lo, hi)] = (xs[lo], ybase, 0)
            return 0
        k = split(hi - lo)
        h = max(rec(lo, lo + k), rec(lo + k, hi)) + 1
        nodes[(lo, hi)] = ((xs[lo] + xs[hi - 1]) / 2, ybase - h * dy, h)
        return h

    rec(0, n)
    return nodes


def default_label(n):
    def lab(lo, hi):
        if hi - lo == 1:
            return f"h{lo}"
        if lo == 0 and hi == n:
            return f"root{n}"
        if hi - lo <= 3:
            return "h" + "".join(str(i) for i in range(lo, hi))
        return f"root{hi - lo}" if lo == 0 else f"h{lo}..{hi - 1}"
    return lab


def tree(n, x0, x1, ybase, dy=48, label=None, cls=None, names=None, bw=54, bh=20, skip=None):
    """Return (shapes, labels, nodes). cls(lo, hi) -> extra rect classes
    ("dash acc", "oktint", "tint acc thick"...). names: leaf captions or None.
    skip: set of leaf ranges to leave undrawn (e.g. leaves the verifier never sees)."""
    label = label or default_label(n)
    cls = cls or (lambda lo, hi: "")
    skip = skip or set()
    nodes = layout(n, x0, x1, ybase, dy)
    shapes, labels = [], []
    for (lo, hi), (x, y, h) in nodes.items():
        if hi - lo == 1 or (lo, hi) in skip:
            continue
        k = split(hi - lo)
        for c in ((lo, lo + k), (lo + k, hi)):
            if c in skip:
                continue
            cx, cy, _ = nodes[c]
            shapes.append(f'<path class="thin" d="M{x:.0f} {y + bh / 2:.0f} L{cx:.0f} {cy - bh / 2:.0f}"/>')
    for (lo, hi), (x, y, h) in nodes.items():
        if (lo, hi) in skip:
            continue
        extra = cls(lo, hi)
        classes = " ".join(c for c in (("paper" if "tint" not in extra else ""), extra) if c)
        shapes.append(f'<rect class="{classes}" x="{x - bw / 2:.0f}" y="{y - bh / 2:.0f}" width="{bw}" height="{bh}" rx="5"/>')
        labels.append(f'<text class="sm mid" x="{x:.0f}" y="{y + 4:.0f}">{label(lo, hi)}</text>')
        if names and hi - lo == 1 and names[lo]:
            labels.append(f'<text class="sm mid t-muted" x="{x:.0f}" y="{ybase + bh / 2 + 14:.0f}">{names[lo]}</text>')
    return "\n".join(shapes), "\n".join(labels), nodes


def fig(w, h, aria, shapes, labels, caption):
    return f'''  <figure class="fig">
    <svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">
      <g class="ink sketch">
{shapes}
      </g>
      <g class="lbl">
{labels}
      </g>
    </svg>
    <figcaption>{caption}</figcaption>
  </figure>'''


def T(x, y, s, c=""):
    """Text. c: space-separated classes, e.g. "sm mid t-acc", "hand end"."""
    c = f' class="{c}"' if c else ""
    return f'<text{c} x="{x:.0f}" y="{y:.0f}">{s}</text>'


def R(x, y, w, h, c="paper", rx=6):
    """Rounded rect."""
    return f'<rect class="{c}" x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" rx="{rx}"/>'


def A(x1, y1, x2, y2, c="", m="arr"):
    """Straight arrow; m in arr, arr-acc, arr-ok, arr-bad."""
    c = f' class="{c}"' if c else ""
    return f'<path{c} d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" marker-end="url(#{m})"/>'


def harness(figs, out_dir, css_url, per_page=3):
    """Write shots/figs_K.html pages, each holding per_page figures, styled by the
    workspace assets at css_url (a file:// URL ending in /)."""
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    keys = list(figs)
    pages = []
    for p in range(0, len(keys), per_page):
        body = "\n".join(figs[k] for k in keys[p:p + per_page])
        html = (f'<!DOCTYPE html><html><head><meta charset="utf-8">'
                f'<link rel="stylesheet" href="{css_url}style.css"><link rel="stylesheet" href="{css_url}figures.css">'
                f'</head><body><main><p class="lesson-kicker">figs {p + 1}–{min(p + per_page, len(keys))}</p>\n{body}\n</main>'
                f'<script src="{css_url}figures.js"></script></body></html>')
        path = out / f"figs_{p // per_page + 1}.html"
        path.write_text(html)
        pages.append(path)
    return pages


def render(html_path, png_path, size=(900, 1500), chrome=CHROME):
    """Screenshot a local HTML file with headless Chrome."""
    url = "file://" + str(pathlib.Path(html_path).resolve())
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={size[0]},{size[1]}", f"--screenshot={png_path}", url],
                   check=True, capture_output=True)
    return png_path


def slices(doc, css_url, out_dir, cuts):
    """Cut a built lesson into section pages for review. cuts: {name: (start_marker, end_marker)}
    where markers are substrings of the document inside <main>."""
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    body = doc[doc.index("<main>"):doc.index("</main>") + 7]
    pages = []
    for name, (a, b) in cuts.items():
        part = body[body.index(a):body.index(b)]
        if not part.startswith("<main>"):
            part = "<main>" + part
        if not part.endswith("</main>"):
            part += "</main>"
        html = (f'<!DOCTYPE html><html><head><meta charset="utf-8">'
                f'<link rel="stylesheet" href="{css_url}style.css"><link rel="stylesheet" href="{css_url}figures.css">'
                f'</head><body>{part}<script src="{css_url}figures.js"></script></body></html>')
        path = out / f"sec_{name}.html"
        path.write_text(html)
        pages.append(path)
    return pages
