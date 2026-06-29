# Top-level README template

The top-level `README.md` is the entry point for both the human reviewer and any agent picking the plan up cold. It orients them, describes what MVP means for *this* project, and ends with a concrete "definition of done" script.

This is **not** the project's user-facing README — that gets written as part of the actual implementation. This README is for the *plan*.

```markdown
# <Project> MVP — Phased Implementation Plan

This bundle is a phased, story-by-story plan to build the <project>
MVP described in `proposal/<file>.md`. It is written for an AI coding
agent (Claude Code in particular) and a human reviewer working
together. Every story is small enough to land in a working state, and
every story is self-contained: narrative, test plan, implementation
hints, acceptance criteria, README updates.

## What "MVP" means here

The MVP is the smallest cut of <project> that delivers the experience
described by the user:

1. **<Headline capability 1.>** One-line elaboration.
2. **<Headline capability 2.>** One-line elaboration.
3. **<Headline capability 3.>** One-line elaboration.
4. ...

Aim for 4–7 numbered items. These are the user-facing commitments;
anything not on this list is either implicit (table-stakes, like
"the binary compiles") or post-MVP.

Then a paragraph naming what's deliberately deferred:

> Everything else from the v<X> proposal — <list a few key deferred
> features> — is deliberately post-MVP.

## How to read this plan

```
<project>-mvp-plan/
├── CLAUDE.md                         # Agent contract (read first)
├── README.md                         # This file
├── phase-00-bootstrap/               # Project skeleton, schema, dev tooling
├── phase-01-<slug>/                  # First user-visible slice
├── phase-02-<slug>/                  # ...
└── phase-NN-<slug>/                  # Final phase
```

Each phase folder has its own `README.md` describing the slice that
phase delivers, plus one file per story.

## Recommended workflow

1. Read `CLAUDE.md`. It is the contract.
2. Open the current phase's `README.md`. It says what the phase
   delivers and why the stories are in that order.
3. Start with the lowest-numbered story not yet done. Each story is a
   single PR worth of work.
4. Follow the TDD order in each story: tests first, implementation
   second.
5. Run the verification steps before declaring done.
6. Move to the next story.

## Why this ordering

Brief notes on phase ordering rationale — usually one sentence per
phase. The point is to defend the structure to a reviewer. Example:

- Phase 0 gets a project on disk and a multi-tenant schema. Nothing
  runs meaningfully yet, but the next phase has a foundation.
- Phase 1 makes `<tool> login` actually work end-to-end. By the end
  of this phase the binary is useful in a small way.
- Phase 2 stores <resource>s and exposes CRUD over CLI. By the end
  the user can manage <resource>s, even though they cannot yet run
  them.
- ...

## Build prerequisites

- Tools: e.g. Go 1.22+, Node 20+, Postgres 15+.
- CLIs: e.g. `golang-migrate`, `sqlc`, `claude` (for Claude Code-driven
  workflows).
- Optional: e.g. Docker for the dev compose stack.

The Makefile produced by Phase 0 has targets for everything: `make
compose-up`, `make migrate-up`, `make test`, `make build`, `make run`.

## Definition of done (the whole MVP)

The MVP is done when a fresh developer can clone the repo and execute
this script end-to-end without manual intervention beyond following
prompts:

```bash
git clone <repo> && cd <project>
cp .env.example .env
make compose-up && make migrate-up
make build && ./bin/<tool> server &

./bin/<tool> login                                    # Phase 1
./bin/<tool> <resource> upload examples/hello.<ext>   # Phase 2
./bin/<tool> <resource> list                          # Phase 2
RUN_ID=$(./bin/<tool> <resource> execute hello -o id) # Phase 3
./bin/<tool> <resource> tail "$RUN_ID"                # Phase 3
./bin/<tool> ui                                       # Phase 4
./bin/<tool> mcp                                      # Phase 5
```

Plus: <whatever cross-cutting capability proves the agent integration
works>.
```

## What goes in this file vs CLAUDE.md

This file is for *humans onboarding to the plan*. CLAUDE.md is for *agents executing the plan*.

- This file says "read CLAUDE.md first." CLAUDE.md doesn't reference this file.
- This file lists prerequisites with version numbers and where to get them.
- This file shows the end-to-end script that's the contract for "MVP shipped".
- CLAUDE.md says how to behave on every PR.

Some overlap is fine (e.g. mentioning the stack in both). When in doubt: rules → CLAUDE.md, narrative → README.

## Length target

80–150 lines. The "definition of done" script is often the most valuable thing in the file — make sure it reflects the actual capabilities of every phase.
