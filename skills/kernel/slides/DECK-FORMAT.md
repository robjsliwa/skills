# Deck Format

One HTML file per lecture. `deck.js` turns it into a presentation; nothing
else is needed.

## Skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lesson 2 · One Phone, Many Views</title>
<link rel="stylesheet" href="../../assets/deck.css">
</head>
<body>
<div class="deck" data-title="Lesson 2 · One Phone, Many Views">

  <section class="slide" id="stale-flag">
    <div class="canvas">
      <h2>The easy way to build a screen</h2>
      <div class="fill"><svg viewBox="0 0 960 380">…</svg></div>
    </div>
    <aside class="transcript">
      <p>Shown at step 0, with the canvas's unstepped parts.</p>
      <p data-step="1">Shown when step 1 reveals its canvas parts.</p>
    </aside>
  </section>

</div>
<script src="../../assets/deck.js"></script>
</body>
</html>
```

Every slide is a direct child `section.slide` of `.deck`, with a unique `id`
(kebab-case, names the idea: `stale-flag`, not `slide-3`), one `.canvas`, and
one `aside.transcript`.

## Steps

- `data-step="k"` on a canvas element hides it until step `k`. The element
  revealed at the current step gets `.now` (SVG rects inside it take the accent
  stroke), so the eye goes to what just changed.
- `data-step="k"` on a transcript paragraph shows it from step `k`. Earlier
  paragraphs turn muted; the newest stays dark.
- `data-hl="k"` highlights at step `k` without ever hiding: use it for code
  lines and table rows the learner should be able to read all along.
- Steps run 1..n with no gaps. A slide with no steps is one step, 0.
- Navigation: → / space / click next, ← back, `t` hides the transcript, `h`
  toggles the handout (every slide fully built, for reading or printing), `f`
  fullscreen. `#/3/2` opens slide 3 at step 2.

## Slide kinds

The template has one of each.

| Kind | Class | Canvas | Use for |
|---|---|---|---|
| Title | `slide title` | `.kicker`, `h1`, `.promise` | the lesson's promise in one sentence |
| Picture | `slide` | `h2`, `.fill` with an SVG | activation, the hook, the model, a mechanism |
| List | `slide` | `h2`, `ul.points` with stepped `li` | the lab bridge, a short sequence |
| Table | `slide` | `h2`, `table` with stepped `tr` | a worked trace, revealed row by row |
| Code | `slide code` | `h2`, `pre` with `span.hl[data-hl]` groups | the code that makes the model real |
| Predict | `slide prompt` | `.question`, `.answer[data-step="1"]` | stop and commit before the reveal |
| Two columns | `slide` | `h2`, `.cols` with two children | before/after, analogy and where it breaks |
| Addendum | `slide addendum` | any | a slide added in office hours, marked as such |

`.big` is a one-line statement in large serif. `.source` is a small credit in
the canvas corner, used only when a quotation is on the canvas; otherwise
sources are links in the transcript.

## Figures

Inline SVG, `viewBox="0 0 960 H"` (H about 340–400), inside `.fill`. Shapes in
`<g class="ink sketch">`, text in a separate `<g>`. Classes (from `deck.css`):

- Shape fills: `tint` (accent), `oktint`, `badtint`, `soft`. Strokes: `acc`,
  `ok`, `bad`, `dash`, `thick`, `thin`.
- Text: `sm`, `big`, `mono`, `hand` (italic serif: the sentence the figure is
  making), `mid`, `end`, `t-acc`, `t-ok`, `t-bad`, `t-muted`.
- Arrows: `marker-end="url(#arr)"`, `#arr-acc`, `#arr-ok`, `#arr-bad`;
  `deck.js` defines them.
- Give every `svg` an `aria-label`: one sentence describing the finished
  picture.
- Group what one step reveals: `<g data-step="2">` around both the shapes and
  their labels (one group in each layer).
- Text width: 20px sans is about 10px per character, 17px mono about 10.2px.
  Check a label fits its box before rendering; the checker reports overlaps,
  not tight fits.

Meaning is fixed across the deck: accent is the thing the argument is about,
green is computed or correct, red is broken or stale, dashed is not built yet.

## Transcript voice

The transcript is what the lecturer says while the slide is up, written as
the `professor` skill's VOICE.md asks: complete sentences, second person,
plain words for why and code for how. Two to four short paragraphs per slide,
one per step. It may link primary sources inline. It never refers to anything
the canvas has not shown yet.

## The check

`render_deck.py` reports, per slide:

| Kind | Means |
|---|---|
| structure | missing id, canvas, or transcript; repeated id |
| overflow | canvas content or a code block is larger than its box |
| dense | too many words on the canvas |
| steps | a step number with nothing to reveal, or a transcript step with nothing on the canvas |
| label | SVG text overlapping other text, or running outside its figure or the canvas |

It also screenshots each step to `build/shots/sNN-kK.png` beside the deck.
