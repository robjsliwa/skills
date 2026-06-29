---
name: vertical-slice-phasing
description: >-
  Turn agreed requirements, an architecture, or a stack of design docs into a
  phased implementation design document built from thin vertical slices, by
  grilling the user one sequencing decision at a time. Use whenever someone
  hands over requirements or finished designs and wants to figure out what to
  build first, phase the work, sequence it into milestones, work out a build
  order, or reach a walking-skeleton-first roadmap where each phase ships usable
  functionality and founds the next. Trigger even when the user just asks "how
  should I build this" or proposes their own phase list and wants it
  pressure-tested. This decides BUILD ORDER, not the architecture (use
  design-interview for that) and not mechanically exploding a proposal into
  story files (use phased-implementation-plan for that). Prefer it whenever the
  architecture is mostly settled and the open question is how to slice it into
  phases that each prove something and stay additive.
---

# Vertical-Slice Phasing

A workflow for turning settled requirements into a phased implementation design,
by interviewing the user relentlessly about sequencing, one decision at a time,
walking the phase tree in dependency order, recommending a slicing at every step,
and capturing the result in a phased design document built from thin vertical
slices.

The product of this skill is an implementation order, not an architecture. It
assumes the architecture is mostly decided (the requirements or design docs the
user hands over are the fixed input) and answers a different question: in what
order do we build it so that every phase ships something usable, the riskiest
claim is proven first, and no phase forces a rewrite of an earlier one.

## The through-line: thin vertical slices, walking skeleton first

One principle shapes every decision this skill makes. Build a thin vertical slice
that runs end to end before building any layer in full. The first phase should
exercise the riskiest, most novel, most falsifiable claim in the whole system,
proving it on a skeleton, and every later phase should thicken that skeleton with
usable capability rather than assembling complete horizontal layers that only
become useful once the last one lands.

The failure mode this exists to prevent is the horizontal plan: build all of
storage, then all of auth, then all of the API, then finally something a user can
touch in phase four. Horizontal plans back-load the falsifiable claims and ship
nothing demoable until late. Vertical slices invert that: each phase is a working
product, thinner than the last is wide.

## When this applies (and when it does not)

Use it when the architecture is settled or nearly so and the open problem is
**sequencing**: what is phase one, where do the cut lines fall, what proves the
thesis, what depends on what, what defers. The tell is that the user has
requirements or design docs in hand and is asking about build order, milestones,
or "what first," possibly with a draft phase list they want pressure-tested.

Do not use it to decide the architecture itself. If the coupled decisions are
about what a tenant is, what the data model is, or what the trust boundary is,
that is `design-interview`'s job; do that first, then phase the result with this.
Do not use it to mechanically explode a finished plan into per-task story files
for an agent to execute; that is `phased-implementation-plan`. This skill sits
between them: the design is agreed, and you are deciding the order and the slices,
through an interview, producing a design document a human reads.

## The contract

Four rules govern every turn. They are what make the interview work, and breaking
them is what makes it fail.

1. **One sequencing decision at a time.** Ask a single coherent phasing decision
   per turn, then stop and wait. Do not stack a second decision "while we're at
   it." Corollaries that depend on the current decision can ride along flagged as
   "I'll pin this in a later question," but the turn has exactly one headline the
   user must rule on.

2. **Recommend a slicing, do not just ask.** Every turn carries your recommended
   phase boundary, the reasoning, and an honest account of the tradeoff. The user
   reacts to a concrete proposal. A bare "where should this go?" wastes their
   attention; the recommendation is the value.

3. **Walk the phase tree in dependency order.** Resolve the decision that unblocks
   the most downstream decisions next. The sequencing philosophy (vertical versus
   horizontal) is the root, because it reshapes the entire list. Then the
   substrate everything sits on, then capability broadening, then deployment and
   scale, then the cross-cutting concerns. Name where each question sits so the
   user sees the shape.

4. **Explore the requirements instead of asking.** Anything answerable from the
   handed-over docs, an existing codebase, or prior conversation, go find it.
   Spend the user's attention only on what needs their judgment: risk appetite,
   what counts as the core thesis, where they want value to land first.

## Step 0: Absorb the requirements before the first question

Do not start cold. Read every requirements and design document in full. Treat the
agreed architecture as fixed input you will not reopen; if you find yourself
wanting to relitigate a design decision, stop, note it as an out-of-scope
boundary, and stay on sequencing. While reading, extract four things, because they
drive the whole plan:

- **The core thesis.** The single most novel, riskiest, most falsifiable claim the
  system makes. This is what phase one must prove. If there are several, pick the
  one whose failure would most invalidate the project.
- **The acceptance criteria.** The user's own definition of done, including any
  milestones. You will map these to phase boundaries at the end.
- **The load-bearing interfaces and seams.** The places the design has already
  separated concerns (a repository interface, a provider seam, a policy interface).
  These are what let a thin slice survive its own growth.
- **Constraints and non-negotiables.** Required dependencies, target platforms,
  hard ordering forced by the domain. These prune branches before you walk them.

If the user handed over a draft phase list, read it as their instinct about the
tree, not as the answer. You will honor its lineage and show how your slicing maps
back to it, but you are free to re-slice.

## Step 1: Map the phase tree, then let the user steer

Before the first question, set the frame explicitly: the architecture is fixed
input, and the interview is only about sequencing. Then lay out the branches you
intend to walk, in order, with a one-line rationale for the ordering. Keep it to a
short paragraph or compact list of the major forks. A typical tree:

1. **Sequencing philosophy (root).** Vertical walking skeleton versus horizontal
   layers. Everything inherits from this.
2. **The substrate.** What storage, identity, and resolution foundations the first
   running slice sits on, and which of them must be present (even degenerately)
   from phase one so later phases stay additive.
3. **Capability broadening.** The order the remaining features arrive in, and where
   each cut falls.
4. **Deployment and scale.** When the work targets each runtime environment, and
   how to split "runs there" from "scales there."
5. **Cross-cutting concerns.** Observability, security, and the machine-readable
   contract, woven rather than phased.

This lets the user reorder, add a branch you missed, or cut one out of scope, and
sets the expectation that this is a sequence of single decisions, not a survey.
Then ask the first question.

## Step 2: Walk the tree, one phasing decision per turn

Each turn has the same anatomy. Following it consistently is most of the skill.

- **Name the decision and its place in the tree.** "Question 3: where does real
  authentication turn on relative to the first running feature?"
- **State your recommended slicing plainly**, up front, before the reasoning.
- **Give the reasoning**, including the tradeoff and why the alternatives lose.
  Explain it to a sharp colleague who will push back.
- **Flag the soft spot.** Name the one place a reasonable person with different
  priors would slice differently, and invite the override, rather than burying it.
  This is where trust is earned.
- **End with the explicit decision you want**, posed as the sharpest version of the
  open fork.

When the user accepts, lock it and restate the settled phase in one line. When they
refine or overrule, fold it in and propagate: a change to one phase boundary often
moves another, so adjust the planned questions before continuing. Do not relitigate
a locked decision.

## The phasing heuristics

These are the reusable judgments that turn a pile of requirements into a good slice
order. Lean on them when forming each recommendation.

1. **Walking skeleton over horizontal layers.** Phase one is a thin end-to-end
   slice that exercises the core thesis. Resist completing any single layer before
   something runs end to end.

2. **Every phase ships usable, demoable functionality** and founds the next. If a
   phase produces only internal scaffolding nobody can exercise, it is a layer, not
   a slice. Fold it into a slice, or justify it explicitly as a hard dependency that
   unblocks the next usable thing.

3. **Make the skeleton survive its growth.** Identify the load-bearing interfaces
   later phases will need and put them in the first slice, even if they operate
   degenerately (a tenant-scoped repository with one constant tenant, a resolver
   seam with one implemented target). The test for whether a deferral is safe: when
   the later phase arrives, is it a swap behind an existing interface, or a rewrite?
   If it is a rewrite, the seam belongs in the earlier phase.

4. **Couple decisions that share an enabling dependency.** If B cannot be meaningful
   without A (real tenancy needs a real principal needs authentication), they belong
   in one phase. Do not split them just to make phases smaller; a phase that ships a
   half-working state is worse than a larger coherent one.

5. **Defer the most independent, most externally-coupled work to the end.** A
   capability with no downstream dependents and a dependency on something external
   (a third-party identity provider, an outside service) is the most floatable.
   Pushing it late keeps earlier phases free of that dependency and matches the
   logic of "add the enterprise upgrade once the platform works."

6. **Split a phase when it bundles two distinct falsifiable claims.** "Runs on the
   cloud" is often two claims: "the same artifact resolves to the target's managed
   services" and "the topology splits and scales out." De-risk them in order, on
   separate phases, instead of proving both at once and not knowing which broke.

7. **Order by dependency first, then by risk.** Among phases with no hard
   dependency between them, sequence the one that de-risks the core thesis earlier.
   And put the foundational or security phase before the thing that depends on it
   being trustworthy (an audit trail and a hardened secret model before running
   arbitrary user code on top).

8. **Weave cross-cutting concerns; do not phase them.** Observability, structured
   errors, the machine-readable contract: establish a floor in phase one and have
   each phase carry its own. A dedicated "observability phase" implies every earlier
   phase shipped something un-verifiable, which contradicts the thin-slice
   discipline that each phase be demoable on the day it lands.

9. **Map acceptance criteria to phase boundaries.** State which phase end satisfies
   each acceptance criterion. This anchors the plan to the user's definition of done
   and exposes whether the slicing actually delivers value when promised.

10. **Name the designed seams.** Every deferred capability should have the interface
    that will eventually receive it identified and placed in its enabling phase, so
    the deferral is a plug-point rather than a future rewrite. Naming these is often
    the most valuable output of the whole exercise.

## Track three lists as you go

Carry these forward through the interview; they become the spine of the document.

- **Settled phases:** each phase and what it delivers, one line.
- **Deferred / out of scope:** what is deliberately not in the plan, and the
  boundary line, including architecture decisions you declined to reopen.
- **Designed seams:** interfaces placed in an early phase specifically so a later
  phase is additive, each noted with which phase introduces it and what it enables.

## Step 3: Know when to stop

The interview is done when every branch is resolved or explicitly deferred and no
accepted decision has left a dangling dependency. Recap in one short pass: the
phase spine you walked, the acceptance criteria mapped to phase ends, and the one
or two boundaries left standing as out of scope. Confirm the user agrees you are
done before writing up. Do not pad with low-value questions, and do not stop with
open forks dangling. The right length is however many sequencing forks the tree
actually has.

## Step 4: Write the phased design document

Capture the agreed plan in a markdown file, save it to the outputs directory, and
present it. Use this structure unless the domain calls for adapting it:

```markdown
# [Subject]: Phased Implementation Design

**Status:** [e.g. Phase 1 plan, agreed]
**Date:** [date]
**Scope:** [What this sequences and what it explicitly does not. State that the
upstream architecture is fixed input and this document decides build order only.]

[One short paragraph naming the through-line: the core thesis the plan front-loads,
and the walking-skeleton philosophy that shapes the cuts.]

## Decisions at a glance
[Numbered list, one line per phase plus the key cross-cutting calls. The executive
summary a reader skims first.]

## How to read this plan
[The sequencing philosophy in prose: prove the thesis early, make the skeleton
survive its growth, keep every phase independently usable and verifiable. This is
where the reasoning behind the order lives.]

## Phase-wide foundations
[The load-bearing interfaces and the cross-cutting floor established in phase one
and required of every phase after. The spine that keeps later phases additive.]

## Phase 1..N: [name per phase]
[For each phase, in order: what it delivers (the usable capability at its end), why
it sits here (the dependency or risk rationale), its concrete scope, its acceptance
checkpoint, and the seams it establishes or relies on. Mirror the interview order.]

## Cross-cutting concerns
[Observability, security, contracts: the floor and how each phase carries its own,
with the reasoning for weaving rather than phasing.]

## Designed seams (chosen now, built later)
[Each interface, the phase that introduces it, and what later work it enables.]

## Out of scope
[What the plan deliberately omits, including architecture left unreopened, and the
boundary so the next conversation knows where to pick up.]

## Open questions and notes
[Anything unresolved, the phase count rationale if it diverges from the user's
draft, and a mapping back to any original phase proposal the user gave so the
lineage is visible.]
```

The document should let someone who was not in the room understand not just what
order was chosen but why, what each phase proves, and what was deliberately left
open. Capture the reasoning, not only the conclusions.

## Conventions

- **Always recommend, even under uncertainty.** "I'm not sure, what do you think"
  is not a turn. If torn between two slicings, recommend the one you lean toward and
  say what would change your mind.
- **Be honest about soft spots.** Surfacing where the user might reasonably re-slice
  is a feature, not a hedge. The recommendation is more useful when its weaknesses
  are visible.
- **Honor the user's draft.** If they proposed a phase list, show how your slicing
  maps back to it and where you re-cut and why, so they see the lineage rather than
  feeling overridden.
- **Hold the architecture boundary.** When a sequencing question tempts a redesign,
  note it and defer it; do not drift into reopening settled decisions.
- **Match the user's depth**, and default to prose over heavy formatting in both the
  questions and the document. Use lists only for genuine enumerations (a phase
  scope, the seams). Avoid em dashes in the written document.
