---
name: slides
description: >-
  Build a lecture deck as one HTML page: a 16:9 canvas per slide (the picture)
  above a transcript (what a warm, precise lecturer would say), with diagrams
  and lists revealed one step at a time, keyboard navigation, and a handout
  view for printing. A checker lays the deck out in headless Chrome, flags
  overflow, crowded canvases, step gaps and overlapping labels, and
  screenshots every step for you to look at. Use when a teaching skill
  (professor) needs a lecture, or when the user says "make slides," "turn this
  into a lecture," "a deck that explains X," or "walk me through this visually."
argument-hint: "What the lecture explains, and where the deck should go."
---

# Slides

A lecture is pictures and talk arriving together, one small piece at a time.
Mayer's multimedia principles say why that shape works: words and pictures
beat words alone, corresponding words and pictures belong together on the
screen, learner-paced segments beat one continuous stream, extraneous material
hurts, and a conversational voice helps ([Mayer 2020](https://ugc.futurelearn.com/uploads/files/7d/d6/7dd6188d-c343-4311-b064-ac98d2c95abc/Multimedia_Principles._R._E._Mayer__2020.pdf)).
A deck built here has a canvas that carries the picture and almost no prose,
a transcript that carries the explanation, and steps that bring the two in
together.

`<skill-dir>` is the folder this `SKILL.md` was loaded from.

- [DECK-FORMAT.md](DECK-FORMAT.md): the HTML contract, every slide kind, steps,
  figures, and the canvas word budget.
- `assets/deck.css`, `assets/deck.js`: the runtime. Seed them into the
  workspace's `assets/` once; every deck links them.
- `assets/deck-template.html`: a worked ten-slide lecture showing every slide
  kind. Copy it and replace the slides.
- `scripts/render_deck.py`: the checker and screenshotter.

## Steps

1. **Have the content first.** A deck is a rendering of a plan, not a way to
   find one. The caller hands over the lecture arc (for `professor`, the
   lesson plan): each slide's one idea, its picture, its transcript points, and
   where the learner is asked to predict. Without that, ask for it or write it
   to a scratch file before any HTML. Done when every slide has one idea that
   fits in a sentence.

2. **Seed the assets.** If the workspace's `assets/` lacks `deck.css` or
   `deck.js`, copy them from `<skill-dir>/assets/`. Done when the deck's
   relative links resolve.

3. **Write the deck** from `deck-template.html`, per DECK-FORMAT.md. Draw each
   diagram once, in its final form, then give its parts `data-step` numbers in
   the order the transcript introduces them. Every quoted number, code line,
   and source on a slide comes from the caller's verified material (the
   `fact-check` skill's values and snippets); a slide never introduces a fact
   of its own. Done when every slide has an id, a canvas, and a transcript
   paragraph per step.

4. **Check and look.**

   ```bash
   python3 <skill-dir>/scripts/render_deck.py lessons/NNNN-slug/lecture.html
   ```

   Fix every FAIL and re-run until it prints `Clean.` Then open the
   screenshots: every step of every slide that builds, the last step of the
   rest. Read each as the learner will. The checker finds collisions; you find
   a diagram that is correct but confusing, a reveal order that gives the
   answer away, a transcript paragraph that talks about something not yet on
   the canvas. Done when you have looked at every screenshot after the last
   fix.

5. **Hand back** the deck's path, its slide count, and which slides ask the
   learner to predict, so the caller can pause there in chat.

## Rules

- **One idea per slide.** If the title needs "and," it is two slides.
- **The canvas shows; the transcript tells.** At most about 30 words on a
  canvas (45 on a predict slide), not counting code, tables, and figure
  labels. Full sentences, citations, and caveats go in the transcript.
- **Build, don't dump.** A diagram with more than four parts arrives in steps,
  in the order the transcript explains them. The finished picture is the last
  step, never the first.
- **Words beside their picture.** A transcript paragraph is tied to the step
  that shows what it talks about. Never describe something the canvas has not
  revealed yet.
- **Signal, don't decorate.** Colour means the same thing on every slide:
  accent for the thing the slide is about, green for computed or correct, red
  for broken, dashed for not built yet. No clip art, no logos, no gradients.
- **Code is cut, not retyped.** Code on a slide is a slice of verified code.
  Eliding a body with `…` is fine; changing a line is not. Highlight with
  `data-hl`; never hide code the learner needs to read.
- **Predict slides stop the lecture.** The question is on the canvas, the
  answer is the last step, and the transcript asks the learner to commit before
  advancing.
- **Self-contained enough.** No network fonts or scripts are required; the deck
  opens from disk.
