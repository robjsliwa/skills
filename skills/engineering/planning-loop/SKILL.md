---
name: planning-loop
description: >-
  Tell the user where they are in the plan-to-build loop and which skill to run
  next, by reading the planning artifacts on disk. Use when the user asks where
  to start, what comes next, or which planning skill applies to what they have.
  It points; it does not do the step.
---

# Planning Loop

One feature, from idea to shipped code, one artifact per step. Every artifact lives
under `docs/planning/<slug>/` (or in the configured tracker), so the user can clear
context between steps and the next skill picks up from disk.

```
grill-with-docs           align; CONTEXT.md and ADRs grow as you go
   │
write-requirements        the WHAT  → requirements.md, or a tracker issue
   │  (clear context)
solution-design           the HOW   → design.md, plus docs/adr/
   │  (clear context)
vertical-slice-phasing    the ORDER → phases.md, walking skeleton first
   │  (clear context)
elaborate-current-phase   this phase only, via to-story → stories/NN-MM-*.md
   │  (clear context)         or tracker issues
tdd  or  code-along        one story per context window; flip Status to done
   │                         tdd builds it for you; code-along builds it with you,
   │                         as a lesson you code, then a debrief
   │
   └── every story in the phase done ──► elaborate-current-phase again,
                                          re-derived against the real code.
                                          Repeat until the last phase.
```

The return arrow is what makes this a loop rather than a line. You do not plan all
phases once. You plan one, build it, then re-plan the next against what the code now
is.

## Find where the work is

Look at `docs/planning/*/` and, if `docs/agents/issue-tracker.md` names a real
tracker, at the tracker. Match the first row that describes what exists, and name its
next step:

| What exists | Next step |
|---|---|
| Nothing, or only an idea | `grill-with-docs`, then `write-requirements` |
| `requirements.md` (or the PRD issue), no `design.md` | `solution-design` |
| `design.md`, no `phases.md` | `vertical-slice-phasing` |
| `phases.md`, current phase has no stories | `elaborate-current-phase` |
| A lesson under `lessons/` with `status: open` | `code-along` (debrief it) |
| Stories with open status | `tdd` or `code-along` on the first unblocked story |
| Every story in the current phase done | `elaborate-current-phase` |
| Every phase done | Nothing. Ship it. |

When the user describes their state instead of having artifacts, map it the same
way: "I have an idea" is row one, "requirements are agreed" is row two, "phase one
shipped" is row six.

## Build mode: tdd or code-along

Both build one story per context window from the same story files; they differ
in whose hands write the code.

- **`tdd`** writes the code. Pick it for work you are happy to delegate and
  review.
- **`code-along`** writes a lesson for the story, you write the code, and a
  debrief records what you built and why before the next lesson is written.
  Pick it for code you will have to maintain, debug, or explain, or when you
  want to learn the stack.

The two mix freely, story by story. If `docs/code-along/NOTES.md` exists, the
user has used code-along in this repo; name it first unless they say otherwise.

## Light path

Not every change earns the loop. Judge by architectural weight, not diff size. A
single coherent vertical slice with no real design choice takes the light path:
`grill-with-docs`, then `to-story`, then `tdd` or `code-along`. The slice is
its own design.

The tell for the heavy path: you cannot name the ports without thinking, the work
has an obvious phase-one-versus-later split, or a wrong call now means a rewrite
later. The tell for the light path: you could open the editor now and the only
question is where the first test goes.

## Rules

One headline next step per turn, named plainly, with a one-line reason. Hand off;
do not run the step inline. State persists in the files, not in the chat, so a
fresh session can pick the loop up at any step by reading them.
