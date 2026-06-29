# [Feature / system name]: Design

**Status:** Draft | Reviewed | Agreed
**Date:** [date]
**Requirements:** [link to the requirements doc / PRD issue this satisfies]
**ADRs:** [links to any docs/adr/ entries this design produced]

One paragraph naming the through-line: the single constraint or principle that shaped
the decisions below. If there is a riskiest claim the design rests on, name it here.

## Decisions at a glance

A numbered list, one line per major decision, each tagged with the requirement ids it
satisfies (R1, R4). This is the executive summary a reviewer skims first and the map
back to the requirements.

## Architecture overview

The shape, described at C4 container and component level, not as a wall of prose.
What are the containers, what are the components inside the one this design touches,
and how do they talk. If a `c4check` contract exists or should exist for this, name
it and note that the design must remain consistent with it.

## Ports

The interfaces the core defines and depends on, listed explicitly. This is a
ports-and-adapters design, so the ports are the spine. For each port: its name, the
single responsibility it abstracts, and the requirement it serves. Define ports
before any adapter that implements one.

- **`PortName`** — what it abstracts, why the core needs it, which R it serves.

## Adapters

The concrete implementations behind each port, one row per adapter. For each: which
port it satisfies, the external thing it adapts (a database, a SIP stack, an HTTP
client, the filesystem), and whether it is MVP or deferred. A port may have a
degenerate adapter now and a real one later; say so, that is a designed seam.

## Deterministic and probabilistic split

The signature decision. State plainly which work is deterministic and belongs in
compiled code or scripts, and which requires judgment and is the only part an agent or
model contributes. Draw the line explicitly. Anything that can be made deterministic
should be, and the document should justify any place where probabilistic behavior sits
on a path that could have been deterministic. This is where this design is graded.

## Domain model

The core types and their relationships. The domain is the center of the hexagon and
knows nothing about adapters. Keep this free of transport, storage, and framework
concerns. If a type here imports an adapter concern, it is in the wrong place.

## Data and persistence

The storage obligations from the requirements made concrete: schema sketch, retention,
and isolation. If multi-tenant, state the isolation mechanism and the rule that keeps
it honest (for example, tenant scoping enforced at the boundary, never by hand-written
predicates in domain code). Encryption and key handling if the requirements demand it.

## Control flow / module pipeline

How a request moves through the system, port to core to port. If the design is a
configurable pipeline of modules, list the modules, their order, and what each may and
may not do. Name the validator-versus-mutator distinction where it applies.

## Concurrency and state

Only if relevant. The concurrency model, what is shared, what is owned, where the
synchronization lives, and what is deliberately stateless. Statelessness, where the
requirements allow it, is a feature; say where it is chosen and why.

## Dependency policy

Stdlib-first. List every external dependency this design introduces and justify each
one in a sentence: what it provides that the standard library does not, and why
writing it is not the better trade. A design that adds dependencies without this
justification is not done. Default to zero new dependencies and defend each exception.

## Testing strategy

How this is proven, table-driven and test-first. Which behavior is tested at the
domain layer with no adapters, which needs an adapter fake, and which needs an
integration test against the real external thing. Map the acceptance criteria from the
requirements to the layer that verifies each. The RED test comes before the code.

## Designed seams (chosen now, built later)

The interfaces placed in this design specifically so a later phase is additive rather
than a rewrite. For each: the seam, what it enables, and the phase expected to fill it.
The test for a safe deferral is whether the later work is a swap behind an existing
port or a rewrite. If it is a rewrite, the seam belongs here, now.

## Trust boundaries and security

Where attacker-controlled data crosses into the system, what is validated at each
boundary, and what the design assumes is trusted. Tie each back to the security
non-functional requirements.

## Observability

What this design makes visible at runtime: the structured events, the metrics, the
spans. Observability is woven into every component, not bolted on, so name what each
component emits rather than deferring it to an ops phase.

## Decisions that became ADRs

Any decision here that is hard to reverse and would surprise a reader without context
gets an ADR under `docs/adr/`. List them with a one-line summary and a link. Do not
write an ADR for reversible or obvious choices; reserve them for the load-bearing,
surprising ones.

## Out of scope (deferred)

What this design deliberately does not address, the boundary, and where it returns.
Feeds the phasing step.
