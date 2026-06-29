# Beat content conventions

How beat-grill lays out a grilled beat in its file. The goal is a beat that reads
cleanly on its own and keeps its branching logic next to the content it belongs
to, so there is no separate graph file to maintain. The bible holds the flag
vocabulary; the beat holds everything else about itself.

## Flag naming

Flags are the shared world-state vocabulary, and they live in the bible's flag
list. The convention:

- `snake_case`, state-or-event shaped: `met_the_smuggler`, `reactor_sabotaged`,
  `knows_the_captains_secret`.
- A flag names a fact about the world, not a UI action. Prefer `door_unlocked`
  over `pressed_button`.
- Boolean by default. If a flag needs more than true/false, say so in its one-line
  meaning in the bible.

Before using a flag as a guard or a consequence, make sure it exists in the
bible's flag list. If it does not, add it there first (beat-grill Step 4).

## Laying out a scene

Within the beat file, write each scene as a short section: the narration, then the
choices, each with its guard and consequence stated plainly, then the dialog that
follows. Keep it readable; this is a script, not a data dump.

```markdown
## Scene 2: The smuggler's offer

[Narration in the bible's voice. The smuggler leans across the table...]

**Choices:**

- **"Take the deal."**
  - guard: none
  - consequence: sets `met_the_smuggler`
  - [The dialog that follows this choice.]

- **"Walk away."**
  - guard: none
  - consequence: sets `refused_the_smuggler`
  - [The dialog that follows this choice.]

- **"Threaten him."** (only if the player is armed)
  - guard: `has_weapon`
  - consequence: sets `smuggler_hostile`
  - [The dialog that follows this choice.]
```

Rules for this layout:

- **guard** is a single flag from the bible's list that must hold for the choice to
  be offered, or `none`.
- **consequence** is the flag(s) the choice sets or clears, or `none`. State each
  one; these are how the world remembers what happened.
- Every flag named here must exist in the bible's flag list.
- A choice may reconverge to a shared continuation, or lead to a different next
  scene. Say which in plain words ("continues to Scene 3" / "ends the beat; the
  player is captured"). No need for node ids; the prose is the link.

## Load-bearing beats

If the bible's structure profile marks this beat as load-bearing (for Bell, the
mirror moment and the knockout), do not write a choice that lets the player skip
it or reach it unearned. Forks inside a load-bearing beat are fine; forks that
route around it are not.
