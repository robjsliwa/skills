# Decide: the decision tree and the findings document

Decide is for a space of **coupled decisions**: an architecture, a tenancy or
auth model, a data model, an API contract, an infra topology, a product scope, a
research plan. The tell is that one decision changes the rest, so order matters.

## Mapping the tree

Before the first question, list the decisions as nodes and order them by what
inherits from what. Root decisions are the ones everything else assumes:

- what the core thing is (a tenant, an account, a document);
- where the trust boundary sits;
- the shape of the data;
- what is synchronous and what is not.

Leaves hang off them: naming, retry counts, pagination, error shapes. Name the
order and the one-line reason. A decision that turns out to block an earlier one
moves up; say so when you reorder.

Structural forks (two or three shapes, not settings) become option turns with an
options block. A tree that is mostly structural also earns a "show, then ask"
turn after the root decisions, so the user sees the shape they have chosen
before the leaves.

## Writing the findings document

When another skill invoked the interview, hand back the three lists and the
reasoning and let it write its own document. Otherwise write
`docs/planning/<slug>/findings.md` (planning root from the profile) and present
it. Adapt the sections when the domain calls for it.

```markdown
# <Subject>: <what was decided>

**Status:** <e.g. agreed>
**Date:** <date>
**Scope:** <one or two sentences: what this covers and what it does not>

<One short paragraph: the through-line, the single principle or constraint that
shaped the decisions, if there is one.>

## Decisions at a glance
1. <one line per major decision>

## <One section per major decision, in tree order>
<The decision, the reasoning, the tradeoff, and any mechanism agreed. Include the
chosen option's diagram where one was drawn. Fold in designed-seam notes where
they belong.>

## Designed seams (not built now)
<Interfaces and shapes chosen now so later work is additive. What each enables.>

## Out of scope
<What was deliberately not decided, and the boundary line.>

## Open questions / notes
<Anything unresolved, and subtleties the decisions imply but do not state.>
```

A reader who was not in the room should learn what was decided, why, and what
was left open. Keep the reasoning; it is what makes a decision defensible later.

Every diagram in the document is a Mermaid block drawn per `visualize`, with
glossary terms as node labels. Any decision that clears the ADR bar
(the `glossary` skill's `ADR-FORMAT.md`) is also offered as an ADR, linked from
its section.
