# Story bible schema

The output of a narrative-grill session, and the shared context the rest of the
chain reads. Keep it prose-first and human-readable. It carries exactly one piece
of structured state, a plain flag list, and nothing heavier. Save it into the
project as a markdown file (default `story-bible.md` in the working directory, or a
path the user names). On a Claude.ai surface, also save it to the outputs directory
so it can be downloaded.

Use this structure unless the story genuinely calls for adapting it.

```markdown
# [Game title]: Story Bible

**Status:** [e.g. premise grilled, agreed]
**Date:** [date]
**Structure profile:** [e.g. Bell (LOCK + two doorways + mirror moment)]
**Scope:** [one or two sentences on what this covers and what it does not]

[One short paragraph naming the through-line: the single theme or constraint that
shaped the decisions.]

## Logline and disturbance
[The premise in a sentence or two, and the disturbance that starts the story.]

## Theme and the mirror question
[The thematic argument, and the question the midpoint forces the protagonist to
confront. The spine's mirror moment realizes this.]

## World rules and constraints
[The hard rules of the setting: what is possible, what is forbidden, the
constraints that keep later generation honest.]

## Factions and forces
[Each faction: who they are, what they want, who they conflict with. Note which
faction the central opposition draws from, and which factions are shaped to carry
future subquests.]

## The protagonist arc
[The Lead. The authored want that drives the plot, any player-chosen want, and the
need or flaw underneath. The central opposition and why it is strong enough that
the outcome is in doubt.]

## Tone and narrator voice
[The register the prose and dialog adopt, with a short sample line in voice.]

## Structural spine
[The main quest mapped to the active profile's beats, in order. For each beat:
what happens, and for the doorways, why it is one-way. This is the spine that
story-decompose explodes into per-beat files. Number the beats; the numbers carry
into the beat filenames.]

## Branches and seams
[In prose: where the spine forks, what world-state gates each fork, and where the
later skills should attach. Name the flags involved; they live in the flag list
below.]

## World-state flags
[A plain list, the shared vocabulary for branch conditions. One line each:

- `met_the_smuggler` — set when the Lead first allies with the smuggler faction.
- `reactor_sabotaged` — set if the player sabotages the reactor at the second doorway.

Keep names snake_case and verb-or-state-shaped. beat-grill appends new flags here
as it invents them, so this stays the single place the vocabulary lives.]

## Out of scope
[What was deliberately not decided, and the boundary, so the next session knows
where to pick up.]

## Open questions / notes
[Anything unresolved, plus notes that clarify a subtlety the decisions imply.]
```

The bible is the contract the rest of the chain depends on, so the two things that
must stay clean are the **numbered structural spine** (story-decompose reads it to
make one file per beat) and the **flag list** (beat-grill reads and appends to it
to keep branch conditions coherent). Everything else is prose for a human.
