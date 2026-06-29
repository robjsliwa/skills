# Beat file template

Each beat is one markdown file in the beats folder, named with its spine number:
`01-disturbance.md`, `02-care.md`, and so on. A file decompose writes is a stub:
enough context to be grilled on its own, but no branching dialog yet.

Use this template:

```markdown
# Beat 03: [Beat name]

**Bible:** [relative path back to the story bible, e.g. ../story-bible.md]
**Act:** [which act this beat sits in]
**Structural role:** [the profile beat this realizes, e.g. "first doorway of no
  return; one-way into the central conflict"]
**Status:** stub

## What this beat does
[One short paragraph: the beat's job in the spine, drawn from the bible. Enough
that someone can grill it without re-reading the whole bible, though the link is
right there if they need it.]

## Scenes
[A checklist of the scenes this beat contains, for beat-grill to work through. One
line each. This is a plan, not the content.

- [ ] The Lead finds the wreck.
- [ ] The smuggler's offer.
- [ ] The choice to commit.]

## Known forks
[Any branch points the bible already named for this beat: the choice, and the
world-state flag that gates or results from it. Reference flags by the names in
the bible's flag list. If the bible named none, say "none yet; beat-grill will
find them." beat-grill fills in the real choices, guards, consequences, and
dialog.]

## Relevant context
[Factions, characters, or world rules from the bible that bear on this beat, named
so beat-grill has them at hand. Pointers, not copies.]
```

The `Status: stub` line is just a marker a human can read at a glance. It is not a
state machine; do not build tooling around it. Promote it to a richer status field
only if and when eyeballing the folder stops telling you what is done.
