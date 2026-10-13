---
name: to-story
description: >-
  Break a design, or one phase of a phased design, into stories a person can
  see: each with a Scenario, a Demo, a Picture, and Acceptance in the user's
  words, owning the context-window sized Tasks that carry the design detail
  (interfaces, data, algorithm, sample code, RED-first TDD plan). A critic in a
  fresh context checks the breakdown before the user sees it. Publishes to the
  configured tracker or as story files. Use when the user says "write the
  stories," "break this into stories," "explode this phase," or when
  elaborate-current-phase or light hands work over.
---

# To Story

Turn a design into stories. Each story is one change a person can see, in the
format the `story` skill owns (its `FORMAT.md`). Each story owns
one to five tasks, and each task is what an agent builds in one context window,
with the design detail the design doc already settled riding along. People read
the top of the file; agents read the tasks.

The order matters. Slice by what a person would notice first, then decide the
tasks that deliver it. Slicing by tasks first is how a breakdown turns into
"tenant port, Postgres adapter, redirect endpoint."

## Inputs

Work from what is already in context, then fetch what is not.

- **The design doc**, `docs/planning/<slug>/design.md`, and the requirements it
  traces to (their R-ids). If there is no design, stop and say so, unless `light`
  handed over a single change, whose story carries its own small design.
- **The phase to explode**, when elaborate-current-phase hands one over or the
  user names one: its scope, its acceptance checkpoint, its seams, its part of
  the story map, and the rows of the traceability table in `phases.md` that
  assign requirement ids to it. Stories go no wider than the phase and together
  serve every requirement the table gives it.
- **`GLOSSARY.md` and `CONTEXT.md`.** The actors and the words. Story titles,
  scenarios, and pictures use them.
- **The codebase.** Real ports, adapters, schema, and ADRs in the area. Where
  built code and the design disagree, the code is ground truth; say so in the
  task.
- **`docs/agents/profile.md`.** Where stories are published, and the `Run the
  app` command the Demos use.

## 1. Find the changes a person would see

Walk the phase's slice of the journey (the story map in `phases.md`, or the
journey in the requirements) and list the moments where somebody can do
something new. Each one is a candidate story. Write each as a title and a Demo
sentence, nothing else yet.

- The first story is a walking skeleton: the thinnest path a person can see
  working end to end, hardcoded where that keeps it thin.
- Split big candidates with the `story` skill's `SPLITTING.md`: workflow steps,
  rule variations, happy then unhappy, one data variation, one interface,
  hardcode then generalize, defer performance, spike the unknown. Never by layer.
- A candidate with no possible human demo is not a story. It becomes a task in
  the first story that needs it, or a spike if the unknown is the work.

## 2. Decide each story's tasks

For each story, the tasks that deliver its Demo, one to five, in build order.

- A task is one context window and one TDD plan with its own Verify.
- **Contract first, inside the story.** The walking skeleton's T1 usually fixes
  the interface, schema, or route table that later tasks and stories build
  behind, so they test against stable signatures.
- **Prefactoring** that makes a story easy is that story's first task: make the
  change easy, then make the easy change.
- **Wide refactors** are the exception. A mechanical change whose blast radius
  spans the codebase cannot land green as one task. Sequence it as expand,
  migrate in batches, contract: each batch a task, or a story of its own whose
  Demo is "everything still works and the old form is gone."

Give every story its **blocking edges**: the stories that must finish first.

## 3. Carry the design into the tasks

For each task, pull from the design doc the parts it touches, and only those:
interfaces and types in the repo's language; data and invariants; the algorithm
as numbered steps where a reader could get it wrong; a Mermaid diagram (per
`visualize`) when a picture beats prose; a ten to forty line sketch of the
decision-rich core; the files it creates or touches. Then a RED-first TDD plan
(`Subject_Condition_Outcome`, simplest first, each at a named seam) and Verify
commands with expected output.

Stories inherit `CLAUDE.md`, the agent contract solution-design wrote. A rule for
every story lives there, not in each task. Derive, do not invent: a decision the
design does not make is marked `(story decision)` and listed in the hand-off so
the design can absorb it.

## 4. Write the human header

For each story, per FORMAT.md: the Scenario (a person and a reason), the Demo,
the Picture (one diagram of the change a person notices, glossary terms as
labels, drawn and validated with `visualize`), Acceptance tied to R-ids, Out of
scope, and Verification (the Demo as commands, plus the full test command).

## 5. Run the critic

Follow "Check a breakdown" in the `story` skill: a fresh sub-agent
reads only the drafts, `GLOSSARY.md`, `CONTEXT.md`, and CRITIC.md, and rules
PASS or REJECT per story, then on the breakdown. Revise and rerun. Three
rejections on one rule go to the user with the objection attached.

## 6. Quiz the user

Present the breakdown as a numbered list. For each story: the title, its Demo
sentence, blocked by, the R-ids it serves, and its task titles on one line. Then
name every requirement the traceability table assigns to this phase that no
story serves; the user adds a story, moves the requirement, or strikes it. Ask
whether each story is something they would want to see, whether the edges are
real gates, and whether anything should merge or split. When the viewer is
running, also write the list to `docs/planning/<slug>/stories/BREAKDOWN.md` so it
renders with its pictures. Iterate until the user approves; only then write the
full stories. Delete `BREAKDOWN.md` after publishing.

## 7. Publish

Read `docs/agents/profile.md`.

- **A real tracker:** one issue per story, blockers first so edges reference real
  ids, using the native blocking or sub-issue relationship where the tracker has
  one. Apply the profile's ready label. Link the parent (requirements issue or
  epic). The body is the story without the `Status` line.
- **Local files, or no profile:** one file per story at
  `docs/planning/<slug>/stories/NN-MM-<slug>.md`, `NN` the phase (`01` with no
  phases), `MM` the dependency order from `01`, the slug taken from the title.

Do not close or modify the parent issue.

### Fill the traceability table

When `phases.md` exists, write the story ids into the Stories cell of every
requirement this phase's stories serve. A requirement assigned to this phase that
no story serves keeps an empty cell, so the gap stays visible. If a story serves a
requirement assigned elsewhere or nowhere, correct the row and say so. On the
light path, with no `phases.md`, the story's `Serves` line is the only trace.

## Style

Two registers in one file. The human header is plain and concrete, in the
user's words: "Maya taps the link and lands on her menu." The tasks are
practitioner notes: "set `app.tenant_id` inside the transaction; never write
`WHERE tenant_id = ?` in app code." No em dashes.

## Hand off

Work the frontier, any story whose blockers are done, one story at a time with
`tdd` (the agent builds it, task by task) or `code-along` (the user builds it
from a lesson, then debriefs), clearing context between stories. When every story
in the phase is done, run `elaborate-current-phase` to re-derive the next phase
against the real code.
