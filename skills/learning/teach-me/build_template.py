#!/usr/bin/env python3
"""build_000N.py — assemble lessons/000N-*.html from template parts, generated
figures, and code slices cut from the verified scratch module. Every value the
prose quotes is recomputed here and asserted. Copy, fill the TODOs, run."""
import html, re, sys, pathlib, hashlib, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import figsN as figs                                   # TODO: the lesson's figure module

S = pathlib.Path(__file__).parent
REPO = pathlib.Path("/abs/path/to/workspace")          # TODO
OUT = REPO / "lessons" / "000N-title.html"             # TODO
N = "N"                                                # TODO: template part prefix tpl_000N_

M = (S / "lN/main.go").read_text()                     # TODO: verified scratch code
run_out = "\n".join(l.rstrip() for l in (S / "run_output_N.txt").read_text().rstrip("\n").split("\n"))
old = (S / "old_000N.html").read_text()                # rewrite only; else old = ""


# ---------------------------------------------------------------- Go-aware slicer
def top_blocks(src: str):
    blocks, cur = [], []
    depth, in_raw = 0, False
    for line in src.split("\n"):
        if not in_raw and depth == 0 and line.strip() == "":
            if cur:
                blocks.append("\n".join(cur))
                cur = []
            continue
        cur.append(line)
        i, n = 0, len(line)
        while i < n:
            c = line[i]
            if in_raw:
                if c == "`":
                    in_raw = False
            elif c == "`":
                in_raw = True
            elif c == "/" and i + 1 < n and line[i + 1] == "/":
                break
            elif c == '"':
                i += 1
                while i < n and line[i] != '"':
                    if line[i] == "\\":
                        i += 1
                    i += 1
            elif c == "'":
                i += 1
                while i < n and line[i] != "'":
                    if line[i] == "\\":
                        i += 1
                    i += 1
            elif c in "({[":
                depth += 1
            elif c in ")}]":
                depth -= 1
            i += 1
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def slice_of(src: str, first: str, last: str | None = None) -> str:
    blocks = top_blocks(src)
    i = next(k for k, b in enumerate(blocks) if first in b)
    j = i if last is None else next(k for k, b in enumerate(blocks) if last in b)
    assert j >= i, (first, last)
    return "\n\n".join(blocks[i : j + 1])


def code(s: str) -> str:
    return html.escape(s, quote=False)


def pre_blocks(doc):
    return [html.unescape(p) for p in re.findall(r"<pre><code>(.*?)</code></pre>", doc, re.S)]


# ---------------------------------------------------------------- slices
slices = {
    # TODO: one entry per @@PLACEHOLDER@@ in the templates
    "C_MAIN": slice_of(M, "func main()"),
    "C_FULL": M.rstrip("\n"),
    "RUN_OUTPUT": "$ go run .\n" + run_out,
}
assert slices["C_MAIN"].startswith("func main()")
if old:
    old_pres = pre_blocks(old)
    assert slices["C_MAIN"] == next(p for p in old_pres if p.startswith("func main()"))
    # TODO: assert every other slice equals its old snippet, and run_out equals the old expected output

# ---------------------------------------------------------------- recompute every quoted value
def leaf(d): return hashlib.sha256(b"\x00" + d).digest()
def node(l, r): return hashlib.sha256(b"\x01" + l + r).digest()
sh = lambda d: d.hex()[:12]
H = figs.H                                             # the figure module's value table
# TODO: recompute each entry of H and every list/length/edge case the prose quotes, and assert.

# ---------------------------------------------------------------- quiz
if old:
    quiz = re.search(r"<script>\n(renderQuiz\(.*?\]\);)\n</script>", old, re.S).group(1)
else:
    quiz = (S / f"quiz_{N}.js").read_text().strip()   # written per SKILL.md's Quiz rules
assert quiz.count("q:") >= 3

# ---------------------------------------------------------------- assemble
tpl = "".join((S / f"tpl_000{N}_{p}.html").read_text() for p in "abcd")
for k, v in slices.items():
    tpl = tpl.replace(f"@@{k}@@", code(v))
for k, v in figs.FIGS.items():
    tpl = tpl.replace(f"@@{k}@@", v)
tpl = tpl.replace("@@QUIZ@@", quiz)
left = re.findall(r"@@[A-Z_0-9]+@@", tpl)
assert not left, left

# links: every old link survives; every relative link resolves
for href in set(re.findall(r'href="([^"]+)"', old)):
    assert href in tpl, href
for href in set(re.findall(r'href="([^"]+)"', tpl)):
    if href.startswith("http"):
        continue
    assert (OUT.parent / href).exists(), href

# tag balance
for tag in ["p", "div", "figure", "figcaption", "svg", "g", "table", "tr", "td", "th", "pre", "code", "details",
            "summary", "ol", "ul", "li", "aside", "blockquote", "h1", "h2", "h3", "main", "script", "text", "span",
            "a", "strong", "em"]:
    opens = len(re.findall(rf"<{tag}[\s>]", tpl))
    closes = len(re.findall(rf"</{tag}>", tpl))
    assert opens == closes, (tag, opens, closes)

# every hash value in the prose is one we computed
known = set(H.values())
for hx in set(re.findall(r"\b[0-9a-f]{12}\b", re.sub(r"<pre><code>.*?</code></pre>", "", tpl, flags=re.S))):
    assert hx in known, hx

OUT.write_text(tpl)
print(f"wrote {OUT} ({len(tpl):,} bytes, {tpl.count('<figure')} figures, "
      f"{tpl.count('class=\"code-loc\"')} code slices, {tpl.count('<aside')} asides, "
      f"{tpl.count('<h2')} h2, {tpl.count('<h3')} h3)")
