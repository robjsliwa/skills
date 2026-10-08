---
name: pair-slice
description: >-
  Start a new piece of paired work from a spec: take a file or pasted text
  describing the main idea plus "I want to work on this piece," carve that
  piece into a slice small enough for one PR (goal, scope, acceptance checks,
  a short plan), cut its feature branch, record it in the memory bank, and
  hand off to the step loop. Use when the user points at a spec, idea, or
  requirements and names what to build next, says "let's work on X," "next
  piece," or "start a slice."
argument-hint: "A spec file path or pasted text, plus the piece to work on (e.g. 'docs/spec.md, the invoice totals part')."
---

# Pair Slice

A slice is the unit of pairing: one piece of the spec, one branch, one PR, one
to a few sessions. This skill turns "here's the idea, I want to work on this
part" into a slice file with a goal, observable acceptance checks, and a short
plan whose first step is tiny, then cuts the branch and starts pairing. It
asks only what it takes to get to step 1; everything else is learned by
building.

Call the Skill tool with `pairing` and read its MEMORY-BANK.md for the slice,
STATE, and ROADMAP formats.

## 1. Preflight

- `docs/pairing/WORKING-AGREEMENT.md` exists on the default branch. If it
  exists only on an unmerged setup branch, the setup PR merges first: offer
  `pair-ship` on that branch and stop. If it exists nowhere, hand off to
  `pair-setup` and stop.
- `STATE.md` shows no active slice (`Phase: merging` with a merged PR counts
  as none). If one is active, ask once: finish it first, or park it? Parking
  runs `pair-checkpoint` with `parked`, which commits and pushes its branch;
  then continue here.
- The tree is clean, and the default branch is checked out and current
  (`git fetch` then `git pull --ff-only`). Never carry uncommitted work onto a
  new branch; ask the user to commit or stash.

Done when you are on an up-to-date default branch with a clean tree.

Steps 2 to 4 read and talk; they write nothing. Every file is written in step
5, after the branch exists, so nothing is ever left uncommitted on the default
branch.

## 2. Take in the source

- **A file inside the repo**: it will be referenced by path, as a new entry
  in the `Sources` list of `ROADMAP.md` (S1, S2, ...) if it is not there.
- **Pasted text, or a file outside the repo**: it will be copied verbatim to
  `docs/pairing/sources/NNNN-<slug>.md` with a one-line header (date, where
  it came from), and listed as a source. Future sessions cannot read the chat.
- **The user names a roadmap row** ("the late fees piece"): use its source.

Read the whole source, not only the named part; the piece sits inside the
rest. If this source is new and large, offer once to sketch candidate pieces
as `later` rows for `ROADMAP.md`. On no, carry on with the one piece.

Done when you have read the whole source and know how it will be recorded.

## 3. Ground in the code and the decisions

Read the glossary, the ADR titles (and the full text of any that touch this
piece), the previous slice's `Drift` and `Parked` lists, and the code the
piece will touch. Note every term the piece uses that the glossary defines
differently, and every ADR that constrains it. Done when you can name the
files likely to change and the ADRs that apply.

## 4. Carve

Run the `design-interview` contract (call that skill if installed): one
question per turn, each with a recommendation and its trade-off. Usually two
to five questions, in this order, skipping any the source already answers:

1. **The piece**: quote the source lines it covers. Confirm the boundary.
2. **In and out**: what this slice does not do, especially the tempting
   neighbours. Out-of-slice work becomes `later` rows in `ROADMAP.md`.
3. **Acceptance**: two to five observable checks, each with how it will be
   checked (a test name, a command, a manual action).
4. **First step and mode**: the smallest thing that proves the direction,
   often a single failing test or a walking-skeleton path.

Size test: one PR a reviewer can read in one sitting, three to eight plan
steps. Bigger means split; propose the cut, keep the first part, and put the
rest in `ROADMAP.md`. Done when the acceptance checks are observable and the
plan's step 1 can start right now.

## 5. Write and branch

1. Number the slice: one more than the highest number found under
   `docs/pairing/slices/`, in `ROADMAP.md`, and in slice branch names from
   `git branch -a` (parked slices live only on their branches). Setup is 0000.
2. Create the branch from the agreement's naming, e.g.
   `feat/0003-invoice-totals`. Record `git rev-parse HEAD` of the default
   branch as `base`.
3. Bring the previous slice up to date if `main` still shows it `merging`
   and its PR is merged: its slice file and roadmap row become `merged`.
4. Write the source copy or entry from step 2, any `later` rows, and the
   slice file per MEMORY-BANK.md with `status: building`, the
   applicable ADRs in `adrs`, an empty `Journal` except a first `Decision:
   Slice carved` entry that records the questions asked, the answers, and
   what was cut.
5. Update `ROADMAP.md` (the row's slice number and status) and `STATE.md`
   (active slice, branch, `Phase: building`, next step = plan step 1, the
   previous slice under `Recently shipped`).
6. Commit those memory bank files alone, e.g.
   `chore(pairing): start slice 0003 invoice totals`. The PR will carry its
   own origin story.

Done when the branch exists with that one commit and the tree is clean.

## 6. Hand off

Show the slice in a few lines (goal, acceptance, plan), then call the Skill
tool with `pairing` and propose plan step 1 in its step-loop format.

## Rules

- **Carve, don't design.** Settle only what step 1 needs and what defines
  done. Later questions are answered by building, in the journal.
- **The user's words for the goal.** Quote them where possible.
- **Acceptance must be observable**, each with its check.
- **One active slice.** Park or finish before starting another.
- **The spec is respected or the drift is written down.** If the user wants
  something the source contradicts, record it in the slice's `Drift` and in
  `ROADMAP.md`, and ask whether to update the source in this PR.
