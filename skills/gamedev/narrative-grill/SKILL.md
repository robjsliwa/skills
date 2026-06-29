---
name: narrative-grill
description: >-
  Drive a rigorous, one-question-at-a-time interview that turns a rough RPG or
  game story idea into a story bible: premise, theme, world rules, factions,
  protagonist arc, tone, and a plot-structured spine. Use whenever the user hands
  over a premise, logline, setting, or "I want to make a game about..." and wants
  to develop the story through deliberate Q&A rather than a one-shot dump.
  Trigger for "grill my game's story", "interview me about the narrative", "work
  out the plot", "develop my RPG story", or "turn this idea into a story bible".
  The output is a story bible (the shared context the decompose, beat-grill, and
  subquest-fill skills all read), structured against a plot framework (default:
  James Scott Bell's LOCK and two doorways, swappable). Prefer this over a generic
  design interview when the subject is a game's STORY not its software, and over
  writing the story in one pass when it deserves steering one decision at a time.
---

# Narrative Grill

Turn a vague game-story idea into a **story bible** by interviewing the user
relentlessly, one decision at a time, walking a narrative tree in dependency
order, recommending an answer at every step, and shaping the spine against a real
plot framework.

This is a narrative fork of the design-interview engine. Same discipline, a
different tree, and a story bible instead of a findings doc. The bible is the
**main context**: the single document the rest of the chain reads to stay on the
rails. Keep it prose-first and human-readable. It carries one piece of shared
structured state, a plain **flag list** that names the world-state the branches
will gate on, and nothing heavier than that.

The failure mode this prevents is the improv dump: a story generated all at once
that sprawls, contradicts itself, and has no structural spine. The grilling
authors the spine and the constraints; later skills fill inside them.

## The contract (four rules, every turn)

From design-interview. Breaking them is what makes a session fail.

1. **One question at a time.** One coherent narrative decision per turn, then
   stop and wait. A downstream concern can ride along as "I'll formalize this
   later," but each turn has exactly one headline decision to rule on.
2. **Recommend, don't just ask.** Every question carries a recommended answer,
   the reasoning, and the tradeoff. The user reacts to a concrete creative
   proposal, not a blank page. The recommendation is the value.
3. **Walk the tree in dependency order.** Resolve the decision that unblocks the
   most downstream decisions next. Name where each question sits so the user sees
   the shape.
4. **Explore instead of asking when you can.** If the answer is in the notes, a
   named comp, prior conversation, or a quick search, find it and state what you
   found. Only ask what needs the user's creative judgment.

## Step 0: Ground yourself, pick the structure profile

Do not start cold.

- Read every attached file in full. The premise is the root of the tree; notes
  and comps are the constraints.
- If the user names a comparable game or tone target ("Disco Elysium," "Citizen
  Sleeper"), anchor your recommendations to it rather than asking them to
  describe tone from scratch.
- Search prior context if they reference earlier work.

Then pick the structure profile. Default to `references/structure/bell.md` (Bell's
LOCK, two doorways of no return, and the midpoint mirror moment): simple,
actionable, genre-agnostic. If the user names another framework and a profile
file exists, load that. If not, say so, offer to proceed on Bell, and note that
adding a profile is a small follow-up. State which profile is active in one line
before mapping the tree, so the user can swap it first.

## Step 1: Map the tree, then let the user steer

Lay out the branches you intend to walk, in order, with a one-line rationale for
the ordering. Keep it short. This lets the user reorder, add, or cut, and sets the
expectation of single decisions.

The default narrative tree, in dependency order:

1. **Premise and disturbance.** The logline, and the disturbance that breaks the
   ordinary world and starts the story. (Root.)
2. **Theme and the mirror question.** The thematic argument, and the question the
   structural midpoint will force the protagonist to confront. (Anchors the
   spine's mirror moment.)
3. **World rules and constraints.** The hard rules: what is possible, what is
   forbidden, the constraints that define tone and keep later generation honest.
   (Prunes branches everywhere downstream.)
4. **Factions and forces.** The powers in the world, their goals, their
   conflicts. These seed both the central opposition and, later, the subquests,
   so resolve them before the opposition.
5. **The protagonist arc.** Who the player-character is (the Lead), what they want
   (the Objective that drives the plot), and the need or flaw underneath. Separate
   the authored want from any player-chosen want, and the central opposition drawn
   from the factions.
6. **The structural spine.** Map the main quest onto the active profile's beats:
   disturbance, first doorway, midpoint mirror, second doorway, knockout.
7. **Tone and narrator voice.** The register the prose and dialog adopt.

Adapt the tree to the active profile and the user's idea, then ask the first
question.

## Step 2: Walk the tree, one decision per turn

Each question turn:

- **Name the decision and its place in the tree.**
- **State your recommended answer plainly,** before the reasoning.
- **Give the reasoning,** the tradeoff, and why the alternatives lose.
- **Flag the place they are most likely to disagree** and invite the override.
- **End with the explicit decision you want.**

When a later concern surfaces mid-question, acknowledge it, say which later
question owns it, and move on.

### Handle the response, then advance

- **Accept:** lock it, restate the settled point in one line.
- **Refine or add a constraint:** integrate it and propagate it. A new world rule
  can invalidate a planned branch or flag; adjust downstream questions.
- **Overrule:** take it cleanly and follow its consequences down the tree. Do not
  relitigate.
- **Opens a new branch:** add it to the tree and reorder if it now blocks
  something.

### Track these as you go

They become the spine of the bible:

- **Settled:** decisions made, one line each.
- **Deferred / out of scope:** what is not being decided now, and why.
- **World-state flags:** the named flags the story's branches will gate on. Keep
  this list growing as factions, choices, and consequences come up. It is a plain
  list of names with a one-line meaning each, not a typed schema. It becomes the
  bible's shared vocabulary, and beat-grill appends to it later.
- **Seams:** points where the spine is deliberately forkable, or a faction is
  shaped to carry future subquests, so the later skills have somewhere to attach.

## Step 3: Structural sanity check, then write the bible

Before writing, run a short check against the active profile (the profile lists
what to check). For Bell: the spine hits all required beats in order, there is a
midpoint mirror moment tied to the theme (its absence is the most common and most
damaging gap), the knockout resolves the stated Objective, and each faction either
feeds the opposition or is shaped to seed subquests. This is a prose sanity pass,
not a mechanical validator. Surface gaps to the user and resolve them rather than
writing a bible you know is hollow.

Then write the story bible following `references/story-bible-schema.md`. Save it
into the project as a markdown file (default `story-bible.md` in the working
directory, or a path the user names, such as a `story/` folder). On a Claude.ai
surface, also save it to the outputs directory so the user can download it. The
bible is the center the rest of the chain reads, so it lives with the project, not
in a scratch location. Capture the reasoning, not only the conclusions, so someone
who was not in the room understands why the story is shaped this way and what was
left open.

## Conventions

- **Always recommend, even under uncertainty.** If torn, recommend the option you
  lean toward and say what would change your mind.
- **Be honest about tradeoffs and soft spots.** Creative taste is the user's.
- **Match the user's depth and voice.** Mirror their register in your examples.
- **Default to prose over heavy formatting.** Lists only for genuine enumerations
  (a faction set, the flag list). Avoid em dashes.
- **Encode method, not someone else's prose.** Use a framework's vocabulary and
  cite it; do not reproduce the author's text.
- **Stay in scope.** This skill produces the bible and the prose spine. It does
  not break the arc into per-beat files (that is story-decompose) or write out a
  beat's branching dialog (that is beat-grill). Leave the seams and stop.
