---
name: diagnose
description: >-
  A disciplined loop for hard bugs and performance regressions: build a
  feedback loop that goes red on this bug, shrink the repro, rank hypotheses
  and test them one at a time with tagged instrumentation, fix only what the
  evidence confirms, pin it with a regression test, clean up, and record the
  dead ends. Use when a bug survives two guesses, when there is no fast red
  signal, when something got slower, or when the user says "debug this,"
  "why is this failing," "it's flaky," or "this got slow."
argument-hint: "The symptom: an error, a failing test, a slow path, or 'it does X when it should do Y'."
---

# Diagnose

Most debugging time is lost to guessing without a signal: change something,
squint, change something else. This skill refuses to guess until there is a
loop that shows the bug on demand, and refuses to fix until the evidence
says why. Each phase has a gate; do not cross it early.

Read `docs/agents/profile.md` for the fast test command and how to run the
app. If it is missing, use the repo's obvious commands and say once that
`/repo-setup` would make them explicit.

## 1. Build a feedback loop that goes red

Get a command that fails on this bug, every time, in seconds if you can:

- a failing test at the nearest seam that shows the symptom, or
- a script with one clear signal: an exit code, a diff against expected
  output, an assertion, a timing over a threshold.

For a **performance regression**, the loop is a benchmark or a timed script
with a stated threshold, run several times so noise is visible. Record the
baseline: the numbers before the regression (a known-good commit) and now.

For a **flaky** bug, loop the command until it fails (`for i in $(seq 50)`)
and report the failure rate. A rate is a signal; one lucky pass is not.

If the bug only appears in an environment you cannot run, say so, and ask the
user for the narrowest thing they can give: logs, a captured request, a data
sample, or a run of your script on their side.

**Gate:** the loop is red on the bug, and you have shown its real output. No
hypotheses before this.

## 2. Minimise the repro

Shrink the input, the data, the config, and the code path until removing
anything more makes the loop go green. Every cut you make and its result is a
clue. For a regression with a known-good commit, `git bisect run <loop>` often
finishes this phase and the next in one go.

**Gate:** the smallest repro you can get, still red, written down.

## 3. Hypothesise

List two or three hypotheses, ranked by likelihood times cheapness to test.
For each, write what you would expect to observe if it were true and if it
were false. Test **one at a time**, cheapest-likely first.

A hypothesis that cannot be told apart from the others by any observation is
not yet a hypothesis; sharpen it.

## 4. Instrument

Add the narrowest observation that splits the hypothesis: a log line, an
assertion, a timer, a debugger breakpoint. Tag every added line with a unique
marker for this session, e.g. `[DEBUG-7f3a]`, so cleanup is a grep:

```
log.Printf("[DEBUG-7f3a] total before round: %v", total)
```

Run the loop. Record what the hypothesis predicted and what happened. Wrong
hypotheses are not waste: write each one down with the evidence that killed
it before moving to the next.

**Gate:** one hypothesis is confirmed by evidence you have shown: a log line,
a value, a timing. "It's probably X" is not confirmation. No fix before
this.

## 5. Fix

Make the smallest change that addresses the confirmed cause, not the
symptom. Run the loop: it goes green (or the timing drops under the
threshold, across several runs). Then run the fast test command so the fix
broke nothing else.

If the loop stays red, the hypothesis was wrong or incomplete. Revert the
fix, go back to phase 3 with the new evidence.

## 6. Regression test at the right seam

Turn the loop into a permanent test, at the seam where the bug is cheapest to
describe: usually the public boundary a user of the code would call, not the
private function you changed. Confirm it fails without the fix (stash the
fix, run, restore) and passes with it. For a performance bug, a benchmark
with a recorded threshold, or a note of why one is not practical. Follow the
`tdd` skill's naming and seam rules.

## 7. Remove instrumentation

```
grep -rn "DEBUG-7f3a" .
```

Remove every hit, and any scratch scripts that do not become tests. Run the
fast tests once more. **Gate:** the grep returns nothing.

## 8. Record the dead ends

Write a short entry where the next reader will find it:

- **Pairing:** a `Debug: <symptom>` journal entry in the active slice (format
  in `skills/pairing/pairing/MEMORY-BANK.md`).
- **A story:** a `### Debug notes` subsection under the task that hit it.
- **Otherwise:** a section in the PR description.

The entry holds the loop command, the minimal repro, every hypothesis tried
with the evidence for or against it, the cause, and the fix. The wrong
hypotheses answer "why didn't you just..." for the reviewer.

## When to stop and ask the user

- You cannot make a loop go red after a real attempt. Say what you tried and
  what access or data would let you.
- Three hypotheses have died and there is no fresh one that the evidence
  points to. Show the evidence and ask what they know about this area.
- The confirmed cause is a design flaw, a spec question, or sits in code
  outside the change's scope. The fix becomes a decision, not a patch.
- The fix needs something the repo has ruled out (a new dependency, a change
  to a merged migration, a deviation from an ADR).

## Rules

- **No hypothesis before red. No fix before evidence.**
- **One hypothesis at a time**, with its prediction written first.
- **Every debug line is tagged**, and the tag is grepped out before commit.
- **Show real output**, trimmed to the signal. Never "that should fix it."
- **The dead ends are part of the result.** Record them.
