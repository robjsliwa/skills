---
name: vertical-slice-phasing
description: >-
  Decide the build order for an agreed design by interviewing the user one
  sequencing decision at a time, then write phases.md: thin vertical slices,
  walking skeleton first. Use when the user says "phase this," "what do I build
  first," "sequence the work," "build order," "milestones," or hands over a
  draft phase list to pressure-test. Not for the architecture (design-interview)
  or the stories (elaborate-current-phase, to-story).
---

# Vertical-Slice Phasing

Turn a settled design into an implementation order by running `design-interview`
on sequencing decisions only, judging every recommendation by the phasing
heuristics below, and writing the result as a phased design document built from
thin vertical slices.

The product is an order, not an architecture. The design the user hands over is
fixed input; the question this skill answers is in what order to build it so that
every phase ships something usable, the riskiest claim is proven first, and no
phase forces a rewrite of an earlier one.

## The through-line: thin vertical slices, walking skeleton first

One principle shapes every decision. Build a thin vertical slice that runs end to
end before building any layer in full. Phase one exercises the riskiest, most
falsifiable claim in the system on a skeleton; every later phase thickens that
skeleton with usable capability rather than assembling a complete horizontal layer
that only becomes useful once the last one lands.

The failure mode is the horizontal plan: all of storage, then all of auth, then all
of the API, then finally something a user can touch in phase four. Horizontal plans
back-load the falsifiable claims and ship nothing demoable until late. Vertical
slices invert that: each phase is a working product, thinner than the last is wide.

## When this applies (and when it does not)

Use it when the architecture is settled or nearly so and the open problem is
sequencing: what is phase one, where the cut lines fall, what proves the thesis,
what depends on what, what defers. The tell is a user with requirements or design
docs in hand asking about build order, milestones, or "what first," possibly with a
draft phase list to pressure-test.

Do not use it to decide the architecture. If the coupled decisions are about what a
tenant is or where the trust boundary sits, that is `solution-design` with
`design-interview`; do that first, then phase the result. Do not use it to write
stories; that is `elaborate-current-phase`, one phase at a time through `to-story`.

## Run the interview

Invoke `design-interview` and follow its contract unchanged: one decision per turn,
a recommendation every turn, dependency order, explore before asking. What this
skill supplies is the subject, the tree, the judgment, and the document.

**Inputs.** `docs/planning/<slug>/design.md` and the requirements it links (a file
or a tracker issue), plus any `CONTEXT.md` and ADRs in the area. Read all of it
before the first question. Treat the architecture as fixed; when a sequencing
question tempts a redesign, note it under out of scope and stay on sequencing.
While reading, extract four things, because they drive the plan:

- **The core thesis.** The single most novel, riskiest, most falsifiable claim the
  system makes. Phase one must prove it. If there are several, pick the one whose
  failure would most invalidate the project.
- **The requirement ids and acceptance criteria.** The user's own definition of
  done. Every requirement id gets a phase end or an explicit deferral.
- **The load-bearing interfaces and seams.** Where the design has already
  separated concerns. These are what let a thin slice survive its own growth.
- **Constraints and non-negotiables.** Required dependencies, target platforms,
  ordering the domain forces. These prune branches before you walk them.

If the user handed over a draft phase list, read it as their instinct about the
tree, not as the answer. Honor its lineage by showing how your slicing maps back to
it and where you re-cut and why, but re-slice freely.

**The tree.** Set the frame explicitly (architecture fixed, sequencing only), then
map these branches in this order. Everything inherits from the root.

1. **Sequencing philosophy (root).** Vertical walking skeleton versus horizontal
   layers.
2. **The substrate.** What storage, identity, and resolution foundations the first
   running slice sits on, and which must be present, even degenerately, from phase
   one so later phases stay additive.
3. **Capability broadening.** The order the remaining features arrive in, and where
   each cut falls.
4. **Deployment and scale.** When the work targets each runtime environment, and
   how to split "runs there" from "scales there."
5. **Cross-cutting concerns.** Observability, security, and the machine-readable
   contract, woven rather than phased.

**The questions.** Each turn recommends a phase boundary; a bare "where should this
go?" is not a turn. Spend the user's attention only on what needs their judgment:
risk appetite, what counts as the core thesis, where they want value to land
first. A change to one boundary often moves another, so propagate before
continuing.

**The lists.** Carry design-interview's three lists under these names, because
they become the spine of the document: settled phases (each with what it delivers,
one line), deferred and out of scope (including architecture you declined to
reopen), and designed seams (each with the phase that introduces it and what it
enables).

**Stopping.** Done when every branch is resolved or deferred, every requirement id
has a phase or a deferral, and the definition of done maps to phase ends. Recap
the spine and confirm before writing.

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

9. **Map requirements to phase boundaries.** State which phase end satisfies each
   requirement id and acceptance criterion. This anchors the plan to the user's
   definition of done and exposes whether the slicing actually delivers value when
   promised. Write it twice: as a runnable end-to-end script, one line per
   capability, tagged by phase, and as a traceability table, one row per
   requirement id, that to-story later fills with story ids.

10. **Name the designed seams.** Every deferred capability should have the interface
    that will eventually receive it identified and placed in its enabling phase, so
    the deferral is a plug-point rather than a future rewrite. Naming these is often
    the most valuable output of the whole exercise.

## Write the phased design document

Capture the agreed plan as `docs/planning/<slug>/phases.md`, in place of
design-interview's findings document, and present it. Use this structure unless
the domain calls for adapting it:

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
**Status:** planned
[For each phase, in order: what it delivers (the usable capability at its end), why
it sits here (the dependency or risk rationale), its concrete scope, its acceptance
checkpoint, and the seams it establishes or relies on. Mirror the interview order.
The Status line is state for elaborate-current-phase, which flips it to current and
done and appends Drift notes beneath the phase as the build teaches.]

## Definition of done
[An end-to-end script a fresh developer runs after the last phase: clone, build,
then one command per delivered capability, each line tagged with the phase that
makes it pass. This is the concrete form of the acceptance-criteria mapping and the
contract for "shipped". elaborate-current-phase checks a phase's lines before
marking it done.]

## Traceability
[One row per requirement id, in id order. Phase is the phase whose end satisfies
the requirement, or "deferred" with the out-of-scope entry it points to. Leave
Stories empty; to-story fills it with the story ids that serve the requirement
when it explodes that phase. A blank Phase is a gap in the plan. A blank Stories
cell in a current phase is a gap in the elaboration, visible before the phase is
built.]

| Requirement | Phase | Stories |
|---|---|---|
| R1 | 1 | |
| R2 | 3 | |
| R3 | deferred (see Out of scope) | |

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
open. Capture the reasoning, not only the conclusions. Prose over heavy formatting;
lists only for genuine enumerations (a phase scope, the seams). No em dashes.

## Hand off

Commit `phases.md`. The next step is `elaborate-current-phase`, which details the
first phase only, through `to-story`. It is safe to clear context first. Do not
write stories for every phase now; that is the waste this loop exists to avoid.
