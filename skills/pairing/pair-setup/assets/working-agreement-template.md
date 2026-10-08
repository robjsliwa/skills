# Working agreement template

The contract every pair-* skill reads first and obeys. Terse and declarative:
rules and commands, not reasons (the reasons live in ADRs). Aim for 60 to 150
lines. Delete any section that does not apply rather than leaving it empty.

```markdown
# Working agreement

This file outranks every pair-* skill and every agent default. Change it
through a `chore/` branch and a PR like any other change.

## Product
<One sentence: what we are building and for whom.>
Sources: see `docs/pairing/ROADMAP.md`.

## Stack
- Language: <e.g. Go 1.23>
- Runtime / platform: <e.g. Linux container, AWS Lambda>
- Framework and libraries: <closed list, each with a one-word role>
- Persistence: <e.g. PostgreSQL 16 via pgx; migrations with goose>
- Dependency policy: <e.g. stdlib first; a new dependency needs a slice that
  names it and an ADR if it carries lock-in>

## Commands
- Fast tests (every step): `<cmd>`
- Full check (before commit on ship, and in CI): `<cmd>`
- Lint: `<cmd>`   Format: `<cmd>`   Typecheck: `<cmd>`
- Run locally: `<cmd>`

## Layout
- `<dir>/`: <what lives here>
- `<dir>/`: <what lives here>
<The one rule that keeps them apart, e.g. "core never imports adapters".>

## Coding style
Enforced by tools: <formatter, linter, config file names>.
Rules no tool enforces:
- <e.g. errors are wrapped with context at every package boundary>
- <e.g. no exported identifier without a doc comment>
- <e.g. functions over 60 lines are a smell worth a word in review>

## Testing
- Framework: <e.g. stdlib testing + testify/require>
- Tests live: <e.g. next to the code, *_test.go>
- Seams: <the public boundaries tests target; no tests against internals>
- TDD: <e.g. test first for domain logic; test after is fine for wiring>

## Git flow
- Default branch: `main`. Nobody commits to it directly.
- Branch: `<type>/<NNNN>-<slug>`, type in feat | fix | chore | refactor | docs
- Commits: <e.g. Conventional Commits; subject under 72 chars; body says why>
- Who commits: <agent, after each green step | user, agent proposes message>
- Checkpoints: `wip:` commits allowed on slice branches; pushed: <yes | no>
- Update from main before ship: <rebase | merge>
- Merge strategy: <squash | merge commit | rebase>; delete branch after merge
- CI must be green before merge: <yes | no CI yet>

## Pull requests
- Mode: <github | gitlab | local (no remote; merge --no-ff with the PR body
  as the merge message)>
- Open as: <draft | ready>
- Agent review axes: standards, spec, decisions (ADRs and glossary)
- Post agent review as a PR comment: <yes | no>
- Human reviewers: <none | @handle>
- Who merges: <agent after explicit yes in chat | user only>
- Footer: <optional line every PR body ends with>

## Pairing preferences
- Default mode: <driver | navigator | ping-pong | dictation>
- Step size: <small (one test) | medium (one behaviour)>
- Explanations: <terse | explain new ideas | teach as we go>
- Journal: <every step | every commit-worthy step>
- Checkpoint: <every N steps | when I say | when context is heavy>

## Hard rules
- <e.g. never edit files under migrations/ that are already merged>
- <e.g. no network calls in unit tests>
```
