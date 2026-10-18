---
name: light
description: >-
  Take one coherent change from idea to built code with the least ceremony that
  still works: a short align interview, one story a person can see (with its
  own small design in its tasks), then tdd or code-along. Escalates to the full
  loop when the change turns out to carry real design weight. Use when the user
  says "quick change," "small feature," "just this one thing," runs /light, or
  when start recommends the light loop.
disable-model-invocation: true
argument-hint: "The change, in a sentence."
---

# Light

The full loop earns its cost when the architecture is the hard part. Most changes
are not like that: one slice, no real design choice, done in a story or two. The
light loop keeps the parts that make those changes go well (shared language, a
story a person can see, test-first building) and skips requirements, design, and
phasing documents.

```
interview (align, short)  →  story (one, with design in its tasks)  →  tdd or code-along
```

## 1. Align, briefly

Run `interview` with the subject **align**, scoped to this one change. Explore
the code and `GLOSSARY.md`, `CONTEXT.md`, and `docs/adr/` first; ask only what
they do not answer. Usually three to six questions: who notices this change,
what they see when it works, what is out, what could go wrong, which term means
what. Use one **show, then ask** turn when the change has any structure (a flow,
a state, a screen): draw what you think the change is and ask what is wrong with
the picture.

Settle terms with `glossary` as they come up. Offer an ADR only if a decision
clears the bar; on the light path that is rare, and its appearance is itself a
signal (step 2).

## 2. Check the weight

Before writing anything, check whether this is still light. Escalate to the full
loop when any of these is true:

- You cannot name the seams the change plugs into without thinking.
- It needs more than two stories, or a story needs more than five tasks.
- A decision cleared the ADR bar and is hard to reverse.
- The change touches a trust boundary, persistence shape, or public contract that
  other work depends on.

Two other signals send it elsewhere:

- **Fog.** Nobody can yet say what the questions are; every answer opens three
  more. Hand off to `/trailblazer` to find the way first.
- **One technical unknown.** The change is clear but you do not know if the
  approach works (the library, the limit, the payload). Run a `spike` before
  writing the story, then continue here with its verdict.

To escalate, say which signal fired in one line, and hand off to
`/write-requirements` (or `/trailblazer` for fog); the interview so far is its
raw material. Otherwise continue.

## 3. Write the story

Write one story (two at most) with the `story` skill, in its
`FORMAT.md`. The light path has no design doc, so each
task's Design section carries the mechanism: the interface or function
signature, any data shape, the algorithm steps if a reader could get them wrong,
and a short sketch of the core. Draw the Picture with `visualize`.

Run the critic from the `story` skill. Show the user the story's title, Demo,
and task titles in a few lines, and ask if it is the change they meant. Iterate
until they agree.

Publish per `docs/agents/profile.md`: on a tracker, one issue; otherwise
`docs/planning/<slug>/stories/01-01-<slug>.md` (and `01-02` for a second story),
`<slug>` a short kebab-case name for the change.

## 4. Build

Ask which hands write it, recommending from history: if
`docs/code-along/NOTES.md` exists the user has coded along here before.

- **`tdd`**: the agent builds it task by task and performs the Demo.
- **`code-along`**: the user builds it from a lesson, then debriefs.

It is safe to clear context first; the story file has everything. After the
build, suggest `review-change` with the story as the spec, then the `pr` skill
to open the PR from the story's journal.

## Rules

- **One change.** If a second, unrelated change appears, park it as a line in the
  hand-off for its own `/light` run.
- **No documents the change does not need.** No requirements, design, or phases
  file. The story is the design.
- **The story is still a story.** The light path skips documents, not the Demo,
  the Picture, or the critic.
- **Escalating is success.** Finding out early that a change is heavy is the
  cheapest time to find out.
