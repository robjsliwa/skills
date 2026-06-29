---
name: write-requirements
description: >-
  Turn a finished grilling or design-interview session into a detailed,
  template-driven requirements document (a PRD with teeth), then hand it to
  to-prd to file in the issue tracker. Use this whenever the user is ready to
  capture requirements, write a PRD, write a spec, or "write up what we just
  decided," and especially when they feel their requirements come out too thin
  or get handed to to-issues underspecified. Use it before to-prd, not instead
  of it: this skill produces the body, to-prd files it. Trigger it even when the
  user just says "write the PRD" or "capture the requirements" for anything
  beyond a trivial one-slice change. Do not use it to decide the technical
  approach; that is solution-design's job and comes after this.
---

# Write Requirements

Produce a requirements document detailed enough that solution-design and to-issues
never have to guess what the system must do. The output is the WHAT and the WHY. It
contains no architecture, no ports, no chosen libraries. Mechanism is the next step.

This skill exists to fix one specific failure: requirements that read fine but are
silent on the dimensions that later force a rewrite. Latency budgets, failure
behavior, trust boundaries, retention, the second caller. The template is the cure,
because it enumerates those dimensions and makes their absence visible.

## Precondition: do not write from a cold start

A good requirements doc is the residue of a good interrogation. Before writing,
confirm the understanding is actually shared:

- If a grilling session (`grill-me`) or a `design-interview` already happened in this
  conversation, use it. The decisions are the raw material.
- If it did not, stop and run the grilling first. Writing requirements from an
  unexamined one-line brief is how thin requirements happen. Say so plainly and
  invoke the interview rather than papering over the gap.
- Explore before asking. Anything answerable from the codebase, the uploads, prior
  ADRs, or `CONTEXT.md` should be read, not asked.

## Write to the template, fill every section

Read `assets/requirements-template.md` and produce a document with every section
present. The discipline is in the sections you are tempted to skip:

- **Non-goals** are mandatory. If you cannot name what this is not, scope is still
  infinite and the requirements are not done.
- **Non-functional requirements** has a row per dimension. Fill each or strike it with
  a stated reason. A blank, silent row is the bug this skill exists to catch. For
  anything in a call path, the latency window is not optional.
- **Edge cases and failure modes** must be a real list. For every happy-path
  requirement, ask what its failure requirement is.
- **Acceptance criteria** are checkable, each tied to a numbered requirement. "It
  works" is not a criterion; "`centon validate` rejects an unsigned INVITE with a 4xx
  and a structured reason" is.

Keep behavioral requirements numbered (R1, R2, ...) so the design, the phasing, and
the stories can all reference them by id. That id is the thread that runs through the
whole loop.

## Style

Match the house style: first-person where natural, dry, prose over bullet salad, no
em dashes. Requirements are terse and declarative. Use "shall" for obligations. State
the observable outcome, never the mechanism. If you find yourself writing how, you
have drifted into the design; cut it and note it for solution-design.

## Self-check before handing off

- [ ] Every section of the template is present and non-empty, or struck with a reason.
- [ ] Every behavioral requirement is single-behavior, numbered, and testable.
- [ ] Every happy-path requirement has a corresponding failure requirement.
- [ ] Non-functional rows are all filled or explicitly struck.
- [ ] Acceptance criteria are checkable and each maps to a requirement id.
- [ ] Out-of-scope items carry the phase or milestone where they return.

## Hand off

Save the document, then invoke `to-prd` to file it in the configured issue tracker so
it lives where the rest of the chain expects it. Do not also paraphrase it back in
chat; the document is the artifact. The next step is `solution-design`, which turns
this WHAT into a HOW.
