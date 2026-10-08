---
name: pair-checkpoint
description: >-
  Save the pairing session to the memory bank so a clean context can resume
  it: catch the journal up, write a session-end entry, rewrite STATE.md, and
  commit (and push) everything on the slice branch, as wip if tests are red.
  Also parks a slice. Use before /clear, when the context is heavy, when the
  user says "let's stop here," "save where we are," "checkpoint," "park this,"
  or when the pairing loop says it is time.
argument-hint: "Optional: 'parked' to park the active slice, or a note on what's in your head."
---

# Pair Checkpoint

A session ends; the work does not. This skill moves everything that lives
only in the chat (the half-finished step, the open question, what the user
was about to try) into the memory bank and git, so `/clear` then `/pair`
resumes exactly here. It is the repo-resident cousin of `handoff`: the next
session reads the memory bank, not a temp file.

Call the Skill tool with `pairing` and read its MEMORY-BANK.md for the
formats.

## Steps

1. **Catch the journal up.** Compare the slice's journal with the chat and
   with `git log $(git merge-base <default> HEAD)..HEAD --no-merges`. Write
   any missing `Step`, `Debug`, or `Decision` entries now, while the reasons
   are still in context. Done when every slice commit and every decision made
   in this session has an entry.

2. **Ask for what is in the user's head**, one question: "Anything you were
   about to try, or worried about, that should go in the notes?" Skip it if
   they passed a note as the argument, or said they are in a hurry.

3. **Write the `Session end` entry**: what was in flight (a half-done step,
   and exactly what remains of it), the state of the tests, the open threads,
   and the user's note.

4. **Rewrite `STATE.md`** per MEMORY-BANK.md: last step, next step and its
   mode, tests at HEAD, open threads, uncommitted work. For `parked`, set the
   slice and its roadmap row to `parked`, `Phase: idle`, write a `Parked`
   journal entry, and say in `Next step` how to unpark ("checkout
   feat/0003-..., then /pair"). The park lives on the slice branch; `pair`
   finds it later through `git branch --no-merged`.

5. **Run the fast tests** so `STATE.md` tells the truth about green or red.

6. **Commit.** Stage the memory bank and any in-flight work by path. Green:
   commit in the agreement's convention. Red, or a step half done: commit as
   `wip: <step title> (red: <one-line reason>)`. If the agreement says the
   user commits, show the message and wait. Done when `git status` is clean.

7. **Push** the slice branch when a remote exists and the agreement says
   checkpoints push (the default; it doubles as a backup). If the branch was
   rebased since its last push, use `git push --force-with-lease`, on the
   slice branch only.

8. **Tell the user** in two lines what was saved and how to resume:
   > Saved on feat/0003-invoice-totals (3a7c0de, green). Next: step 5,
   > reject negative quantities. `/clear`, then `/pair` to pick up here.

   For `parked`, also check out the default branch so the next slice starts
   clean.

## Rules

- **Nothing important stays in the chat.** If the next session would need it,
  it goes in the journal or `STATE.md`.
- **Never commit to the default branch.** With no active slice there is
  nothing to checkpoint; say so and stop.
- **`wip` commits say they are red**, and `STATE.md` says why. They are
  squashed or rewritten at ship time if the agreement's merge strategy asks.
- **Never discard work.** No `reset`, `checkout --`, or `stash drop` without
  an explicit request.
