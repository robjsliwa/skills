---
name: write-requirements
description: >-
  Turn a finished grilling or design-interview session into a detailed,
  template-driven requirements document (a PRD with teeth), then publish it as
  docs/planning/<slug>/requirements.md or as an issue in the configured
  tracker. Use whenever the user is ready to capture requirements, write a
  PRD, write a spec, or "write up what we just decided," for anything beyond a
  trivial one-slice change. Do not use it to decide the technical approach;
  that is solution-design's job and comes after this.
---

# Write Requirements

Produce a requirements document detailed enough that solution-design and to-story
never have to guess what the system must do. The output is the WHAT and the WHY. It
contains no architecture, no ports, no chosen libraries. Mechanism is the next step.

This skill exists to fix one specific failure: requirements that read fine but are
silent on the dimensions that later force a rewrite. Latency budgets, failure
behavior, trust boundaries, retention, the second caller. The template is the cure,
because it enumerates those dimensions and makes their absence visible.

## Precondition: do not write from a cold start

A good requirements doc is the residue of a good interrogation. Before writing,
confirm the understanding is actually shared:

- If a grilling session (`grill-with-docs` or `grilling`) or a `design-interview`
  already happened in this conversation, use it. The decisions are the raw material.
- If it did not, stop and run the grilling first. Writing requirements from an
  unexamined one-line brief is how thin requirements happen. Say so plainly and
  invoke the interview rather than papering over the gap.
- Explore before asking. Anything answerable from the codebase, the uploads, prior
  ADRs, or `CONTEXT.md` should be read, not asked. Use the glossary's vocabulary.

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

## Self-check before publishing

- [ ] Every section of the template is present and non-empty, or struck with a reason.
- [ ] Every behavioral requirement is single-behavior, numbered, and testable.
- [ ] Every happy-path requirement has a corresponding failure requirement.
- [ ] Non-functional rows are all filled or explicitly struck.
- [ ] Acceptance criteria are checkable and each maps to a requirement id.
- [ ] Out-of-scope items carry the phase or milestone where they return.

## Publish

Read `docs/agents/issue-tracker.md` (written by `setup-matt-pocock-skills`) and
publish where it points:

- **A real tracker** (GitHub, GitLab, Jira, Linear, or a freeform workflow the
  config describes): file the document as one issue, an epic where the tracker has
  them, titled `<Feature>: Requirements`, with the full document as the body. Apply
  the `ready-for-agent` label. Report the issue reference; it is the input to the
  next step.
- **Local markdown, or no config:** save to `docs/planning/<slug>/requirements.md`,
  where `<slug>` is a short kebab-case feature name. Create the folder; the design,
  the phases, and the stories for this feature will live beside it.

Do not paraphrase the document back in chat; the artifact is the deliverable.

## Hand off

Name the next step: `solution-design`, pointed at the requirements (the path or the
issue reference). It is safe to clear context first; everything the next step needs
is in the artifact.
