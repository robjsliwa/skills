---
name: to-story
description: >-
  Break a design, or one phase of a phased design, into tracer-bullet stories
  that carry the design detail an implementer needs: interfaces, data
  structures, algorithms, sample code, diagrams, a RED-first test plan, and
  blocking edges. Publishes them to the configured issue tracker or as story
  files. Use when the user says "write the stories," "break this into
  stories," "explode this phase," or when elaborate-current-phase hands over a
  phase to detail.
---

# To Story

Turn a design into stories an agent can build one per context window. Each story
is a tracer bullet: a narrow but complete vertical slice, demoable on its own,
that declares which stories block it. Unlike a bare ticket, a story carries its
design. The interfaces, structures, algorithm, sample code, and diagrams the
design doc already settled ride along, trimmed to what this slice needs, so the
implementer inherits a mechanism instead of inventing one per session.

## Inputs

Work from what is already in context, then fetch what is not.

- **The design doc**, `docs/planning/<slug>/design.md`, and the requirements it
  traces to (their R-ids). If there is no design, stop and say so; stories written
  from requirements alone guess at mechanism, which is what solution-design
  exists to prevent.
- **The phase to explode**, when elaborate-current-phase hands one over or the
  user names one: its scope, its acceptance checkpoint, the seams it introduces
  or relies on. Stories go no wider than the phase.
- **The codebase.** Real ports, adapters, schema, `CONTEXT.md`, and ADRs in the
  area. Story vocabulary follows the glossary. Where built code and the design
  disagree, the code is ground truth; note the disagreement in the story.
- **The tracker config**, `docs/agents/issue-tracker.md`. It decides where stories
  are published (step 5).

## 1. Slice

Break the work into tracer-bullet stories.

- Each story cuts a narrow but complete path through every layer it touches
  (schema, port, adapter, surface, tests): vertical, never one layer.
- A completed story is demoable or verifiable on its own.
- One story is one PR and fits one fresh context window. Split when the
  acceptance criteria fall into two groups with no shared prerequisite, or when
  the design section would run past a screen of code.
- Front-load the contract. The first story in a phase usually defines the
  interfaces, types, or schema the rest implement behind, so later stories test
  against stable signatures.
- Prefactoring comes first. If a small refactor makes the slice easy, it is its
  own story at the head of the chain: make the change easy, then make the easy
  change.

Give every story its **blocking edges**: the stories that must finish before it
can start. A story with no blockers can start immediately.

Wide refactors are the exception to slicing. A mechanical change whose blast
radius spans the codebase (rename a column, retype a shared symbol) cannot land
green as one slice. Sequence it as expand, migrate, contract: add the new form
beside the old; migrate call sites in batches sized by blast radius, each batch a
story blocked by the expand; delete the old form in a story blocked by every
batch.

## 2. Carry the design

This is what separates a story from a ticket. For each story, pull from the
design doc the parts this slice touches, and only those:

- **Interfaces and types.** Signatures in the repo's language: the port, the
  domain type, the request and response shape.
- **Data.** Schema or struct sketch, invariants, the isolation rule if
  multi-tenant.
- **Algorithm.** Numbered steps or pseudocode for anything a reader could get
  wrong: ordering, retries, state transitions, validation order.
- **Diagram.** A Mermaid block when a picture beats prose: a sequence diagram for
  a flow across components, a state diagram for a state machine, an ER diagram
  for data.
- **Sample code.** A sketch of the decision-rich core, ten to forty lines, not a
  working implementation. It shows the shape the implementer should land on.
- **Files.** The paths the story creates or touches.

Derive, do not invent. If a story needs a decision the design does not make,
make it in the story, mark it `(story decision)`, and say so in the hand-off so
the design doc can absorb it. Trim to the decision-rich parts. Omit any
subsection the story does not need; an empty heading is noise.

## 3. Prove it

- **TDD plan.** Numbered tests, RED first, named `Subject_Condition_Outcome`,
  ordered the way they should be written (simplest pure function first, the
  most integrated last), each at a named seam. Name the fake or fixture where
  it matters.
- **Acceptance criteria.** Checkable, each tied to a requirement id. "It works"
  is not a criterion.
- **Verification.** The commands that prove the story, with expected output,
  including one manual smoke (a curl, a CLI call) that produces visible output.

## 4. Quiz the user

Present the breakdown as a numbered list. For each story: title, blocked by,
and the end-to-end behaviour it delivers. Ask whether the granularity is right,
whether each blocking edge is a real gate, and whether anything should merge or
split. Iterate until the user approves. Only then write the full stories.

## 5. Publish

Read `docs/agents/issue-tracker.md`.

- **A real tracker** (GitHub, GitLab, Jira, Linear, or a freeform workflow the
  config describes): one issue per story, blockers first so edges can reference
  real ids. Use the platform's native blocking or sub-issue relationship where
  it has one; otherwise a `Blocked by` line. Apply the `ready-for-agent` label.
  Link the parent (the PRD issue or epic) when there is one. The body is the
  template below without the `Status` line; the tracker holds the state.
- **Local markdown, or no config:** one file per story at
  `docs/planning/<slug>/stories/NN-MM-<story-slug>.md`, `NN` the phase number
  (`01` when there is no phased design) and `MM` the story index in dependency
  order from `01`. Never one combined file.

Do not close or modify the parent issue.

## Story template

````markdown
# NN-MM: <Story title>

**Status:** ready-for-agent
**Phase:** <phase number and name, or "none">
**Blocked by:** <NN-MM title, ...> or "None, can start immediately"
**Serves:** R3, R7; design: Ports, Control flow

## What to build

The end-to-end behaviour this story makes work, from the user's perspective.
Two to four sentences. Name what is deliberately kept simple.

## Design

### Interfaces and types
### Data
### Algorithm
### Diagram
### Sample code
### Files

(Keep only the subsections this story needs.)

## TDD plan

1. **Subject_Condition_Outcome** at <seam>: what it asserts.
2. ...

## Acceptance criteria

- [ ] <checkable statement> (R3)
- [ ] ...

## Out of scope

What this story does not do, and which story or phase does.

## Verification

```bash
<test command>
<manual smoke>   # expect: ...
```
````

A worked example is in `references/example-story.md`; read it before writing the
first story of a session so the density is right.

## Style

Practitioner notes, not ticket-speak. Direct and concrete: "set `app.tenant_id`
inside the transaction; never write `WHERE tenant_id = ?` in app code." Prose
where prose works, code where code is shorter. State the default when there is a
choice. No em dashes.

## Hand off

Work the frontier, any story whose blockers are done, one story at a time with
`tdd`, clearing context between stories. When a story lands, flip its `Status`
to `done` (or close the issue). When every story in the phase is done, run
`elaborate-current-phase` to re-derive the next phase against the real code.
