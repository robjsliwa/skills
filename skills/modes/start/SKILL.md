---
name: start
description: >-
  The front door and the router. Read the repo's state, the planning artifacts
  on disk, and the user's goal, then recommend one of the five modes
  (trailblazer, full loop, light loop, code-along, pairing), or the next step of
  work already under way, with a one-line reason and the exact first command.
  Use when the user says "where do I start," "what should I run," "which loop,"
  "what comes next," "where are we in the plan," "which planning skill applies,"
  "I have an idea," or runs /start. It points; it does not do the step.
argument-hint: "Optional: what you want to build or change, in a sentence."
---

# Start

Five ways to work, one entry point. This skill looks at what exists, asks at most
one question, and names a mode and its first command, or the next step of the
work in progress. It never runs the step itself; the mode skill does that in a
clean context.

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
`professor` or `trailblazer` in a clean context, and brings the answer back.
Learning a whole subject, rather than unblocking a task, is not a build mode
either: that is `/professor <subject>` in its own workspace.

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
| `docs/planning/<slug>/` with artifacts (or a PRD in the tracker `docs/agents/profile.md` names) and work left | The next step from [The full loop](#the-full-loop) |
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

## The full loop

One feature, from idea to shipped code, one artifact per step. Every artifact
lives under `docs/planning/<slug>/` (or in the configured tracker), so the user
can clear context between steps and the next skill picks up from disk.

```
interview (align)         align; GLOSSARY.md, CONTEXT.md, ADRs grow as you go
   │
write-requirements        the WHAT  → requirements.md, or a tracker issue
   │  (clear context)
solution-design           the HOW   → design.md, plus docs/adr/
   │  (clear context)
vertical-slice-phasing    the ORDER → phases.md, walking skeleton first
   │  (clear context)
elaborate-current-phase   this phase only, via to-story → stories/NN-MM-*.md
   │  (clear context)         or tracker issues; each story a change a person can
   │                          see, owning its tasks
tdd  or  code-along        one story per context window; flip Status to done
   │                         tdd builds it for you, task by task; code-along builds
   │                         it with you, as a lesson you code, then a debrief
review-change              review against the story, scaled to its risk
   │
   └── every story in the phase done ──► elaborate-current-phase again,
                                          re-derived against the real code.
                                          Repeat until the last phase.
```

The return arrow is what makes this a loop rather than a line. You do not plan
all phases once. You plan one, build it, then re-plan the next against what the
code now is.

Match the first row that describes what exists, and name its next step:

| What exists | Next step |
|---|---|
| `requirements.md` (or the PRD issue), no `design.md` | `solution-design` |
| `design.md`, no `phases.md` | `vertical-slice-phasing` |
| `phases.md`, current phase has no stories | `elaborate-current-phase` |
| Stories with open status | `tdd` or `code-along` on the first unblocked story |
| Every story in the current phase done | `elaborate-current-phase` |
| Every phase done | Nothing. Ship it. |

When the user describes their state instead of having artifacts, map it the same
way: "requirements are agreed" is the first row, "phase one shipped" is the
fifth. An idea with no artifacts is not in this table: decide the mode from the
goal.

`tdd` writes the code: pick it for work the user is happy to delegate and review.
`code-along` writes a lesson, the user writes the code, and a debrief records
what they built: pick it for code they will maintain, debug, or explain, or to
learn the stack. The two mix freely, story by story.

## Shared spine

Every mode reads and writes the same files, so switching later is free:
`CONTEXT.md` (system context), `GLOSSARY.md` (language), `docs/adr/` (decisions),
`docs/agents/profile.md` (tracker and commands), `CLAUDE.md` (agent contract). A
feature designed in the full loop can be built story by story with `code-along`,
or slice by slice with `/pair-slice` pointed at its `design.md`.

## Rules

One recommendation per turn, named plainly, with the command to type. Do not run
the step. If the user disagrees with the mode, take their choice without argument
and give that mode's first command. State persists in the files, not in the chat,
so a fresh session can pick up at any step by reading them.
