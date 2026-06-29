---
name: subquest-fill
description: >-
  Walk the factions and world-state flags in a story bible and seed side quests
  that hang off them, so subquests inherit established lore instead of floating
  free. Each seeded subquest is a small beat stub that beat-grill can later expand.
  Use whenever the user has a bible (and usually a decomposed main spine) and wants
  to "add side quests", "seed subquests", "fill out the world with optional
  content", "give the factions something to do", or "generate side content that
  fits the lore". Trigger after the main story exists and the user wants optional
  branches anchored to the established world. The output is a set of subquest stub
  files under the beats folder, each tied to a faction and referencing existing
  flags. Do not use this to write the bible (narrative-grill), decompose the main
  spine (story-decompose), or write a beat's dialog (beat-grill).
---

# Subquest Fill

Seed side quests that grow out of the world the bible already established. The rule
that makes this skill earn its place: a subquest must hang off something already in
the bible, a faction with a goal or a world-state flag the player can reach, so it
inherits established lore rather than floating free as generic filler.

The output is stubs, not finished content. Each subquest is seeded as a small beat
stub in the same shape story-decompose produces, so beat-grill can expand it with
the same workflow as any main-spine beat. Subquests reuse the chain; they do not
need their own.

## Step 0: Read the bible

Read the whole bible, with attention to two sections: the **factions** (who they
are, what they want, who they conflict with) and the **world-state flags** (what
the player can have done or reached). These are the two anchors every subquest must
attach to. Also note the tone and world rules, so seeded subquests fit.

If there is no bible, stop and say so.

## Step 1: Find the hooks

For each faction, look for the natural side-quest hooks the bible already implies:

- An **unmet goal** the faction has that the main spine does not resolve.
- A **conflict** between two factions the player could be pulled into.
- A **flag** the player might set on the main path that a faction would react to
  (`reactor_sabotaged` gives the engineers' faction a grievance; `met_the_smuggler`
  opens a smuggler errand).

Propose a short list of candidate subquests, grouped by faction, each in one line:
the faction it hangs off, the hook, and the flag or goal it attaches to. Recommend
which ones are worth seeding and which are thin. Let the user pick and adjust. Do
not seed every idea; a few well-anchored subquests beat a pile of generic ones.

## Step 2: Seed the stubs

For each chosen subquest, write a beat stub under `beats/subquests/<faction>/`,
using the same beat file template story-decompose uses. Create the `subquests/`
subfolder now, because there is finally content to put in it. Each stub records:

- The **faction** it hangs off and the **hook** (the unmet goal, conflict, or flag).
- The **entry condition**: the world-state flag or main-spine point that makes this
  subquest available. Reference a flag from the bible's flag list. If the subquest
  needs a new flag, name it and add it to the bible's flag list, the same single
  home beat-grill uses.
- A first-pass **scene checklist**, as a plan for beat-grill.
- The **lore it draws on**: the faction details and world rules from the bible it
  must stay consistent with.

The stub does not contain choices or dialog. beat-grill writes those later, exactly
as it does for spine beats.

## Step 3: Hand off

Present the seeded subquest stubs and where they live. Note that the next step is
to run beat-grill on whichever subquest the user wants to flesh out first. Do not
grill them yourself.

## Conventions

- **Anchored, not free-floating.** Every subquest hangs off a named faction and an
  entry flag or goal from the bible. If you cannot name what it attaches to, it is
  generic filler; drop it or anchor it.
- **Reuse the chain.** Seed subquests in the same beat-stub shape so beat-grill
  expands them with no special case.
- **One home for flags.** A new entry or consequence flag goes in the bible's flag
  list, not a private list in the subquest file.
- **Fit the tone.** Subquests inherit the bible's voice and world rules. A side
  quest that breaks tone is worse than no side quest.
- **Seed a few, well.** Quality of anchoring over quantity. Avoid em dashes.
