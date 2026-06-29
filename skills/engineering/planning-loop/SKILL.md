---
name: planning-loop
description: >-
  Route to the right planning step and explain the full plan-to-build loop. Use
  this when the user asks where to start, what comes next, "what skill do I use
  for this," how the planning pipeline fits together, or when they have a rough
  idea and are not sure whether they need a grilling, a PRD, a design, phasing,
  or just to start coding. A user-invoked orchestrator over the planning skills:
  it points you at the next step, it does not do the step itself. Invoke the
  model-invoked skills it names to actually do the work.
---

# Planning Loop

The spine that connects the Pocock chain, the existing planning skills, and the
progressive-elaboration loop. Its job is to tell the user, or you, which step the work
is at and what to invoke next. It orchestrates; it never does the downstream step
itself.

## The loop

```
grill-me / design-interview   align, resolve the design tree
        │
write-requirements → to-prd   the WHAT, template-driven, filed as an issue
        │
solution-design               the HOW: ports, adapters, det/prob split, seams, ADRs
        │  (invokes design-interview for coupled decisions)
vertical-slice-phasing        the build ORDER: walking-skeleton-first phases
        │
elaborate-current-phase       detail THIS phase only, via phased-implementation-plan
        │                     or to-issues; later phases stay sketches
tdd                           build the phase, RED first
        │
story-review                  gate the work
        │
        └── phase done ──► elaborate-current-phase again (re-derive next phase
                            against the real codebase). Loop until the last phase.
```

The thing that makes this a loop rather than a line is the return arrow. You do not
plan all phases once. You plan one, build it, then re-plan the next against what the
code now is.

## Pick the path: light or heavy

Not every change earns the whole loop. Judge by architectural weight, not size of diff.

- **Light path** (a single coherent vertical slice, no real architectural choice):
  `grill-me` to align, then `to-issues`, then `tdd`. The slice is its own design. Do
  not manufacture ceremony for it. This is the Pocock chain as-is, and it is correct
  for this case.
- **Heavy path** (coupled decisions, multiple phases, a contract others depend on, or
  anything you will regret getting wrong): the full loop above. The design and phasing
  steps are not overhead here; they are the cheapest place to be wrong.

The tell for the heavy path: you cannot name the ports without thinking, the work has
an obvious phase-one-versus-later split, or a wrong call now means a rewrite later. The
tell for the light path: you could open the editor right now and the only question is
where the first test goes.

## Where you probably are, and what to invoke

- "I have an idea but it is fuzzy" → `grill-me`, or `design-interview` if the decisions
  are coupled and you want a durable findings doc.
- "We have aligned, write it up" → `write-requirements`, then `to-prd`.
- "Requirements are agreed, how do we build it" → `solution-design`.
- "Design is done, what is the build order" → `vertical-slice-phasing`.
- "We have phases, what do I build first" → `elaborate-current-phase` (current phase
  only).
- "Phase one is shipped, what now" → `elaborate-current-phase` again, to re-derive
  phase two against the real code.
- "A story is ready to build" → `tdd`.
- "Review this story before I build it" → `story-review`.

## Invocation rules

This is a user-invoked orchestrator. It may invoke the model-invoked planning skills
(`write-requirements`, `solution-design`, `elaborate-current-phase`) and point at the
other user-invoked ones (`grill-me`, `design-interview`, `vertical-slice-phasing`,
`to-prd`, `to-issues`, `tdd`, `story-review`). It does not run a downstream step's
work inline; it hands off. One headline next-step per turn, named plainly, with a
one-line reason.

## The principle behind the loop

State persists in files, not in the chat: the requirements doc, the design doc and its
ADRs, the phased design, the per-phase stories, `CONTEXT.md`. A fresh session can pick
up the loop at any step by reading those artifacts. The chat is scaffolding; the
documents are the system. Plan the phase you are about to build in full, sketch the
rest, and re-derive each next phase only when the code that informs it exists.
