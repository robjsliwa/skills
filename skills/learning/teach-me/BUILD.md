# Build and Assert

The page is assembled by a per-lesson `build_000N.py` copied from [build_template.py](build_template.py). The script is the proof that the chapter tells the truth: the code shown is the code that ran, and every number in the prose was computed.

## Inputs

- `tpl_000N_{a,b,c,d}.html` — the template parts, prose with `@@NAME@@` slots.
- The scratch module the code ran in (`lN/main.go` or a scratch copy of the package), never the learner's own directory.
- Saved run output (`run_output_N.txt`, the stretch's too).
- `figsN.py` exporting `FIGS = {"FIG_1": "<figure…>", …}`.
- The old lesson (for a rewrite): the quiz is extracted verbatim from it.

## Slicing code

`top_blocks` splits Go source into top-level declarations at blank lines outside braces, parens, strings and raw strings, so a comment stays attached to its function and blank lines inside a body do not split it. `slice_of(src, first, last)` returns the blocks from the one containing `first` through the one containing `last`. Name each slice for the placeholder it fills and assert its shape (how many `func`s, what it starts with, what it must not contain). For a lesson in another language, replace `top_blocks` with a splitter for that language's top-level declarations; the assertions stay the same.

## Assertions, in order

1. Each slice has the expected shape, and on a rewrite equals the old lesson's snippet after `html.unescape`.
2. The saved run output equals the old lesson's expected output (rewrite) or matches the values script (new lesson).
3. Every value quoted in the prose is recomputed in Python and compared: hashes, proof lists, lengths, edge cases, the exhaustive small-size checks the asides and Challenges rely on.
4. The quiz has the expected number of questions and is inserted unescaped.
5. No `@@` placeholder remains.
6. Every `href` of the old lesson appears in the new one; every relative `href` of the new one resolves on disk.
7. Tag balance for `p div figure figcaption svg g table tr td th pre code details summary ol ul li aside blockquote h1 h2 h3 main script text span a strong em`.
8. Every 12-hex-character token in the prose (code blocks excluded) is in the set of values the script computed.

The script ends by writing the lesson and printing byte count, figures, code slices, asides, `h2`s and `h3`s.

## Render the page

```python
doc = OUT.read_text()
figlib.slices(doc, css_url, "shots", {"intro": ("<main>", "<h2>N.4"), "alg": ("<h2>N.4", "<h2>N.7"), "code": ("<h2>N.7", "<h2>N.8"), "end": ("<h2>N.8", "</main>")})
for name in ("intro", "alg", "code", "end"):
    figlib.render(f"shots/sec_{name}.html", f"shots/sec_{name}.png", size=(900, 6000))
```

Then confirm the live page: `chrome --headless=new --dump-dom <lesson.html>` should contain the quiz questions (`class="quiz-q"`), the four arrow markers and the `#sketch` filter. Compare the quiz block of the old and new files for byte identity on a rewrite.
