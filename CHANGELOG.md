# Changelog

## 3.0.0 (2026-10-31)

A cleanup, and the repo is now general purpose.

### Changed

- The plugin and its marketplace entry are now both `agent-skills`. Anyone
  installed through the old `.claude-plugin` names must reinstall.
- `start` absorbs `planning-loop`: it holds the full loop and names the next
  step from `docs/planning/`. It can now be invoked by the model, so "what
  comes next" reaches it without typing `/start`.
- `code-along` picks up the "don't write the code for me" requests and, with no
  story, sends a small change to `light` for one.
- `go-boilerplate` finds its script from `<skill-dir>`, so it works however the
  skill is installed, and its description says when to use it.
- Examples in templates and format files use neutral wording.

### Removed

- `planning-loop`: use `/start`.
- `let-me-code`: use `code-along`. Moved to `skills/deprecated/`.
- `docs/adr/vpid`, a stray process-id file.

## 2.4.0 (2026-10-28)

A professor for any subject. Design: [`docs/planning/professor/`](docs/planning/professor/design.md),
[ADR 0005](docs/adr/0005-learning-kernel-and-no-quiz.md).

### Added

- `professor` (learning): teaches any subject over many sessions, one lesson
  at a time. Each lesson is a lecture deck (a canvas built step by step over a
  conversational transcript, with predict slides answered in chat), a lab that
  builds the next slice of a project the learner chose or picked from two or
  three proposals, office hours, and a teach-back debrief. Before teaching it
  researches primary sources, writes a lesson plan checked against a
  research-backed checklist (PEDAGOGY.md, with citations), verifies every
  claim, and has a fresh agent cold-read the lesson as the learner. Five
  subject lenses (DOMAINS.md) replace per-subject skills. No multiple-choice
  quiz: spaced open prompts open each session instead. Can adopt a
  `teach-me` workspace and rewrite its lessons.
- `learner` (kernel): owns the teaching workspace record: `MISSION.md` (now
  with a Starting point), `SYLLABUS.md`, `RESOURCES.md` with source tiers,
  learning records, `PRACTICE.md` (the spaced retrieval queue), `GLOSSARY.md`,
  and `NOTES.md`. Formats match `teach-me` and `code-along`.
- `slides` (kernel): lecture decks as one HTML page with step reveals,
  highlight-only steps for code, a handout view, and `render_deck.py`, which
  finds Chrome or a Playwright Chromium, reports overflow, crowded canvases,
  step gaps, and overlapping SVG labels, and screenshots every step.
- `fact-check` (kernel): a claims ledger verified by kind, a values script,
  and `assemble.py`, which fills a page from verified snippets and values and
  refuses to write it while anything is unresolved, unverified, or quoted by
  hand.

### Changed

- `research` notes gain an optional For teaching section (core idea,
  misconceptions, a concrete example, what can wait), and go to `research/` in
  a teaching workspace.
- `detour`, `start`, and `trailblazer` send "I need to learn this" to
  `professor` (`teach-me` still works in its existing workspaces).
- `code-along` records use the `learner` skill's format.
- `teach-me` points to `professor` as its successor; its behaviour is
  unchanged.

## 2.3.0 (2026-10-18)

Step out to learn, then come back.

### Added

- `detour` (productivity): a round trip out of the work in progress. Leaving
  pauses the active flow through its own checkpoint, writes a committed brief in
  `docs/detours/` (the gap, where it hit, what you know, what unstuck means),
  and prints the first line for `teach-me`, `trailblazer`, or `spike` in a
  clean context. `/detour back` asks you to say the answer in your own words and
  writes it into the brief's Return section for the paused flow to fold in.

### Changed

- `interview` can pause to `docs/planning/<slug>/interview.md` (tree, the three
  lists, the question on the table) and resume with `/interview resume <slug>`.
- `pair`, `code-along`, and `trailblazer` fold answered detours in on resume;
  a detour still out shows up in pairing's Open threads in `STATE.md`.
- `teach-me` and `trailblazer` accept a detour brief as their starting point
  and end with the return line.
- `start` routes an answered detour back to the flow it paused.
- The profile gains a `Detours` location.
- README: how to update installed skills, and pin or unpin a release tag,
  with the skills CLI or a clone.

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
