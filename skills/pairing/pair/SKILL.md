---
name: pair
description: >-
  Pick up pair programming where it left off: rebuild context from the memory
  bank (docs/pairing/), git, and the open PR, brief the user in a few lines,
  then continue the slice or route to setup, a new slice, or shipping. Use at
  the start of a fresh session on a paired repo, or when the user says "where
  were we," "pick up where we left off," "let's continue," or runs /pair.
argument-hint: "Nothing, to resume. Or a spec file or text plus the piece to work on, which goes to pair-slice."
---

# Pair

The entry point for every pairing session. A fresh context knows nothing; the
memory bank, git, and the PR know everything. This skill reads all three,
reconciles them, tells the user in a few lines where things stand, and then
gets back to work. It never re-plans: the slice on disk is what was agreed.

Call the Skill tool with `pairing` first. It holds the step loop and
MEMORY-BANK.md, the formats this skill reads.

If the user passed a spec, a file, or "I want to work on X," and no slice is
active, call the Skill tool with `pair-slice` with their argument and stop
here.

## 1. Read

- `CLAUDE.md` and `docs/pairing/WORKING-AGREEMENT.md`. If the agreement is
  missing, hand off to `pair-setup` and stop.
- `docs/pairing/STATE.md`, then the active slice file in full: goal,
  acceptance, plan, parked, drift, and the whole journal (the last session's
  `Session end` entry first).
- `ROADMAP.md`, the glossary, and the ADRs the slice lists. Skim the titles of
  the rest of `docs/adr/`.
- Git: `git branch --show-current`, `git status --short`,
  `git log <base>..HEAD --oneline`, `git log -1 --format=%cd`, and
  `git branch -a --no-merged <default>` to find slice branches still in
  flight (parked or awaiting merge).
- The PR, when `STATE.md` or the slice names one and a remote exists:
  `gh pr view <n> --json state,reviewDecision,comments,reviews,statusCheckRollup`.
  The PR state outranks `STATE.md` (see MEMORY-BANK.md).

Done when every file above that exists has been read and every command run.

## 2. Reconcile

The disk can disagree with `STATE.md` because the user kept working without
an agent, or a session ended without a checkpoint. Find each mismatch and
settle it before the brief.

| Found | Do |
|---|---|
| On a different branch than `STATE.md` names | Ask which is current. Never switch branches with uncommitted changes |
| Uncommitted changes | Read the diff. Ask the user what it is, one question. Journal it as `User-coded`, and commit it when they confirm it is green |
| Commits after the last journaled commit | Read them. Journal one `User-coded` entry summarizing them, with the user's reason |
| Plan steps ticked in commits but not in the slice, or the reverse | Fix the slice to match the code; the code is ground truth |
| PR has unaddressed review comments or failing checks | Route to `pair-ship` (address stage) |
| PR merged, but the local default branch is behind or the slice branch remains | Route to `pair-ship` (wrap stage) |
| Tests red at HEAD with no `wip` note in `STATE.md` | Say so in the brief; the first step is to get back to green |

Run the fast test command from the agreement once, so the brief reports the
real state. Done when the memory bank matches git, or each remaining mismatch
is in the brief as a question.

## 3. Brief

Ten lines at most, in this shape:

```
Building: 0003 Invoice totals (S1 §3.2), on feat/0003-invoice-totals.
Done: steps 1 to 4 of 6. Last: half-even rounding, green, committed.
Since then: you renamed Line.Amount to Line.Subtotal (journaled).
Tests: green.  PR: none yet.
Open: is a zero-quantity line an error or a no-op?
Next: step 5, reject negative quantities, test first, ping-pong.
```

Then the one question that unblocks work: usually "carry on with step 5?",
or the open thread if step 5 depends on it.

## 4. Route

Take the first row that matches. PR rows come first because the PR state
outranks the memory bank.

| State | Next |
|---|---|
| No `WORKING-AGREEMENT.md` on this branch or the default branch | `pair-setup` |
| A recorded PR is open (any phase) | `pair-ship`; it picks its own stage |
| A recorded PR is merged, local branches not wrapped | `pair-ship` wrap stage |
| On a slice branch whose slice is `parked` | Ask to unpark. On yes: slice and `STATE.md` back to `building`, an `Unparked` journal entry, continue the `pairing` loop |
| Active slice, plan steps open | Append a `Session start` journal entry and continue the `pairing` step loop from `Next step` |
| Active slice, plan done | Offer `pair-ship` |
| No active slice, a parked slice branch exists | Mention it in the brief, then ask: unpark it or start a new piece |
| No active slice, `ROADMAP.md` has a `next` piece | Offer `pair-slice` on it |
| No active slice, nothing agreed | Ask which piece of the spec to work on; then `pair-slice` |

`Phase: merging` with a merged PR counts as no active slice.

## Rules

- **Read everything before saying anything.** The brief is built from files
  and commands, not from guesses.
- **The user's offline work is data, not drift.** Record it and the reason.
- **One question at a time** during reconcile; never a list of five.
- **Do not re-carve the slice.** If the user wants to change direction, edit
  the plan as a `Plan change` journal entry, or park the slice through
  `pair-checkpoint` and start a new one.
