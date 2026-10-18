# Changelog

## 2.2.0 (2026-10-18)

Every PR reads like a pairing PR.

### Added

- `pr` (kernel): writes and opens the PR for any flow from the journal, the
  ADRs, and the diff: why, one Mermaid picture whose type fits the change
  (sequence, before/after, state, data, rule, journey; skipped only with a
  stated reason), a What, Why, and How row per concern, the rationale journal
  with its dead ends, decisions, evidence, and merge danger. With no journal,
  it reconstructs one from the commits and asks for any missing why.

### Changed

- `tdd` keeps a `## Journal` in the story file (one entry per ticked task,
  plan change, decision, debug, and spike) and hands off to `pr`; a PR for a
  story is never written ad hoc.
- `pair-ship` calls `pr` for its PR stage; the template moved from
  `pair-ship/assets/` to `pr/assets/`.
- `light`, `code-along`, and `diagnose` route PRs and debug notes through the
  story journal and `pr`.

## 2.1.0 (2026-10-14)

Finding things out, together. Design: [`docs/planning/research-skills/`](docs/planning/research-skills/design.md),
[ADR 0004](docs/adr/0004-research-lives-in-files.md).

### Added

- `trailblazer` (mode): pair research around a living Mermaid trail map in
  `docs/research/<topic>/`. Silent recon first, one question per turn with a
  sketch, node states coloured on the map, background research and spikes,
  forks shown as side-by-side diagrams, a playback after every decision, the
  user picks the next node, and a `report.md` that hands off to the right loop.
- `research` (kernel): a background agent answers a factual question from
  primary sources with every claim marked cited, inferred, or conflict; a recon
  variant reports what the repo already has.
- `spike` (kernel): one technical question, framed with pass and fail criteria,
  run in an isolated worktree inside a timebox, ending in a Confirmed, Rejected,
  or Partial verdict and a brief. Spike code is never merged.
- `prototype` (kernel): LOGIC, UI, and FLOW prototypes from tested single-file
  templates, each with a tradeoff drawer and a feedback bar; the decision is
  redrawn as Mermaid (state, sequence, or screen flow).
- Docs viewer: a `/prototype` route that runs scripts for files under a
  `prototypes/` folder, and a `prototype` event type for picks and notes.

### Changed

- `start` routes foggy ideas to `trailblazer` and resumes trails in progress.
- `interview` hands facts to `research`, can-it-work questions to `spike`, and
  show-me moments to `prototype`.
- `light` escalates fog to `trailblazer` and runs a `spike` for a single
  technical unknown.
- `story`, `tdd`, and `pairing` run spikes with the `spike` skill.
- `write-requirements` accepts a trail report as its raw material.
- The profile gains `Research` and `Spikes` locations.

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
