---
name: visualize
description: >-
  Draw the picture that makes a question or decision clear, as a Mermaid block
  inside the markdown artifact it belongs to: C4 context, containers and
  components as flowcharts, journeys, screen flows linked to HTML mockups,
  sequences, states, data, option pairs, and before/after. Validates every
  block with mmdc, renders PNGs to look at, and runs a local viewer where the
  user picks options and comments on nodes. Use when the user says "draw it,"
  "show me," "diagram this," "wireframe," "open the viewer," or when another
  skill needs a picture, a show-then-ask turn, or an options block.
---

# Visualize

A picture earns its place when it answers a question faster than the prose
beside it. Draw it as Mermaid inside the file it explains, so GitHub renders
it, a PR diff shows it change, and nobody has to hunt for a separate drawing.
The rules here are the same whether the user asked for a diagram or another
skill (interview, story, solution-design) needs one.

`<skill-dir>` below is the folder this `SKILL.md` was loaded from (for example
`~/.claude/skills/visualize` or `.agents/skills/visualize`). Other skills that
point at "the `visualize` skill's `scripts/...`" mean the same folder.

## Settings

Read the `## Diagrams` section of `docs/agents/profile.md` if it exists:

- `Validate:` the mmdc command, or `off`. Default: `npx -y @mermaid-js/mermaid-cli`.
- `Viewer port:` default `4178`.

If the profile is missing, use the defaults and say once that `/repo-setup`
would make them explicit.

## 1. Decide whether to draw

Draw when the subject is structural: who talks to whom, what happens in what
order, what states something moves through, what the data is, which screens
follow which, which of two shapes to pick. Skip it when the answer is one
sentence, a list, or a table; a diagram of three boxes in a row is a sentence
wearing a costume.

## 2. Pick the diagram

Name the question first, then take the diagram and home artifact from the
table in [NOTATION.md](NOTATION.md). It has a worked example per row, the C4
levels, and which UML diagrams are worth drawing. C4 diagrams use the class
block and label convention in [C4-STYLE.md](C4-STYLE.md); paste the
`classDef` lines into every C4 diagram rather than inventing colors.

## 3. Draw it

- **One idea per diagram.** If the caption needs "and," it is two diagrams.
- **About 12 nodes, at most.** Past that, zoom out a C4 level or split by
  flow. A sequence diagram counts participants and keeps to about 12 messages.
- **Caption after the block.** One sentence that says what to look at: "The
  token never reaches the browser; follow the dashed arrow." Not a restatement
  of the title.
- **Labels are glossary terms.** Node labels come from `GLOSSARY.md`. When you
  need a label the glossary lacks, flag it in your reply: either the glossary
  is missing a term (hand it to `glossary`) or the design has a smell (a thing
  nobody can name is often a thing that should not exist).
- **Stable node ids.** Short, lowercase, meaningful (`checkout`, `ordersDb`),
  never `A`, `B`, `C`. Keep ids when you edit so the diff shows the one edge
  that changed, not a renumbered picture.
- **Quote labels** with `["..."]` whenever they hold spaces, punctuation, or
  `<br/>`. Edge labels go in `|"..."|`.

## 4. Validate and look

Run the checker on the file you touched:

```bash
python3 <skill-dir>/scripts/mermaid_check.py docs/planning/<slug>/design.md
```

It reports PASS or FAIL per block with `file:line` and the parser error, and
exits 1 on any failure. Fix every FAIL before showing the user anything.

Then look at it. Parsing is not the same as reading well:

```bash
python3 <skill-dir>/scripts/mermaid_check.py <file> --png <scratch-dir>
```

Open each PNG (with an image-reading tool when you have one) and check, in the
order problems usually appear:

1. Edges that cross for no reason. Reorder node declarations, switch `LR` and
   `TB`, or group with a `subgraph`.
2. Labels clipped or overlapping an edge. Shorten them or add `<br/>`.
3. A long thin strip. Change direction or split into two diagrams.
4. A node that floats with no edge: it is either missing a relationship or
   does not belong in this picture.
5. More than about 12 nodes once rendered. Split.

Done means you looked at the final render, not that the script ran.

**When mmdc is unavailable** (exit code 2: no Node, no network, no browser, or
`Validate: off`), say so plainly in your reply, still write the diagram, and
make `%% unvalidated` the first line inside the block. The next run that has
mmdc removes the marker once the block passes.

## 5. Options blocks, for choices

When the user has to pick between shapes, draw two or three small diagrams in
an options block. It is plain markdown, so it reads fine on GitHub and the
viewer renders it as cards with a Choose button:

````markdown
<!-- options: storage-shape -->
### Option A: one table per tenant
```mermaid
...
```
Tradeoff line: what you get, what it costs.

### Option B: shared table with tenant_id
```mermaid
...
```
Tradeoff line.
<!-- /options -->
````

The id after `options:` is a short kebab-case slug, unique in the file. Draw
every option at the same zoom with the same node ids for shared things, so the
difference is the only thing that changes. Put your recommendation in the
reply, not in the block.

When the user picks, move the chosen option's diagram into the artifact it
decides (requirements, design, or an ADR's Decision section), record the
rejected options in the ADR's alternatives if the choice is worth an ADR, and
delete the whole options block. An options block left behind after the
decision is stale.

## 6. Show, then ask

The `interview` skill uses this turn when the subject is structural. Draw your
current understanding as one diagram, validate it, and ask a single question:
"What is wrong with this picture?" Add your recommendation of where to look:
the node or edge you are least sure of, and why. One diagram, one question.
When the answer comes back, redraw with the same node ids so the user sees the
correction land.

## 7. Wireframes

Screens are low-fidelity HTML sidecars under `docs/planning/<slug>/mockups/`,
linked from a Mermaid screen flow with `click` directives. The screen flow is
the record; the HTML only shows layout. The contract and the CSS kit are in
[MOCKUPS.md](MOCKUPS.md).

## 8. The viewer

A local page that renders `docs/` with the diagrams drawn, reloads on save,
turns options blocks into choosable cards, previews mockups, and lets the user
click a diagram node to comment on it. Offer it when the user is reviewing
several diagrams or choosing between options.

```bash
python3 <skill-dir>/scripts/docs_viewer.py --root . --port 4178 --open
```

Run it in the background, give the user the URL (`http://127.0.0.1:<port>/`),
and keep going. It binds to 127.0.0.1 only. Before the first start, make sure
`.viewer/` is in the repo's `.gitignore`; add the line if it is not.

Choices and comments append JSON lines to `.viewer/events.jsonl`:

```json
{"ts": "2026-10-13T09:12:03Z", "type": "choice", "file": "docs/planning/x/design.md", "block": "storage-shape", "choice": "Option B: shared table with tenant_id"}
{"ts": "2026-10-13T09:13:40Z", "type": "comment", "file": "docs/planning/x/design.md", "node": "Orders DB", "text": "this is two stores"}
```

Every turn the viewer is in use, read the file first, act on each event (a
choice resolves its options block as in step 5; a comment is an answer to
"what is wrong with this picture"), then truncate it to empty so the next turn
sees only new events. Say in your reply which events you acted on. Stop the
viewer when the session is done with it.

## Style

Practitioner prose around diagrams, never decoration. Direct captions. State
the default when there is a choice. No em dashes.
