---
name: pairing
description: >-
  Pair-program the active slice one small step at a time: agree the step,
  build it in the chosen mode (driver, navigator, ping-pong, dictation), prove
  it with a run, journal the why, commit on green. Also holds the memory bank
  formats every pair-* skill writes. Use when pairing on a slice, when the
  user says "let's pair," "you drive," "I'll write this one," "write exactly
  this," "ping-pong," or when another pair-* skill hands off to the loop.
---

# Pairing

The planning loop decides the whole feature up front. Pairing decides one step
at a time. The user reads the spec, we agree one small piece of it (a
**slice**), and then work the slice in **steps**: each one observable change,
a few minutes of work, proven by a run before the next one is discussed. Two
people at one keyboard: whoever is not typing is navigating.

Everything that matters is written to the **memory bank** under
`docs/pairing/` as it happens, so a fresh session can pick up mid-slice with
`/pair`, and the slice's journal becomes the rationale section of its PR.

Reference beside this file:

- [MEMORY-BANK.md](MEMORY-BANK.md): the layout and the format of every file
  under `docs/pairing/` (STATE, ROADMAP, slice file, journal entries). Read it
  before writing any of them, from any pair-* skill.

`docs/pairing/WORKING-AGREEMENT.md` outranks this skill. Its commands, git
flow, coding style, and pairing preferences apply as written. If it does not
exist, stop and hand off to `pair-setup`.

## Orient (once per session)

Read `WORKING-AGREEMENT.md`, `STATE.md`, the active slice file in full,
`GLOSSARY.md` (or `CONTEXT.md` if that is what the repo uses), every ADR the
slice lists, then run `git status` and `git log <base>..HEAD --oneline`
(`<base>` as MEMORY-BANK.md defines it). If you
arrived through `pair`, this is already done. Done when you can state the slice
goal, the last journaled step, and the next planned step in three lines.

## Modes

| Mode | Who types | The agent's job | The user says |
|---|---|---|---|
| **driver** | agent | Write exactly the agreed step and nothing more; show the diff | "you drive," "go" |
| **navigator** | user | Wait for "done," then re-read the files from disk, run the proof, spot bugs, suggest. Never edit the files they are working in | "I'll write it," "let me drive" |
| **ping-pong** | alternating | One side writes the failing test, the other makes it pass; swap each step | "ping-pong," "you write the test" |
| **dictation** | agent, verbatim | Type exactly what the user dictates. Raise a concern only if it will not compile or contradicts the slice, and ask before deviating by a single token | "write exactly," a pasted code block |

The default comes from the working agreement. The user can switch on any step;
follow the switch without comment and record the mode in the journal entry.

## The step loop

1. **Propose.** One step: what changes, in which file, which run proves it (a
   test name, a command, or a manual check the user performs), and the mode.
   Two to four lines. If the user already said what to do, restate it in one
   line and go. Done when the user agrees or redirects.

2. **Build** in the mode. As driver, write the smallest diff that makes the
   proof pass. Anything else worth changing goes on the slice's `Parked` list
   and is mentioned in one line, not done. As navigator, wait for "done," then
   read the changed files fresh. Done when the change is on disk.

3. **Prove.** Run the step's proof, then the fast test command from the
   working agreement. Show the real output trimmed to the signal. An expected
   red (test written first) counts as proof. Done when the run shows what the
   step promised, or a failure is in front of you.

4. **Debug** when the run surprises you. Read the error, state one
   hypothesis, test it. After two wrong hypotheses, or when there is no fast
   red signal, say so and call the Skill tool with `diagnosing-bugs` if it is
   installed, starting from its feedback loop. Tag any debug logging with a
   `[DEBUG-xxxx]` prefix and grep it out before committing. Journal the dead
   ends; the wrong hypotheses are the most valuable part for the PR reader.

5. **Journal.** Append an entry to the slice's `Journal` per MEMORY-BANK.md:
   what, why, how, evidence, what was considered. Write it now; the why is
   gone an hour later. Done when the entry is on disk.

6. **Commit on green.** Tick the step in the slice's `Plan`, update `Last
   step` and `Next step` in `STATE.md`, stage this step's files by path plus
   the memory bank, glossary, and ADR files the step touched, and commit in
   the agreement's convention, with
   the one-line why in the body. If the agreement says the user commits,
   propose the message and wait. Done when `git status` is clean, or shows
   only files the user is deliberately holding back.

7. **Next.** Propose the next step from the plan. When every plan step is
   ticked, run each acceptance check; when they pass, say the slice looks
   ready and suggest `/pair-ship`.

A refactor is its own step, green before and green after, with its own commit.
A step that turns out bigger than proposed gets split: commit what is green,
re-plan the rest as new plan lines, tell the user.

## Decisions as they happen

- **A term gets settled.** Update the glossary in place, in the
  `domain-modeling` format (call that skill if it is installed). Challenge a
  term that conflicts with the glossary the moment it is used.
- **A decision clears the ADR bar**: hard to reverse, surprising without
  context, and the result of a real trade-off. Offer an ADR in one line. On
  yes, write it on this branch so it ships with the PR, add its number to the
  slice's `adrs`, and link it from the journal entry.
- **Code and an ADR or the spec disagree.** Stop and raise it. Three ways out:
  change the code, supersede the ADR with a new one, or record spec drift in
  the slice's `Drift` section and in `ROADMAP.md`. The user picks.
- **New scope appears.** `Parked` in the slice, or a new line in `ROADMAP.md`
  if it belongs to a later piece.

## Context health

Pairing spends context fast. After about a dozen steps, when the context is
visibly heavy, or when the user says they are stopping, call the Skill tool
with `pair-checkpoint`. The state lives on disk, not in the chat, so `/clear`
and `/pair` cost nothing.

## Rules

- **The agreed step is the whole step.** Never run ahead to the next one.
- **The disk is ground truth.** Re-read a file before editing it; the user
  may have changed it between turns.
- **Their hands, their files.** In navigator mode, suggest in chat; the user
  edits. If they ask you to make one change for them, make that one change
  and journal it as written by the agent.
- **Dictation is verbatim.**
- **Nothing is claimed without a run.** "That should work" is not evidence.
- **Journal, then commit.** Commits happen on green, on the slice branch
  only. The only red commit is a checkpoint's `wip`, and it says so.
- **Silence is drift.** A disagreement with the spec, an ADR, or the
  agreement is spoken, then recorded.

## Self-check after each step

- [ ] The diff contains only the agreed step (plus memory bank updates).
- [ ] The proof ran, and its real output was shown.
- [ ] The journal entry exists and says why, not only what.
- [ ] Plan tick and `STATE.md` match the commit.
- [ ] No `[DEBUG-` tags remain in the tree.
