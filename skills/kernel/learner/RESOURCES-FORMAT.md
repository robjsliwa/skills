# RESOURCES.md Format

`RESOURCES.md` is the curated set of sources the teaching draws on, and the
communities wisdom comes from. Knowledge is taken from here, not from memory.
Research notes in `research/` cite these; a source used there and found good is
promoted here.

## Template

```md
# {Topic} Resources

## Knowledge

- [Spec: SE-0395 Observation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0395-observability.md)
  **Tier:** primary. Use for: what `@Observable` tracks and why it tracks reads.
- [Book: _Intermediate Macroeconomics_, 3rd ed., ch. 4](https://example.com)
  **Tier:** authoritative secondary. Use for: the IS-LM derivation.

## Wisdom (communities)

- [Swift Forums](https://forums.swift.org/)
  Language questions; core team answers. Use for: "why does the compiler say..."

## Gaps
- {What the mission needs that no good source covers yet}
```

## Tiers

Every knowledge entry carries a tier. The `professor` skill's DOMAINS.md says
what counts as primary for each kind of subject.

- **primary**: the thing itself or its owner. A spec, the source code at a
  version, a statute or opinion, a historical document, a dataset, the score,
  the original paper.
- **authoritative secondary**: a recognised textbook or review written by
  experts and checked against primary sources.
- **pointer**: a blog, video, or forum answer. Never cited for a claim; kept
  only because it leads to a primary source or explains one unusually well.

## Rules

- **High-trust only.** Marketing dressed as education stays out.
- **Annotate every entry.** One line: what it covers and when to reach for it.
- **Name the edition or version.** Quotes and page numbers must match one copy.
- **Surface gaps.** A `## Gaps` list drives the next research.
- **Prune.** Wrong, shallow, or off-mission sources are removed, not buried.
- **Respect opt-outs.** If the learner does not want communities, say so here.
