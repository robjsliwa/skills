# CLAUDE.md template

`CLAUDE.md` is the contract another coding agent (Claude Code typically) reads on every turn while building the project. It's the project-level constitution: the rules that, if violated, would cause systemic damage to the codebase.

This is **not** a tutorial or README. It's terse, declarative, and authoritative. Aim for 100–200 lines.

```markdown
# CLAUDE.md — agent contract for <project>

You're building <project>, described in `proposal/<file>.md`. The
implementation plan is in this same repo: read each
`phase-NN-*/README.md` for context on the slice you're working in,
and the relevant `story-NN-MM-*.md` for the unit of work.

## Stack

- Language(s) and version: e.g. Go 1.22+, TypeScript 5.x.
- Architectural style: e.g. hexagonal (ports and adapters).
- Database(s): e.g. PostgreSQL 15+. No SQLite, even for dev.
- Key libraries pinned by name: e.g. chi router, sqlc, pgx/v5,
  golang-migrate, mark3labs/mcp-go.
- Frontend stack if applicable: e.g. React 18 + TS + Vite +
  Tailwind 4 + @xyflow/react.
- Build tooling: e.g. Make, Vite, Docker Compose for dev.

This list is closed. Don't introduce new dependencies without a
story explicitly authorizing it.

## Layering

Describe the directory layering rules. Example for a hexagonal Go
project:

- `internal/core/domain/` — pure types and business invariants.
- `internal/core/ports/` — interfaces consumed by services.
- `internal/core/services/` — orchestration; no I/O.
- `internal/adapters/primary/` — driving adapters (HTTP, CLI, MCP).
- `internal/adapters/secondary/` — driven adapters (Postgres, broker).
- `cmd/<tool>/` — entry points only; no business logic.

State the rule precisely: "core never imports adapters. Adapters
implement ports." If layering is enforced by `go-arch-lint` or a
similar tool, name it.

## Persistence contract

Spell out the persistence rules — the rules that, if broken, would
cause data leaks, integrity bugs, or compliance failures. Examples:

- Every tenant-scoped table has `tenant_id NOT NULL` with an FK to
  `tenants(id)`. RLS is enabled. The app sets
  `SET LOCAL app.tenant_id = $1` inside every transaction. **Never**
  write `WHERE tenant_id = ?` in application code; RLS handles it.
- Migrations are forward-only. Rollback is a new migration, not
  reversing the prior one.
- All writes go through repository ports. No raw SQL outside
  `internal/adapters/secondary/postgres/`.

## Auth and authorization contract

- Token format: e.g. JWT HS256 with claims `{iss, sub, tid, email,
  iat, exp, scope, jti}`.
- Middleware: every API route is gated by token verification +
  policy check.
- Authorization is OPA-only (or whatever applies). No inline role
  checks. The `PolicyEngine` port is the only way to ask "can this
  user do this action".

## Observability

- Structured logging via `slog` with at minimum `tenant_id`,
  `request_id` baked into every log line on a request path.
- OTel traces wired through HTTP middleware and key service entry
  points. Span names follow the pattern `<package>.<Function>`.
- Prometheus metrics for the standard golden signals (request rate,
  errors, latency).

## Public surface

Enumerate the public surface — these are the things the agent should
not invent or extend without an explicit story. Examples:

### CLI surface

- `<tool> login` — authenticate.
- `<tool> logout` — clear credentials.
- `<tool> workload upload <file>` — create a workload.
- `<tool> workload execute <id>` — enqueue a run.
- ...

### REST surface

- `POST /v1/workloads` — create.
- `GET /v1/workloads` — list.
- ...

This list is closed. New endpoints come from new stories.

## Definition of done (per story)

A story is done when:

- The story's acceptance criteria checkboxes are all checked.
- All tests in the story's TDD plan are written and passing.
- `make test` is green at HEAD; `go test -race ./...` is green.
- Linters pass (`make lint`).
- Migrations apply cleanly on a fresh database.
- The story's "README updates" section has been applied to the
  affected READMEs.
- The story's "Verification" commands run successfully.

## Working style

- TDD: write tests first; let them go red before implementation.
- One story = one PR (or one logical commit if you're working solo).
- README updates ship in the same change as the code that motivates
  them — never in a separate "docs" PR.
- If you find a problem the story didn't anticipate, prefer
  documenting it in the next-story file over silently fixing it.
- Don't refactor across story boundaries unless the story explicitly
  authorizes it. Refactor stories are normal — they just need to be
  named.

## When in doubt

- Re-read the proposal section the story references.
- Re-read this file.
- Stop and ask the human, rather than inventing.
```

## What goes in CLAUDE.md vs README.md vs story files

This is the most common confusion. The rule:

- **CLAUDE.md** — rules that apply to *every* story. Stack, layering, contracts, definition of done, working style.
- **Top-level README.md** — orientation for a reader. What MVP means, prerequisites, how to read the plan, the end-to-end "definition of done" script.
- **Phase README.md** — what *this phase* delivers and why these stories in this order.
- **Story file** — what *this one PR* does, with tests and verification.

If you find yourself adding "in story NN-MM, do X this way" to CLAUDE.md, it belongs in the story. If you find yourself repeating "every story should set `app.tenant_id`" in three different stories, it belongs in CLAUDE.md.

## Length target

100–200 lines. CLAUDE.md is reread constantly; long ones get skimmed. If you exceed 200 lines, the most likely culprit is that story-specific detail has leaked in — pull it back into the relevant story.
