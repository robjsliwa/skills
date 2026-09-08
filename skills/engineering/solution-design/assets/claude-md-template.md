# CLAUDE.md agent contract template

`CLAUDE.md` is the contract a coding agent reads on every turn while building. It
holds the rules that apply to every story: the ones that, if broken, damage the
codebase systemically. It is terse, declarative, and authoritative. The design doc
holds the reasoning; this holds the rules. Story-specific detail belongs in the
story, not here.

Aim for 100 to 200 lines. If it runs longer, story detail has leaked in.

```markdown
# CLAUDE.md

You are building <project or feature>. The design is
`docs/planning/<slug>/design.md`; the build order is
`docs/planning/<slug>/phases.md`; the unit of work is one story under
`docs/planning/<slug>/stories/` (or the tracker issue you were pointed at).

## Stack

- Language(s) and version: e.g. Go 1.22+, TypeScript 5.x.
- Architectural style: e.g. hexagonal (ports and adapters).
- Database(s): e.g. PostgreSQL 15+. No SQLite, even for dev.
- Libraries pinned by name: only those the design's dependency policy
  justified.
- Build tooling: e.g. Make, Docker Compose for dev.

This list is closed. A new dependency needs a story that authorizes it.

## Layering

The directory rules and the one sentence that enforces them. Example for a
hexagonal Go project:

- `internal/core/domain/`: pure types and invariants.
- `internal/core/ports/`: interfaces the core depends on.
- `internal/core/services/`: orchestration; no I/O.
- `internal/adapters/primary/`: driving adapters (HTTP, CLI, MCP).
- `internal/adapters/secondary/`: driven adapters (Postgres, broker).
- `cmd/<tool>/`: entry points only.

Core never imports adapters. Adapters implement ports. Name the tool that
enforces it if one exists.

## Persistence contract

The rules whose violation leaks data or corrupts it. Examples:

- Every tenant-scoped table has `tenant_id NOT NULL`. RLS is on. The app
  sets `SET LOCAL app.tenant_id` inside every transaction and never writes
  `WHERE tenant_id = ?` by hand.
- Migrations are forward-only; a rollback is a new migration.
- All writes go through repository ports.

## Auth and authorization contract

- Token format and claims.
- Which routes are gated, by which middleware.
- The single port through which "can this principal do this" is asked.

## Observability

- Structured logging and the fields every request-path line carries.
- Tracing: where spans start, the span naming pattern.
- Metrics: the golden signals, by name.

## Public surface

The CLI commands, routes, and MCP tools that exist. This list is closed; new
surface comes from new stories.

### CLI
- `<tool> <verb>`: one line each.

### REST
- `POST /v1/<resource>`: one line each.

## Definition of done (per story)

- The story's acceptance criteria are all checked.
- Every test in the story's TDD plan exists and passes, RED first.
- `make test` (or the project's equivalent) is green at HEAD; race detector
  clean where the language has one.
- Linters pass.
- Migrations apply cleanly on a fresh database.
- The story's verification commands run and show the expected output.
- The story's `Status` is flipped to `done` (or the issue closed).

## Working style

- TDD at the story's named seams; one test, one implementation, repeat.
- One story is one PR.
- A problem the story did not anticipate goes into the next story or a
  `Drift` note in `phases.md`, not into a silent fix.
- No refactors across story boundaries unless a story authorizes it.

## When in doubt

Re-read the design section the story cites. Re-read this file. Then ask,
rather than inventing.
```

## Merging into an existing file

Most repos already have a `CLAUDE.md` (or `AGENTS.md`). Edit the one that exists;
never create the other alongside it. Map each template section onto the existing
file: a `## Stack` heading already there gets updated in place, not duplicated;
a missing section is added; everything else in the file is left untouched,
including any `## Agent skills` block written by `setup-matt-pocock-skills`. For a
feature added to an existing system, the typical merge is a few new public-surface
lines, a new persistence or auth rule, and nothing else.
