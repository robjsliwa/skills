# ADR format

An architecture decision record explains one decision to someone who arrives
later and wonders why. ADRs live in `docs/adr/` (or the profile's `Docs / ADRs`)
as `NNNN-slug.md`: a four-digit number, then a short kebab-case slug.

## The bar

Write one only when the decision is all three:

1. **Hard to reverse.** Undoing it means real rework, a migration, or a broken
   contract.
2. **Surprising without context.** A capable newcomer would question it.
3. **A real tradeoff.** A credible alternative existed and lost for stated
   reasons.

Library choices, naming, and anything a refactor can undo in an afternoon
usually do not clear it. When unsure, offer it and let the user decide.

## Numbering

List the folder, take the highest number, add one. Pad to four digits. Never
reuse a number, even for a rejected ADR.

## Template

````markdown
# N. <Decision, stated as a fact>

**Status:** proposed | accepted | superseded by [NNNN](NNNN-slug.md)
**Date:** YYYY-MM-DD

## Context

<The forces at play: what problem, what constraints, what made this a real
choice. Glossary terms. A few short paragraphs at most.>

## Decision

<What was decided, in one or two paragraphs. The alternatives that lost, and why,
in a sentence each.>

## Consequences

- <What gets easier.>
- <What gets harder, or what we now live with.>
- <What would make us revisit this.>
````

Title is the decision ("Tenants share one database"), not the question
("Database per tenant?").

## Optional before/after diagram

When the decision changes a structure, add one small Mermaid diagram in Context
(before) and one in Decision (after), drawn per `visualize`
(the `visualize` skill's `NOTATION.md`), node labels from `GLOSSARY.md`. If the
decision came out of an options block in an `interview`, the chosen option's
diagram goes in Decision and the losing one may stay in Context as the
alternative.

## Supersede, do not edit

An accepted ADR's decision is never rewritten. When a decision changes:

1. Write a new ADR whose Context says what changed and links the old one.
2. Set the old ADR's Status to `superseded by [NNNN](NNNN-slug.md)`. That
   line is the only edit to the old file.

Typos and broken links may be fixed in place.

## Linking

Link ADRs from where the decision bites: the design section, the `CONTEXT.md`
constraint, the story task that relies on it. Relative links.
