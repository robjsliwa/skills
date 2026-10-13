# Changelog

## 2.0.0 (2026-10-13)

Self-contained, organised around four modes, with stories a person can see and
Mermaid pictures in every planning artifact. Plan and decisions:
[`docs/planning/skills-v2/`](docs/planning/skills-v2/), [`docs/adr/`](docs/adr/).

### Breaking

- **No dependency on `mattpocock/skills`.** Its skills are replaced by this repo's
  kernel: `grill-with-docs` and `grilling` by `interview` (align), `domain-modeling`
  by `glossary`, `setup-matt-pocock-skills` by `repo-setup`, `tdd` by `tdd`,
  `diagnosing-bugs` by `diagnose`, and `code-review` by `review-change`.
- **`design-interview` is deprecated**, superseded by `interview` (decide).
- **`docs/agents/issue-tracker.md` becomes `docs/agents/profile.md`.** `repo-setup`
  migrates it.
- **`CONTEXT.md` changes meaning.** It is now system context (C4 level 1, actors,
  boundary, why). The glossary lives in `GLOSSARY.md`. `repo-setup` offers to split
  an old glossary-style `CONTEXT.md`.
- **New story format.** A story is one change a person can see (Scenario, Demo,
  Picture, Acceptance) and owns its agent-sized Tasks. v1 stories are still read.
- `pair-ship/REVIEW.md` is replaced by the `review-change` skill.

### Added

- `start`: recommends a mode and its first command.
- `light`: the light loop as a skill, with escalation to the full loop.
- `story`: format, splitting patterns, and a critic that runs in a fresh context.
- `visualize`: notation guide (C4 as flowcharts, journeys, screen flows, sequences,
  states, data), HTML mockup sidecars, `mermaid_check.py`, and `docs_viewer.py`, a
  local viewer with live reload, option cards, mockup previews, and node comments.
- "Show, then ask" interview turns and options blocks.
- Context diagram and user journey in requirements, C4 container diagrams in
  designs, a story map in phases, a before/after diagram in PR bodies.
- `scripts/check-skills.py` for frontmatter, unique names, and independence.

### Changed

- `to-story` slices by what a person would see first, then decides each story's
  tasks; the critic checks the breakdown before you see it.
- `code-along` builds lessons from a story's tasks and splits parts at task
  boundaries.
- `pair-setup` extends `repo-setup`; `pair-slice` writes a story header (Scenario,
  Demo, Picture) and runs the critic.

## 1.0.0

The skill set built on top of `mattpocock/skills`: the planning loop, code-along,
the pairing loop, teach-me, gamedev skills, and go-boilerplate.
