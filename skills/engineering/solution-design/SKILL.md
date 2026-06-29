---
name: solution-design
description: >-
  Turn an agreed requirements document or PRD into a detailed technical design
  document (the HOW): ports, adapters, the deterministic-versus-probabilistic
  split, domain model, data, seams, and the decisions that become ADRs. Use this
  as the missing step between to-prd and to-issues, whenever the user has
  requirements in hand and is about to break work into issues but there is no
  design artifact yet, or whenever they say "design this," "how should we build
  this," "work out the architecture," or "write the design doc." This is the
  step that stops to-issues from guessing at mechanism. It produces a design,
  not a build order; phasing the design is the next step. For resolving genuinely
  coupled, branching architecture decisions, invoke design-interview from inside
  this skill rather than guessing.
---

# Solution Design

The step the Pocock chain skips. `to-issues` goes straight from PRD to vertical-slice
issues, which is fine for a single thin slice and wrong for anything with real
architectural weight. This skill inserts the design artifact in between, so the issues
inherit a chosen mechanism instead of inventing one per agent.

The output is a design document: how the system is built, expressed in this repo's
conventions. Hexagonal core with explicit ports and adapters, deterministic work in
compiled code and probabilistic judgment fenced off and minimized, stdlib-first with
every dependency justified, table-driven and test-first. The template carries these so
the design is graded against them by construction.

## Precondition: requirements first

Do not design against a vague brief. Confirm an agreed requirements doc or PRD exists
(the output of `write-requirements` / `to-prd`). If it does not, stop and produce it
first; designing without requirements produces a design that satisfies nothing
checkable. Read the requirements in full and carry the requirement ids (R1, R4)
forward so every decision traces back to what it serves.

## Resolve the decisions before writing

A design is a set of resolved decisions. Two ways to resolve them:

- When the decisions are independent or obvious, make them, and record the reasoning.
- When they are coupled and branching, where one choice reshapes the next (what is a
  tenant, what is the trust boundary, what is the data model), invoke `design-interview`
  and walk the tree one decision at a time. Do not guess your way through a coupled
  tree; that is exactly what the interview exists to prevent. Come back here to write
  up the result.

Explore before asking or assuming. Existing ports, adapters, `CONTEXT.md`, and prior
ADRs answer many questions outright and constrain the rest. Read the code.

## Write to the template

Read `assets/design-template.md` and produce a document with every section. The
sections that carry this repo's standards, and where designs usually fail:

- **Deterministic and probabilistic split.** State the line explicitly. Anything that
  can be deterministic should be, in compiled code or a script. Justify any place
  probabilistic behavior sits where determinism was possible. This section is the one
  most worth getting right.
- **Ports before adapters.** Define the interfaces first. An adapter described before
  its port is a sign the core has leaked.
- **Dependency policy.** Default to zero new dependencies. Every external dependency
  gets a one-sentence justification against the standard library. No justification,
  no dependency.
- **Designed seams.** Name the interfaces placed now so a later phase is a swap, not a
  rewrite. This is what makes the phasing step's deferrals safe, so it is the bridge
  to what comes next.
- **Testing strategy.** Map each acceptance criterion to the layer that proves it, RED
  test first.

## ADRs, not prose monuments

When a decision is hard to reverse and would surprise a reader without context, write
an ADR under `docs/adr/` and link it from the design. Do not write ADRs for reversible
or obvious choices. The design doc holds the whole picture; ADRs hold the few
load-bearing, surprising commitments.

## Style

Dry, first-person where natural, prose over bullet salad, no em dashes. Show structure
with a small diagram or a typed interface sketch rather than three paragraphs about it.
A twelve-line Go interface says more than a page of description.

## Self-check

- [ ] Every decision traces to a requirement id.
- [ ] Ports are defined before their adapters.
- [ ] The deterministic / probabilistic line is explicit and defended.
- [ ] Every new dependency is justified against the stdlib, or there are none.
- [ ] Designed seams name what they enable and the phase that fills them.
- [ ] Acceptance criteria are each mapped to a test layer.
- [ ] Hard-to-reverse surprising decisions have ADRs; reversible ones do not.

## Hand off

Commit the design and any ADRs. The next step is `vertical-slice-phasing`, which takes
this design as fixed input and decides the build order. Do not start exploding work
into issues yet; phase first, then elaborate only the first phase.
