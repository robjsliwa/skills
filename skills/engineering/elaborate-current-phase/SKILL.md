---
name: elaborate-current-phase
description: >-
  Detail exactly one phase of a phased design into stories, through to-story,
  leaving later phases as sketches, then re-derive the next phase against the
  real codebase once the current one ships. Use after vertical-slice-phasing,
  when the user says "detail phase 1," "what do I build first," "explode this
  phase," or "now do the next phase." Deliberately refuses to detail phases
  beyond the current one.
---

# Elaborate Current Phase

Progressive elaboration: detail the phase you are about to build, sketch the rest,
and re-derive each next phase only when you reach it, against the code that now
exists. Detailing phase four today is fiction, because building one through three
changes what four should be. The phased design is the map; this skill walks it one
phase at a time, and it is the return arrow that makes the planning loop a loop.

## Inputs

- `docs/planning/<slug>/phases.md` from `vertical-slice-phasing`. If it does not
  exist, stop and phase first.
- `docs/planning/<slug>/design.md` and the requirements it links.
- Existing stories for this feature: files under `docs/planning/<slug>/stories/`,
  or issues in the tracker named by `docs/agents/issue-tracker.md`.
- The codebase, which is the ground truth for every built phase.

## 1. Establish where you are

Every phase in `phases.md` carries a `Status` line: `planned`, `current`, or `done`.
The current phase is the one the user names, otherwise the first phase not marked
done.

- If the current phase already has stories and every one is done (`Status: done`,
  or a closed issue), mark the phase done in `phases.md`; the next planned phase
  becomes current. If the statuses look stale against `git log`, ask before assuming.
- If it has stories and some are still open, report the frontier and stop. There is
  nothing to elaborate yet.
- Built phases are evidence. Read their real ports, adapters, and schema, and note
  what turned out harder or easier than the design assumed.
- Later phases stay at the resolution phasing left them: a named capability, a
  rationale for its position, the seams it plugs into. The urge to detail them is
  the failure mode.

## 2. Reconcile the phase against reality

Before exploding, check the phase against the built code:

- **Seams.** Did a built phase establish the seam this phase needs? Then this phase
  swaps in behind it. Did it fail to, because the design was wrong? Then the first
  story of this phase adds the seam, and that is a finding worth recording.
- **Assumptions.** Has built code invalidated any of this phase's assumptions? Adjust
  the phase's scope in `phases.md` under a `Drift` note: what changed, and why.
- **Reach.** If the drift reaches later phases, say so and recommend re-running
  `vertical-slice-phasing` on the remaining phases before continuing. Do not build to
  a stale map.

## 3. Explode the current phase

Invoke `to-story` with the current phase (its scope, acceptance checkpoint, and
seams), the design doc, and the reconciliation notes. Constrain it to this phase
only. It slices, carries the design into each story, quizzes the user, and publishes.

## 4. Record

In `phases.md`, set this phase's `Status` to `current`, list its story ids beneath
it, and keep the `Drift` notes. Commit.

## Self-check

- [ ] Only the current phase has stories.
- [ ] Later phases remain sketches, untouched.
- [ ] The built phases' real code was read, not just the original design.
- [ ] Every divergence from the phased design is recorded under `Drift`, with its
      cause.
- [ ] If later phases are now invalidated, re-phasing is recommended rather than
      silently building to a stale plan.

## Hand off

Work the frontier with `tdd`, one story per context window, flipping each story to
`done` as it lands. When every story in the phase is done, run this skill again.
Report drift like findings from a build, not an apology: the plan changing as the
code teaches you is the system working.
