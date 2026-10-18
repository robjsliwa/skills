---
name: interview
description: >-
  Interview the user one question at a time, with a recommendation every turn,
  until something is settled. Two subjects. Align: intent, scope, users, and
  language become shared, terms are challenged against GLOSSARY.md and written
  as they settle, ADRs offered when a decision clears the bar. Decide: a tree of
  coupled decisions walked in dependency order and written to a findings
  document or the caller's document. Draws the current understanding as a
  Mermaid diagram and asks what is wrong with it. Use when the user says
  "interview me," "grill me," "align on this," "think it through," "walk the
  design tree," "resolve the open questions," or when a mode or skill needs
  intent or a design settled before it writes. Pauses to a file for a
  detour and resumes from it.
argument-hint: "Optional: 'align' or 'decide', then the subject (an idea, a file path, or a question). Or 'resume <slug>' to pick up a paused interview."
---

# Interview

Turn a vague idea, or a design full of open forks, into something settled, by
asking one question at a time, recommending an answer every time, and walking in
dependency order. Replaces v1's `design-interview` and alignment grilling.

The value is discipline. The failures it prevents are the wall of questions
(fifteen at once) and the wall of assumptions (ten guesses presented as a
finished design the user never steered). Each answer changes what the next
question even is.

## Pick the subject

- **Align** when intent, scope, users, or language are not yet shared: a new
  idea, a change request, the start of the full or light loop. Output is the
  shared understanding plus `GLOSSARY.md` and ADR updates, no findings document
  unless the user asks. Playbook: [ALIGN.md](ALIGN.md).
- **Decide** when the problem is a space of coupled decisions: an architecture,
  a data model, an auth model, an API contract, a scope cut. Output is a
  findings document at `docs/planning/<slug>/findings.md`, or the caller's
  document. Tree and template: [DECIDE.md](DECIDE.md).

If unclear, start with align; a decide tree often appears once the language is
shared. Do not use this skill for one well-posed question or when the user wants
a fast one-shot answer. Then just answer.

## The contract

Four rules govern every turn.

1. **One question at a time.** One headline question per turn, then stop. A
   downstream concern can ride along as "a later question owns this," never as
   a second question.
2. **Recommend, don't just ask.** Every question carries your recommended
   answer, the reasoning, and the tradeoff. The user reacts to a proposal; a
   bare question wastes their attention.
3. **Walk in dependency order.** Ask next whatever unblocks the most. What a
   tenant is comes before how tenants are billed. Say where each question sits.
4. **Explore instead of asking.** If the code, the docs spine, an attached file,
   or a quick search answers it, go read it and state what you found. Ask only
   what needs the user's judgment. For a fact that needs real reading, start a
   `research` agent in the background and ask about something else meanwhile.
   When the question is "does it actually work," it is a `spike`; when it is
   "how should it look or behave" and words are not settling it, offer a
   `prototype`. When the questions keep multiplying, suggest `trailblazer`.

## Step 0: Ground yourself

Before the first question, read what exists so you never ask what you could have
read:

- A paused `docs/planning/<slug>/interview.md` for this subject: resume it per
  "Pause and resume" below instead of starting over.
- Every attached or named file, in full.
- `docs/agents/profile.md` for docs locations and diagram settings (defaults if
  missing; say once that `/repo-setup` would make it explicit).
- `CONTEXT.md`, `GLOSSARY.md`, and the ADRs. These are the language and the
  boundary you are working inside.
- The codebase around the subject. Existing patterns and prior decisions answer
  some questions outright and constrain others.

Note constraints, non-negotiables, and stated goals. If it is truly greenfield,
say so in a line and move on.

## Step 1: Map the tree

Lay out the branches you intend to walk, in order, with a line on why that order
(what depends on what). A paragraph or a short list. The user can reorder, add,
or cut before you start. Then ask the first question.

## Step 2: One turn at a time

### Question turns

1. **Name the question and its place.** "Question 4 (after login): what
   credential does a principal carry?"
2. **Recommend plainly**, before the reasoning.
3. **Reason**, with the tradeoff and why the alternatives lose, as to a sharp
   colleague who will push back.
4. **Name the soft spot**: the one sub-fork where a reasonable person with other
   priors would choose differently. Invite the override.
5. **End with the explicit decision**: one or two sentences on exactly what you
   want accepted or changed.

Keep adjacent decisions apart. When a later concern surfaces, say which later
question owns it and move on.

### Option turns

When a decision has two or three structural alternatives (shapes, not
settings), present them as an options block, each with a small Mermaid diagram
and a one-line tradeoff, then your recommendation and the decision you want:

```markdown
<!-- options: storage-shape -->
### Option A: one table per tenant
<mermaid block>
Tradeoff line.

### Option B: shared table with tenant_id
<mermaid block>
Tradeoff line.
<!-- /options -->
```

Draw the diagrams through `visualize` (notation in
the `visualize` skill's `NOTATION.md`). The block goes in the conversation, or
in the document the decision will land in when the viewer is running, so the
viewer shows it as cards with a Choose button. On the user's next turn, read
`.viewer/events.jsonl` for a `choice` event on that block, then truncate the
file. Merge the click with the chat reply; if they conflict, the chat wins. When
settled, move the chosen diagram into the artifact it decides and remove the
options block.

### Show, then ask

Draw your current understanding as one Mermaid diagram via `visualize`, then ask
one question only: **"What is wrong with this picture?"** Add your
recommendation of where to look: the edge or node you are least sure of, and
why.

- Use it when the subject is structural (actors, flow, states, boundaries), and
  at least once in every align session.
- One idea per diagram, roughly 12 nodes, glossary terms as node labels, a
  caption sentence underneath. Validate it with
  the `visualize` skill's `scripts/mermaid_check.py` when the profile has
  validation on; otherwise mark it unvalidated.
- Where it goes: in the conversation by default. If the viewer is running
  (the `visualize` skill's `scripts/docs_viewer.py`), write it to the scratch
  file `docs/planning/<slug>/sketch.md` instead and tell the user to look there;
  read `.viewer/events.jsonl` for node `comment` events next turn and treat them
  as part of the answer.
- Fold the corrections in, and redraw only if the picture changed materially.
  The sketch file is scratch: once the picture lands in its real artifact
  (CONTEXT.md, requirements, design), delete the sketch.

### Handle the response

- **Accept:** lock it, restate it in one line, move on.
- **Refine or add a constraint:** integrate it and propagate it. Check which
  downstream questions it changes, adjust the plan, confirm, continue.
- **Overrule:** take it cleanly and follow its consequences. Do not relitigate.
- **New branch:** add it to the tree; reorder if it now blocks something.

### Track three lists

- **Settled:** one line per decision or agreed fact.
- **Deferred / out of scope:** what is deliberately left, and why.
- **Designed seams:** choices made now so later work is additive, not a rewrite.

## Step 3: Stop

Done when every branch is settled or explicitly deferred and nothing settled
leaves a dangling dependency. Recap in one short pass: what was walked, what is
left out. Confirm the user agrees before writing anything up. Do not pad with
low-value questions; do not stop with forks open.

## Step 4: Write up

- **Align:** the glossary and ADR updates are already written as you went.
  Summarize the shared understanding in the conversation (or in the caller's
  document). Write a findings document only if asked.
- **Decide:** write the findings document from the template in
  [DECIDE.md](DECIDE.md), or hand the three lists and the reasoning to the
  caller.

## When another skill invokes this

`write-requirements`, `solution-design`, `vertical-slice-phasing`, the modes,
and the pairing skills run this interview on their own subject. The caller may
name the subject, what to absorb in step 0, the tree to map, names for the three
lists, and the document to write. Those override the defaults; the contract, the
turn anatomy, and the glossary discipline do not. Hand the result back and let
the caller write its own document.

**Inside a `trailblazer` trail** the trail owns the tree, the files, and the
pace, so only the turn anatomy (Step 2) and the response handling apply. The
trail map replaces Step 1's tree and Step 3's recap. Sketches and options go in
the active node file (`docs/research/<topic>/nodes/`), never in
`docs/planning/`. A fuzzy term goes on the map's Terms in play list and is
settled only when a decision depends on it, instead of stopping the turn. Keep
a turn to about 150 words of prose plus its diagrams; the soft spot is one
sentence inside the recommendation, not a second question.

## Pause and resume

An interview lives in the conversation, so a `/clear` loses the tree and the
three lists. When the user takes a `detour`, or asks to stop and pick up later,
write them to a pause file first: `docs/planning/<slug>/interview.md`
(planning root from the profile), next to the findings document it will become.

```markdown
# Interview: <subject> (paused)

**Subject:** align | decide   **Paused:** <date>, for detour NNNN (or "by the user")
**Caller:** none | <skill>, writing <document>
**Read in step 0:** <the files, so resume re-reads the same ones>

## Tree
1. <branch> (settled)
2. <branch> (on the table)
3. <branch>

## Settled
- <one line per decision or agreed fact>

## Deferred / out of scope
- <item, and why>

## Designed seams
- <item>

## On the table
<The question as asked, the recommendation and its soft spot, and what the user
had said about it so far, including what they did not understand.>
```

Commit it with the detour brief. To resume (`/interview resume <slug>`, or
when step 0 finds a paused file for the subject):

1. Re-read the files it lists and the file itself, then every brief in
   `docs/detours/` whose `Paused` line points at it, per the `detour` skill.
2. Play back in at most 150 words: the subject, what is settled, and what the
   detour returned.
3. Re-ask the question on the table, rewritten with what the user now knows.
   The recommendation may change; say so if it does.
4. Carry on from Step 2. When the write-up lands, delete the pause file; if a
   caller is named, tell the user to re-run it, now that the interview is done.

Inside a trail, the trail's own files are the pause: the active node holds the
question, so no pause file is written.

## Conventions

- **Always recommend, even when unsure.** Lean, and say what would change your
  mind.
- **Show the soft spots.** Visible weaknesses make the recommendation more
  useful, not less.
- **Match the user's depth** and vocabulary, except where the vocabulary is
  fuzzy: then settle the term (see [ALIGN.md](ALIGN.md)).
- **Prose over heavy formatting.** Lists only for real enumerations. No em
  dashes.
- **Stay in scope.** When the user draws a boundary, hold it and note where the
  other side lives.
- **A gap is not a failure.** When the user cannot answer because they do not
  know the subject yet, and a few sentences will not fix it, offer a `detour`
  instead of answering for them.
