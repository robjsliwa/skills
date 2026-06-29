---
name: beat-grill
description: >-
  Grill a single beat file (from story-decompose) into its branch points: the
  scenes, the player choices, the world-state flag that guards each choice, the
  consequences each choice writes back to state, and the actual dialog lines. This
  is the design-interview engine scoped to one beat. Use whenever the user points
  at a beat or scene and wants to "grill this beat", "work out the branches",
  "write the choices and dialog", "flesh out this scene", or "fill in this beat".
  Trigger on a single beat at a time, after a bible and decomposed beat files
  exist. The output is the same beat file, expanded from a stub into full branching
  content, with any new flags appended to the bible's flag list. Do not use this to
  write the bible (narrative-grill), to split the arc into beats (story-decompose),
  or to seed subquests (subquest-fill).
---

# Beat Grill

Take one beat file and grill it from a stub into full branching content: the
scenes play out, the player's choices are named, each choice is gated by a
world-state flag where it should be, each choice writes its consequences back to
state, and the dialog is written. One beat at a time. This is the design-interview
engine pointed at a single beat instead of a whole design.

Working one beat at a time, with the bible open as the center, is the whole point
of the chain. It keeps each session small enough to do well and keeps every beat
consistent with the same world.

## The contract (four rules, every turn)

From design-interview, scoped to this beat.

1. **One question at a time.** One fork in this beat per turn. Do not stack.
2. **Recommend, don't just ask.** Every fork carries your recommended choice
   design, its reasoning, and the tradeoff. The user reacts to a concrete
   proposal.
3. **Walk the beat in order.** Scene by scene, and within a scene, the choices in
   the order the player meets them. A consequence that gates a later choice in the
   same beat comes before it.
4. **Explore instead of asking.** The bible answers most context questions: tone,
   world rules, who a faction is, what a flag means. Read it rather than asking.

## Step 0: Read the bible, then the beat

Read the story bible first (the beat file links to it), then the beat file. You
need the bible for tone, world rules, the factions in play, and especially the
**flag list**, which is the shared vocabulary every guard and consequence must use.
You need the beat file for this beat's job, its scene checklist, and any forks the
bible already named.

If either is missing, stop and say which. This skill expands an existing beat
stub; it does not invent the beat.

## Step 1: Confirm the beat's shape

Restate, in a line or two, what this beat does and the scenes it contains, drawn
from the stub. Ask the user to confirm or adjust the scene list before you grill
the branches, so you are filling the right structure. Recommend your own read.

## Step 2: Grill the branches, one fork at a time

Walk the scenes. At each fork:

- **Name the fork and its scene.** "Scene 2, the smuggler's offer: what does the
  player get to choose?"
- **Propose the choices.** Recommend the set of player choices, two to four, each
  meaningfully different. Say why these and not others.
- **Design each choice's guard and consequence.** For each choice, state whether
  it is gated (a `guard`: a flag from the bible that must hold for the choice to be
  available) and what it writes (a `consequence`: a flag it sets or clears). Use
  flag names from the bible's flag list. If a choice needs a flag that does not
  exist yet, name it, and add it to the bible's flag list (see Step 4).
- **Flag the soft spot.** Where a reasonable designer would gate or branch
  differently, name it and invite the override.
- **End with the explicit decision.** What choices, guards, and consequences you
  are asking the user to accept for this fork.

When the user accepts, write the dialog for that beat of interaction in the bible's
voice: the narration, the choice prompts as the player sees them, and the lines
that follow each choice. Match the tone and any sample voice line from the bible.

Keep the load-bearing structure intact: if this beat is the mirror moment or the
knockout, do not let a fork route the player around it (the bible's structure
profile says which beats are load-bearing).

## Step 3: Write the expanded beat back into its file

Replace the stub's scene checklist and known-forks sections with the full content:
each scene, its choices, each choice's guard and consequence stated plainly, and
the dialog. Keep the choices, guards, and consequences co-located with the scene
they belong to, in the beat file, so the beat stays self-contained and readable on
its own. Update the file's status marker from `stub` to `grilled`.

See `references/beat-content-conventions.md` for how to lay out choices, guards,
consequences, and dialog in the file, and the flag-naming convention.

## Step 4: Keep the flag list coherent

Any flag you introduce in this beat (as a guard or a consequence) that is not
already in the bible's flag list, append to the bible's flag list with a one-line
meaning. This is the one place beat-grill writes outside its own beat file, and it
is what keeps every beat's branch conditions speaking the same vocabulary. Do not
keep a private flag list in the beat file; the bible is the single home for flags.

## Step 5: Hand off

Present the expanded beat file. Note the next unstubbed beat if there is one. Do
not grill the next beat automatically; one beat per session is the discipline.

## Conventions

- **Use the bible's flags, do not fork the vocabulary.** A guard on a flag that is
  not in the bible's list is a broken branch. Add the flag to the bible first.
- **Choices must matter.** A choice with no guard and no consequence is flavor, not
  a branch. That is fine occasionally, but if a whole beat has no consequences, the
  beat does not move the state and that is worth flagging to the user.
- **Match the bible's voice.** Dialog adopts the bible's tone and sample voice.
- **Default to prose for the grilling. Avoid em dashes.**
