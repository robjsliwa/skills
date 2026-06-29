---
name: design-interview
description: >-
  Drive a rigorous, one-question-at-a-time interview to nail down a design,
  architecture, plan, proposal, spec, or decision-heavy problem before writing
  anything up, then capture the agreed design in a markdown findings document.
  Use whenever the user hands over a description, requirements doc, RFC,
  proposal, or rough idea and wants to "think it through," "work out the
  requirements," "interview me," "walk the design tree," "nail down the
  approach," "resolve the open questions," or reach shared understanding through
  deliberate Q&A rather than one dump of answers. Trigger it even when the user
  never says "interview" but is clearly facing a branching set of coupled
  decisions (auth and multi-tenancy, data model, API surface, infra topology,
  product scope) and wants them resolved in dependency order with a
  recommendation at each step. Prefer this over answering a design question in
  one shot whenever the space has multiple interdependent decisions best
  resolved one at a time.
---

# Design Interview

A workflow for turning a vague description plus optional attachments into a
fully-resolved design, by interviewing the user relentlessly, one decision at a
time, walking the design tree in dependency order, recommending an answer at
every step, and capturing the result in a findings document.

The value of this skill is discipline. The failure mode it exists to prevent is
the "wall of questions" or the "wall of assumptions": dumping fifteen questions
at once, or guessing at ten decisions and presenting a finished design the user
never got to steer. Real design happens one fork at a time, where each resolved
decision changes what the next question even is.

## When this applies (and when it does not)

Use it when the problem is a **space of coupled decisions**: an architecture, a
multi-tenancy or auth model, a data model, an API contract, an infra topology, a
product scope, a research plan. The tell is that decisions depend on each other,
so the order you resolve them in matters, and a single decision changes the rest
of the tree.

Do **not** use it for a single well-posed question ("which of these two
libraries should I use"), for pure information retrieval, or when the user
explicitly wants a fast one-shot answer. If the user wants you to just decide and
write it up, do that instead. This skill is for when they want to be in the loop
on every fork.

## The contract

Four rules govern every turn. They come straight from what makes these sessions
work, and breaking them is what makes them fail.

1. **One question at a time.** Ask a single coherent decision per turn, then
   stop and wait for the answer. Do not stack a second question "while we're at
   it." Corollaries that depend on the current decision can ride along as "I'll
   formalize this in a later question," but the turn has exactly one headline
   decision the user must rule on.

2. **Recommend, don't just ask.** Every question carries your recommended
   answer, the reasoning behind it, and an honest account of the tradeoff. The
   user should be reacting to a concrete proposal, not generating a design from
   scratch. A bare question wastes their time; the recommendation is the value.

3. **Walk the tree in dependency order.** Resolve the decision that unblocks the
   most downstream decisions next. A decision that everything else inherits from
   (what is a tenant, what is the data model, what is the trust boundary) comes
   before decisions that hang off it. Name where each question sits in the tree
   so the user can see the shape.

4. **Explore instead of asking when you can.** If a question is answerable from
   the attached files, an existing codebase, the prior conversation, or a quick
   search, go find the answer instead of spending the user's attention on it.
   Only ask the user what genuinely needs their judgment or preference.

## Step 0: Ground yourself before the first question

Do not start interviewing cold. First absorb everything already available so you
do not ask about things you could have read.

- Read every attached file in full. The description the user gave you is the
  root of the tree; the attachments are the constraints.
- If there is a codebase (check the uploads directory, the working directory,
  and any path the user named), explore it. Existing patterns, dependencies, and
  prior decisions answer many questions outright and constrain others. When a
  question can be settled by reading code, read the code and state what you
  found rather than asking.
- If the user references prior work ("the approach we discussed," "my usual
  stack"), search past context for it rather than re-asking.
- Note any constraints, non-negotiables, and stated goals. These prune branches
  of the tree before you ever walk them.

If the request is genuinely greenfield with nothing to explore, say so briefly
and move on. Do not invent a codebase to inspect.

## Step 1: Map the tree, then let the user steer

Before the first question, lay out the branches you intend to walk, in the order
you intend to walk them, with a one-line rationale for the ordering (what depends
on what). Keep it short: a paragraph or a compact list of the major nodes.

This does two things. It gives the user a chance to reorder, add a branch you
missed, or cut one that is out of scope. And it sets the expectation that this
will be a sequence of single decisions, not a survey.

Then ask the first question.

## Step 2: Walk the tree, one decision per turn

Each question turn has the same anatomy. Following it consistently is most of the
skill.

- **Name the decision and its place in the tree.** "Question 4: after login,
  what credential does a principal carry?" The user should always know which fork
  they are on.
- **State your recommended answer plainly**, up front, before the reasoning.
- **Give the reasoning**, including the tradeoff and why the alternatives lose.
  Explain it the way you would to a sharp colleague who will push back.
- **Flag the one place they are most likely to disagree.** If there is a sub-fork
  where a reasonable person with different priors would choose differently, name
  it explicitly and invite the override, rather than burying it. This is where
  trust is earned: do not hide the soft spots in your recommendation.
- **End with the explicit decision you want.** Restate, in a sentence or two,
  exactly what you are asking them to accept or change, and pose the sharpest
  version of the open fork.

Keep adjacent decisions from bleeding together. When a downstream concern comes
up mid-question, acknowledge it, say which later question owns it, and move on, so
the current decision stays clean.

### Handle the response, then advance

When the user replies:

- **If they accept**, lock it. Restate what is now settled in a single line, then
  move to the next question. The running record of "what is locked" keeps the
  session coherent over many turns.
- **If they refine or add a constraint** (this is common and good), integrate it,
  and crucially, **propagate it**: check whether their refinement changes any
  decision still downstream, and adjust your planned questions accordingly. Then
  confirm the integration before continuing.
- **If they overrule you**, take it cleanly, fold the new direction in, and follow
  its consequences down the tree. Do not relitigate a decision the user has made.
- **If their answer opens a new branch**, add it to the tree and reorder if it now
  blocks something.

### Track three lists as you go

Carry these forward through the whole interview; they become the spine of the
findings document:

- **Settled:** decisions made, each in a line.
- **Deferred / out of scope:** things deliberately not being decided now, and why.
- **Designed seams:** decisions made specifically to enable future work without
  building it now (an interface left in place, a schema that separates two
  concerns so a later split is additive rather than a rewrite). Naming these is
  often the most valuable output, because they are the difference between a
  design that can grow and one that has to be torn up.

## Step 3: Know when to stop

The interview is done when every branch of the tree is resolved or explicitly
deferred, and no accepted decision has left a dangling dependency. At that point,
recap in one short pass: the tree you walked, and the one or two things left
standing as out of scope. Confirm the user agrees you are done before writing up.

Do not pad the interview with low-value questions to seem thorough, and do not
stop early with open forks still dangling. The right length is however many
decisions the tree actually has.

## Step 4: Write the findings document

Capture the agreed design in a markdown file. Save it to the outputs directory
and present it. Use this structure unless the domain calls for adapting it:

```markdown
# [Subject]: [What was designed]

**Status:** [e.g. Phase 1 design, agreed]
**Date:** [date]
**Scope:** [one or two sentences on what this covers and what it explicitly does not]

[One short paragraph naming the through-line: the single principle or constraint
that shaped the decisions, if there is one.]

## Decisions at a glance
[A numbered list, one line per major decision. This is the executive summary a
reader skims first.]

## [Section per major decision]
[For each, in tree order: the decision, the reasoning, the tradeoff, and any
mechanism or detail agreed. Mirror the order you interviewed in. Fold in the
"designed seam" notes where they belong.]

## Designed seams (not built now)
[Interfaces and shapes chosen now so later work is additive. State what each
enables.]

## Out of scope
[What was deliberately not decided, and the boundary line, so the next
conversation knows where to pick up.]

## Open questions / notes
[Anything unresolved, plus notes that clarify a subtlety the decisions imply but
do not state outright.]
```

The document should let someone who was not in the room understand not just what
was decided but why, and what was deliberately left open. Capture the reasoning,
not only the conclusions; the reasoning is what makes the decisions defensible
later.

## Conventions

- **Always provide a recommendation, even under uncertainty.** "I'm not sure, what
  do you think" is not a turn. If you are genuinely torn, recommend the option you
  lean toward and explain what would change your mind.
- **Be honest about tradeoffs and soft spots.** The recommendation is more useful
  when its weaknesses are visible. Surfacing where the user might reasonably
  overrule you is a feature, not a hedge.
- **Match the user's depth.** Mirror their technical level and vocabulary. If they
  go deep, go deep; if they keep it high-level, do too.
- **Default to prose over heavy formatting** in your questions and in the findings
  document. Use lists only where a genuine enumeration (a role set, a list of
  seams) is clearer as a list. Avoid em dashes.
- **Stay in scope.** When the user has drawn a boundary (one angle of a larger
  problem), hold it. Note where the other side of the boundary lives and defer it
  rather than drifting across.
