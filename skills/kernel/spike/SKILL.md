---
name: spike
description: >-
  Answer one technical question by running throwaway code against the real
  thing (library, database, API, hardware), in an isolated worktree, inside a
  timebox, and end with a verdict (Confirmed, Rejected, Partial) and a spike
  brief: evidence, sharp edges, and what the real build should do. Code buys
  knowledge and is never merged. Use when the user says "spike this," "can we
  even," "will it keep up," "does X support Y," "try it quickly," or when
  trailblazer, a spike story, light, pairing, or tdd hit a question that
  reading cannot settle.
argument-hint: "The question to answer, in one sentence."
---

# Spike

**Write code to buy knowledge, never to ship.**

A spike answers one technical question that only running code can settle: will
SQLite FTS5 keep up with our schema, does the vendor's webhook really retry, can
the parser stream a 2 GB file. It is one sitting, one question, one verdict. The
code is the receipt, not the product.

Not a spike: a fact the docs state (`research`), a "how should it look or
behave" question (`prototype`), a choice between known options (`interview`),
or many coupled unknowns (`trailblazer`, which will call this skill for each
technical one).

## 1. Frame

Write the frame before any code, two to four lines, and show it to the user in
one message. If they are not around, write it at the top of the brief and go.

```text
Question:   Can FTS5 return ranked matches across 200k notes in under 100 ms?
Hypothesis: Yes, with the porter tokenizer and a prefix index.
Pass:       p95 under 100 ms on 200k generated notes, ranked by bm25.
Fail:       p95 over 300 ms, or ranking needs a second pass in app code.
Timebox:    one session (about 45 minutes of work); stop at the box.
```

Pass and fail are things you can measure or observe. "Feels fast" is not a
criterion. Anything between pass and fail is Partial.

If the question is really two questions ("can it index fast and rank well"),
split it into two spikes and run the riskier one first.

## 2. Check the dependency

When the spike leans on something outside the repo, spend two minutes on its
health before building on it: latest release and commit dates, whether the docs
cover your case, license, install friction, open issues that describe your
exact problem. A dead or hostile dependency can end the spike early, Rejected,
with that as the evidence.

## 3. Isolate

Never touch the main working tree.

```bash
git worktree add ../<repo>-spike-<slug> -b spike/<slug>
```

If the agent may not write outside the repo (a sandboxed or background agent),
use a git-ignored folder inside it instead: add `.spikes/` to `.gitignore`, then
`git worktree add .spikes/<slug> -b spike/<slug>`. Use the same path in the
clean-up commands below.

Without git, or for a snippet with no repo context, use a scratch directory
outside the repo. Record the branch name (or path) for the brief.

## 4. Build the smallest runnable thing

A script, a single test file used as a harness, one endpoint, a tiny HTML page.
No tests of the spike code, no abstractions, no error handling beyond what lets
it run, hardcode everything the question does not care about. Use the real
dependency, real-shaped data, and real sizes where the question is about
scale. Generate data when real data is private; say how in the brief.

## 5. Stress one edge

Pick the one edge case or failure mode the question cares most about (the empty
input, the huge input, the retry, the concurrent write, the expired token) and
run it. A spike that only tried the happy path has answered half its question.

## 6. Measure

Real commands, real output, kept. Numbers with their units, the machine they
ran on, and how many runs. If you could not run something, the brief says so.

## 7. Verdict

- **Confirmed**: the pass criteria were met, with the evidence.
- **Rejected**: the fail criteria were met, or a blocker appeared. A rejected
  spike that rules out a path is a success; say what it rules out.
- **Partial**: it works with conditions, or the timebox ran out first. Name the
  conditions, or what is left and whether it is worth another box.

At the timebox, stop. Do not extend it silently; a Partial with a clear "what is
left" is worth more than an unbounded spike.

## 8. Brief, then clean up

Write the brief (template below), then:

```bash
git -C ../<repo>-spike-<slug> add -A && git -C ../<repo>-spike-<slug> commit -m "spike: <slug>"
git worktree remove ../<repo>-spike-<slug>
```

The branch stays, unmerged, as the primary source. Push it only if the user
wants it shared. Never merge it; when the real build needs the idea, `tdd`
rewrites it properly, test first.

## Where the brief goes

Inside a trail: `docs/research/<topic>/spikes/<slug>.md`. Otherwise
`docs/spikes/NNNN-<slug>.md` (or the `Spikes:` location in
`docs/agents/profile.md`), numbered after any that exist.

```markdown
# Spike: <the question>

**Verdict:** Confirmed | Rejected | Partial
**Date:** <date>   **Timebox:** <planned> / <used>
**Code:** branch `spike/<slug>` at <sha>
**For:** <the trail node, story, or decision it feeds, linked>

## Frame
<The question, hypothesis, pass, and fail, as written before the code.>

## Evidence
<The commands and their output, trimmed to the signal. Numbers with units,
machine, run count.>

## Sharp edges
<What the docs did not say: undocumented limits, payload quirks, config that
mattered, versions that behave differently.>

## Recommended path
<What the real implementation should do, in a few sentences. What to copy from
the spike (the query shape, the setting that mattered) and what it must not copy
(the hardcoding, the missing error handling).>

## Still open
<What this did not settle, and whether another spike would.>
```

## Hand back

Give the caller the verdict and one line of why. Then feed the result where it
belongs:

- **In a trail:** `trailblazer` updates the node (evidence strength **ran it**)
  and redraws the map.
- **A spike story:** the brief is the story's Demo; mark it done.
- **A decision that clears the ADR bar:** offer an ADR with `glossary`'s format,
  linking the brief.
- **Terms** the spike settled go to `GLOSSARY.md`.
- **A recipe worth reusing** (how to call the API, the setting that made it
  fast): offer to add it to `CLAUDE.md` or a short note under `docs/`, once,
  not as a habit.

## Rules

- **One question, one verdict.**
- **The frame comes first.** A spike with no pass and fail criteria cannot fail,
  so it cannot teach.
- **Isolated, timeboxed, unmerged.**
- **Evidence or it did not happen.** Every claim in the brief points at output.
- **Can run AFK.** When framing needs no judgement from the user (the question
  and criteria are already agreed), a background agent can run the whole spike
  and hand back the brief.
