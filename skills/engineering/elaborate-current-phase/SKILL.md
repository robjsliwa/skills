---
name: elaborate-current-phase
description: >-
  Detail exactly one phase of a phased design down to implementable stories or
  issues, leaving later phases as sketches, then re-derive the next phase against
  the real codebase once the current one ships. Use this after vertical-slice-phasing
  has produced a phased design, whenever the user is about to break a multi-phase
  plan into stories or issues, or says "detail phase 1," "what do I build first,"
  "explode this phase," or "now do the next phase." This is the fix for plans that
  over-specify future work that gets thrown away. It deliberately refuses to detail
  phases beyond the current one. Also use it as the re-entry point: when a phase is
  done, invoke it again to elaborate the next phase using what the finished code now
  teaches. Pairs with phased-implementation-plan or to-issues, which it calls to do
  the actual exploding.
---

# Elaborate Current Phase

The discipline this skill enforces is progressive elaboration: detail the phase you are
about to build, sketch the rest, and re-derive each subsequent phase only when you
reach it, against the codebase that now exists. Detailing phase four today is waste,
because building phases one through three will change what phase four should be. The
phased design from `vertical-slice-phasing` is the map; this skill walks it one phase
at a time.

## Why detailing everything up front is wrong

A phased plan that explodes all phases into stories at once produces two failures. The
early stories are good and get built. The late stories are guesses written before the
code that informs them existed, and they are quietly rewritten or abandoned when their
phase arrives. The effort spent detailing them was spent on fiction. The fix is to
treat each phase boundary as a planning checkpoint, not just a build checkpoint.

## Establish where you are

A phased design has N phases. Determine the current phase: the first unbuilt one, or
the one the user names. Everything before it is built and is now evidence. Everything
after it stays a sketch.

- **Built phases** are inputs. Their real ports, real adapters, real schema, and the
  things that turned out harder or easier than the design assumed are the most valuable
  information you have. Read the code, not just the original design.
- **The current phase** is what you elaborate, fully, now.
- **Later phases** stay at the resolution `vertical-slice-phasing` left them: a named
  capability, a rationale for its position, and the seams it will plug into. Do not
  elaborate them. If you feel the urge, that urge is the failure mode.

## Elaborate the current phase

Hand the current phase, plus the design doc, plus the actual state of the built
phases, to `phased-implementation-plan` (for a story-file bundle) or `to-issues` (to
file vertical-slice issues in the tracker). Constrain it to this phase only. The result
is the same quality of detail your existing skills already produce: one-PR stories,
front-loaded contracts, RED-first test plans, verification commands, explicit
out-of-scope per story. The only change is scope: one phase, not all of them.

Before exploding, reconcile the phase against reality:

- Did a built phase establish a seam this phase was going to need? Good, this phase
  swaps behind it. Did it fail to, because the design was wrong? Then the first story
  of this phase is to add the seam, and that is a finding worth noting.
- Has anything in the built code invalidated this phase's assumptions? If so, this is a
  correct-course moment. Adjust the phase's scope and say what changed and why, rather
  than building to a plan reality already overtook.

## The re-derive entry point

When a phase finishes, do not reach for the next batch of pre-written stories, because
there are none, by design. Invoke this skill again. It will:

1. Read the finished phase's actual code as the new ground truth.
2. Pull the next phase's sketch from the phased design.
3. Re-derive that sketch into detailed stories against the code that now exists,
   adjusting scope for what the previous phase taught.
4. Note any drift from the original phased design, and if the drift is large enough to
   change later phases, say so and recommend re-running `vertical-slice-phasing` on the
   remaining phases rather than limping forward on a stale map.

This loop, elaborate then build then re-derive, is the whole point. Each pass is cheap
because it only ever details one phase, and each pass is informed because it runs after
the previous phase is real.

## Self-check

- [ ] Only the current phase has been elaborated to story or issue level.
- [ ] Later phases remain sketches, untouched.
- [ ] The elaboration used the built phases' real code, not just the original design.
- [ ] Any divergence from the phased design is named, with its cause.
- [ ] If later phases are now invalidated, re-running the phasing step is recommended
      rather than silently building to a stale plan.

## Style

Dry, prose over bullets, no em dashes. When you report drift, report it like findings
from a build, not an apology. The plan changing as the code teaches you is the system
working, not a mistake.
