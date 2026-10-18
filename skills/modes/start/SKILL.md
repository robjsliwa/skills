---
name: start
description: >-
  The front door. Read the repo's state and the user's goal, then recommend one
  of the five modes (trailblazer, full loop, light loop, code-along, pairing) with a
  one-line reason and the exact first command. Use when the user says
  "where do I start," "what should I run," "which loop," "I have an idea,"
  or runs /start. It points; it does not do the step.
disable-model-invocation: true
argument-hint: "Optional: what you want to build or change, in a sentence."
---

# Start

Five ways to work, one entry point. This skill looks at what exists, asks at most
one question, and names a mode and its first command. It never runs the step
itself; the mode skill does that in a clean context.

## The five modes

| Mode | Pick it when | First command |
|---|---|---|
| **Trailblazer** | Fog. The idea is big or vague, nobody can yet say what the questions are, and the first job is finding the way, not planning the build. | `/trailblazer <the idea>` |
| **Full loop** | The architecture is the hard part. A wrong call now is a rewrite later, or the work has an obvious phase-one-versus-later split. | `/interview` (align), then `/write-requirements` |
| **Light loop** | One coherent change with no real design choice. You could open the editor now; the only question is where the first test goes. | `/light <the change>` |
| **Code-along** | A story exists (from either loop) and you want to write the code yourself and understand every line. A build mode, mixed freely with `tdd` per story. | `/code-along <story file>` |
| **Pairing** | The spec is clear enough to start and the learning happens in the code. You want to build one small piece at a time with the agent beside you. | `/pair-setup` once, then `/pair-slice <spec> <piece>` |

Judge weight, not size. A two-line change that decides the tenancy model is full
loop. A big but mechanical change is light. Judge fog separately: if you cannot
list the open questions yet, it is trailblazer, whatever the size.

A single technical unknown ("will FTS5 keep up?") is not a mode. It is a `spike`,
and any mode can run one. Neither is "I don't understand this yet" in the middle
of a mode: that is a `detour`, which pauses the mode, sends the gap to
`teach-me` or `trailblazer` in a clean context, and brings the answer back.

## Read the state

Check silently, in this order, and stop at the first row that matches:

| What exists | Recommend |
|---|---|
| No `docs/agents/profile.md` and the user is about to plan or build | `/repo-setup` first, then come back |
| A brief in `docs/detours/` with `Status: answered` | Resume the flow its `Paused` line names; it folds the answer in |
| `docs/pairing/STATE.md` with an active slice | Resume pairing: `/pair` |
| A trail at `docs/research/*/map.md` with `Status: exploring` | Resume it: `/trailblazer <topic>` |
| A trail with `Status: arrived` whose report's Next step has not been run | The step its report names |
| A lesson under `docs/planning/*/lessons/` with `status: open` | Debrief it: `/code-along` |
| `docs/planning/<slug>/` with artifacts but stories not all done | The full loop's next step: `/planning-loop` names it |
| A story with `Status: ready` and no phases (a light change) | Build it: `/tdd <story>` or `/code-along <story>` |
| Nothing in progress | Decide the mode from the user's goal (below) |

## Decide from the goal

If the user gave a goal, weigh it against the table above. Recommend one mode,
with the reason in one line and the first command. Name the runner-up only when
it was close, in one more line.

If the goal is not enough to choose, ask one question, with a recommendation:
"Is the hard part knowing what we need, deciding how to build it, or building
it? I'd guess building it, so light loop, because ___." Then recommend: knowing
what we need is trailblazer, deciding how is the full loop, building is light,
code-along, or pairing.

If `docs/code-along/NOTES.md` exists, the user has used code-along here; mention
it as the build mode once a story exists. If `docs/pairing/WORKING-AGREEMENT.md`
exists, the repo is set up for pairing; pairing costs nothing extra to start.

## Shared spine

Every mode reads and writes the same files, so switching later is free:
`CONTEXT.md` (system context), `GLOSSARY.md` (language), `docs/adr/` (decisions),
`docs/agents/profile.md` (tracker and commands), `CLAUDE.md` (agent contract). A
feature designed in the full loop can be built story by story with `code-along`,
or slice by slice with `/pair-slice` pointed at its `design.md`.

## Rules

One recommendation per turn, named plainly, with the command to type. Do not run
the step. If the user disagrees with the mode, take their choice without argument
and give that mode's first command.
