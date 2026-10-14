---
name: prototype
description: >-
  Build throwaway code that answers a "how should it look or behave" question
  by giving the human something to click and react to: a pure logic module
  behind a page of guided scenarios (LOGIC), radically different screen
  variants behind ?variant= with a floating switcher (UI), or a click-through
  simulator of a sequence across participants with failure injection (FLOW).
  Every prototype states its question at the top, carries a tradeoff drawer
  and a feedback bar, and ends with the decision redrawn as Mermaid. Use when
  the user says "prototype this," "show me," "stop asking, show me," "let me
  click it," "what would it look like," "mock up the flow," or when a mode
  or skill hits a question words cannot settle.
argument-hint: "The question to settle, e.g. 'can a refund happen while the parcel is in transit?' or 'which layout for invoice reminders?'"
---

# Prototype

A prototype is throwaway code that answers one question about how something
should look or behave, by putting a thing in front of the human to react to.
It is the opposite of a spec: nobody reads it, people poke it, and the
interesting moment is "wait, that should not be possible" or "I want the header
from B with the list from C." Those are bugs in the idea, found for the price
of an hour.

Callers: `trailblazer` (prototype nodes, the purple ones on the map),
`interview` (when the human says "show me"), `light`, `solution-design`, and
`pairing`. The human can also call it directly.

`<skill-dir>` below is the folder this `SKILL.md` was loaded from. The viewer
lives in the `visualize` skill's `scripts/docs_viewer.py`.

## When

- The question is a judgement made by looking or clicking: which layout, does
  this state model feel right, what happens to the order when the webhook
  arrives twice.
- Mid-conversation, when words are getting fuzzy: the second round of "it
  depends," two people using the same word for different things, or the human
  says "stop asking, show me." React, do not spec. Build the smallest thing
  that makes the disagreement visible and hand it over.
- A picture in Mermaid is not enough because the answer depends on sequence,
  state, or feel (density, scanning, what is on screen at once).

## When not

| The question is really | Go to |
|---|---|
| A fact someone already wrote down (API limits, library behaviour) | `research` |
| Can it work, here, at our scale | `spike` |
| A choice that needs no artifact, only a clear question | `interview` |
| Where things sit on one screen, no behaviour | a mockup (`visualize`, MOCKUPS.md) |

If you cannot name what the human will decide after clicking, it is not a
prototype yet. Ask that first.

## 1. State the question

Write it in one or two sentences before any code, in the domain's words:
"Should a refund be allowed while the parcel is in transit, and can partial
refunds add up to more than was paid?" It goes at the top of the prototype,
visible, not in a comment. Also write what decides it: "the human picks a
variant" or "the human runs the four scenarios and says which rule is wrong."
A prototype that answers the wrong question is pure waste, and a visible
question is the only way someone returning later can tell.

## 2. Pick a branch

| Branch | One-line test | Reference | Template |
|---|---|---|---|
| LOGIC | "Does this state model or rule set feel right?" Press buttons, watch state | [LOGIC.md](LOGIC.md) | `assets/logic-template.html` |
| UI | "What should this screen look like?" Flip between layouts | [UI.md](UI.md) | `assets/ui-variants-template.html`, or in-app with `assets/switcher-snippet.md` |
| FLOW | "What happens across these parties, and when it fails?" Step through messages | [FLOW.md](FLOW.md) | `assets/flow-template.html` |

The branches produce very different artifacts, so pick deliberately. A
backend module or a set of rules is LOGIC; a page or component is UI; anything
with two or more participants exchanging messages (auth, webhooks, payments,
agents handing off work) is FLOW. If it is genuinely ambiguous and the human
is away, pick the one that matches the surrounding code and say so in the
question line.

## 3. Shared rules

1. **Throwaway and marked.** The "PROTOTYPE, throwaway" badge stays visible.
   Names say prototype. Nothing imports it.
2. **Trivial to run.** One HTML file that opens by double-click, or an app
   route that the existing dev command already serves. No install step.
3. **In-memory state.** No database, no network, no persistence, unless
   persistence is the very thing being asked about (then a scratch file named
   so nobody mistakes it).
4. **No polish, no tests.** Error handling only where it keeps the thing
   running. No abstractions, no "what if we later." One question.
5. **Surface the state.** After every click or variant switch, the full
   relevant state is on screen as labelled fields, with what just changed
   marked. A hidden state is a prototype that cannot be argued with.
6. **Tradeoff drawer, always.** Every variant or scenario lists what it gains
   and what it gives up. Writing it forces you to know why each option exists.
7. **Feedback bar, always.** "Pick this" (or "Looks right") and "Add a note"
   on every prototype, so reactions arrive as data, not as a vague "B is nice."

## 4. Where it lives

- Inside a trail: `docs/research/<topic>/prototypes/<slug>.html`
- Inside planning: `docs/planning/<slug>/prototypes/<slug>.html`
- Neither: `docs/prototypes/<slug>.html`
- In-app UI variants: on the real route in the app, behind `?variant=`,
  committed on a `prototype/<slug>` branch that is never merged. Record the
  branch name in the node file or design doc.

The `prototypes/` folder name matters: the viewer only runs scripts for HTML
under a `prototypes/` directory.

## 5. Build it from the template

Copy the template to its path, then replace everything between the
`/* EDIT HERE */` markers. Keep the chrome (badge, drawer, feedback bar)
untouched. Every template ships with a worked example; delete it entirely,
do not leave half the old example behind. Use glossary terms for every label,
and realistic data ("Order 1042, £120.00"), never lorem ipsum.

Open it yourself before handing it over: click every scenario, switch every
variant, check it at phone width, and look at the browser console.

## 6. Hand it over

Through the viewer, so feedback lands as events:

```bash
python3 <visualize-dir>/scripts/docs_viewer.py --root . --port 4178
```

Then give the URL `http://127.0.0.1:<port>/prototype?path=<repo-relative path>`.
A link to the file from any markdown doc in the viewer also opens it in a new
tab. Without the viewer, the human double-clicks the file; the feedback bar
then copies a plain-text line to the clipboard for them to paste back.

Say in one line what to try first: "Run 'Refund while in transit' and tell me
if support would accept that refusal."

## 7. Read the feedback

Viewer feedback is a JSON line in `.viewer/events.jsonl`:

```json
{"ts": "2026-10-14T10:02:11Z", "type": "prototype", "file": "docs/research/refunds/prototypes/refund-rules.html", "choice": "transit: Refund while in transit", "about": "Shipped", "text": "support refunds lost parcels today, this rule breaks that"}
```

`choice` is the variant or scenario on screen, `about` the labelled part of the
page the human last clicked (optional), `text` the note, or `picked` for a
pick. Clipboard feedback is the same fields on one line:
`prototype | <file> | choice: ... | about: ... | text: ...`. Read, act on each
event, then truncate the file, as the `visualize` skill describes for the
viewer.

Change the prototype in response (add the scenario they asked for, merge B's
header into C) and hand it back. Prototypes evolve; two or three rounds is
normal.

## 8. Close the loop

The prototype settled something; now write it where decisions live.

1. **Capture the decision** in the trail node file or the design doc: the
   question, what was decided, and why, with the prototype linked. The human's
   pick is a decision (**user chose**), not evidence; anything the prototype
   showed by running ("a refund in transit was refused") is evidence of
   strength **ran it**.
2. **Redraw it as Mermaid** in that file, validated with the `visualize`
   checker:
   - LOGIC becomes a `stateDiagram-v2` (the template's "Copy as Mermaid").
   - FLOW becomes a `sequenceDiagram` of the scenario that matters (the
     template's "Copy as Mermaid", once per scenario worth keeping).
   - UI becomes a screen-flow `flowchart` naming the winning layout, linking
     the prototype file with `click`.
3. **Lift the validated module only through `tdd`.** A LOGIC module is a
   reference for the real one, not a paste: each behaviour it proved lands as
   a failing test first. UI winners are rewritten in the app's components.
4. **The HTML stays as the record.** It is never the spec. If the prototype
   and the Mermaid disagree later, the Mermaid wins and the prototype is
   history.

## Anti-patterns

- **No question.** "Let me build a quick demo" with nothing to decide.
- **Variants that differ in colour or copy.** Real variants disagree about
  structure.
- **Logic tangled with the page.** If the module touches the DOM it cannot be
  lifted.
- **Polish.** Animations, a component library, a design system. The human
  starts reviewing the paint.
- **Real backends.** Wiring a prototype to production data or real mutations.
- **Promoting the prototype.** Merging the `prototype/<slug>` branch or
  copying the HTML into the app. Rewrite properly.
- **Leaving the decision in the HTML.** If it is not redrawn in Mermaid in
  the node or design doc, it was not decided.
- **A prototype for a fact.** If reading a doc answers it, that was research.
