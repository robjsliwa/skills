# Decomposition principles

How to slice a proposal into phases and stories. The single most important rule in this document:

> **Phases are vertical slices that end in something demoable.** Stories within a phase are ordered so each one tests on top of the previous.

Everything else flows from that.

## Phase decomposition

### Phase 0 is always foundations

Project skeleton, schema, dev tooling, CI. This is the only phase whose deliverable is "nothing user-visible runs yet — but the foundation is correct." It's exempt from the "demoable" rule.

What goes in Phase 0:
- Project bootstrap (initial scaffold, dependencies, build).
- Database schema and migrations (especially anything that's hard to retrofit: multi-tenancy, RLS, audit columns).
- Dev tooling: linter config, pre-commit hooks, CI workflow.
- The skeleton of the public surfaces (an HTTP server that responds to `/healthz`, a CLI that prints help text, and so on).

What does *not* go in Phase 0:
- Any business logic.
- Any auth flow (that's typically Phase 1).
- Any specific feature implementation.

### Each later phase is a vertical slice

The test of a good phase: can a user (or developer, depending on the audience) point to *something they can do* at the end that they couldn't do before?

Bad phase boundary: "all the REST routes" then "all the CLI commands". Now the user has half a feature in two places.

Good phase boundary: "the user can manage resource X end to end (REST + CLI)" then "the user can manage resource Y end to end".

For services with multiple major resources or capabilities, slice along the *capability* axis, not the *layer* axis.

### Order phases for compounding capability

Each phase should make the previous one more useful, not parallel to it. Example for a typical backend service:

1. **Phase 0 — Bootstrap.** Nothing demoable.
2. **Phase 1 — Identity.** Now you can log in. Useless on its own, but enables every later phase.
3. **Phase 2 — Resource CRUD.** Now logged-in users can store and retrieve things.
4. **Phase 3 — Execution.** Now stored things can be acted upon.
5. **Phase 4 — UI.** Now non-CLI users can do all of the above.
6. **Phase 5 — Agent integration.** Now external systems / LLMs can do all of the above.

Each phase enriches the phases before it. A user could stop at Phase 3 and have a CLI-only product. They could stop at Phase 4 and have a CLI + UI product. Phase 5 just adds another front-end.

### Final phases are often integration

The pattern "Phase N is external surface" (MCP, public API, integration docs, plugin protocol) is common. The last phase is exposed because every other phase has something to expose by then.

### Sizing phases

- **3–7 stories per phase** is the sweet spot.
- **Less than 3** — usually means the phase isn't really a phase; merge it.
- **More than 7** — usually means it's two phases. Split along a capability boundary.

## Story decomposition within a phase

### Front-load the contract

Within a phase, the first story usually defines interfaces, types, or schemas. Later stories implement them. This:

- Lets the agent write tests against stable signatures.
- Makes review of later stories small (the shape was reviewed once).
- Enables in-flight discussion of design before code is written.

Example for Phase 3 (execution) of a workflow service:

1. Gear interface + minimal catalog. (Defines the contract.)
2. In-memory broker port + worker pool. (Implements one collaborator.)
3. Pipeline executor. (Uses the contract and the collaborator.)
4. Execute API + CLI. (Wires the executor to user-facing surfaces.)
5. Run event stream. (Adds observability.)
6. Live tail TUI. (Polish using the events from #5.)

This ordering means: by the end of story 1, the gears interface is stable; story 2 builds on it; story 3 needs both; etc.

### Defer polish

Within a phase, polish goes at the end. If story X-04 is "make the output pretty", that's after the functional work in X-01 through X-03.

Common polish stories:
- TUI / interactive views.
- Output formatting (JSON / text / CSV variants).
- Detailed error messages with hints.
- Observability (metrics, traces) when not part of the contract.

This isn't because polish doesn't matter — it's because it's the most speculative work and benefits from doing it after the substance is settled.

### One PR per story

The single most useful test: "could a senior engineer review this in one sitting?" If no, it's two stories.

Concrete signals it's two stories:
- The acceptance criteria split cleanly into two groups with no shared prerequisites.
- Two different parts of the codebase change (e.g. domain + UI).
- The TDD plan has two clearly distinct test groupings.

Note the "different parts of the codebase" signal cuts against the vertical-slice rule for *phases*. The rule is: phases are vertical, stories are smaller. Within a phase, stories may be horizontal layers if that's how the work naturally divides.

## Hard cases

### Cross-cutting concerns (logging, OTel, error formatting)

These don't get their own phase. They live in:
- Phase 0 if they're truly foundational (e.g. structured logging is set up in the bootstrap).
- The phase that *first* needs them (e.g. OTel wiring lands in the phase that introduces tracing-relevant flows).
- Each story's "Description" if the story extends them (e.g. "this story adds a span around X").

### Refactor stories

A refactor that's needed to enable future stories belongs in its own story, named explicitly: "Story NN-MM — refactor service into ports". Don't slip refactors into feature stories.

### "We discovered we need X"

Mid-build, the agent will sometimes discover the plan missed something. The right response in that situation is to:

1. Note it in the current story's narrative or README updates.
2. Add a new story (or amend a future one) for the missed work.
3. Don't silently bloat the current story.

When you (the planner) write the plan, anticipate this by leaving small slack — don't pack every phase to the gills. A 5-story phase is healthier than a 7-story phase that turns into 9 mid-build.

### Multi-tenancy, encryption, observability

These are easy to retrofit poorly, so they go in *early*:

- Multi-tenancy schema in Phase 0.
- Encryption-at-rest configuration in Phase 0 if it affects schema (encrypted columns).
- Observability scaffolding (logger, OTel SDK) in Phase 0.

The *use* of these capabilities lands in later phases, but the foundation is laid before any business logic.

## Naming

Phase folder name: `phase-NN-<short-slug>`. Examples: `phase-00-bootstrap`, `phase-01-identity-and-rbac`, `phase-02-workload-crud`, `phase-03-execution-engine`, `phase-04-web-ui`, `phase-05-mcp-for-claude-code`.

Story file name: `story-NN-MM-<short-slug>.md`. Examples: `story-00-01-bootstrap-via-init-go-project.md`, `story-03-06-workload-tail-tui.md`.

Slugs:
- All lowercase.
- Hyphenated.
- 2–5 words. Longer slugs become unreadable in `ls` output.
- Should match the H1 inside the file (more or less — abbreviations are fine).

Two-digit zero-padding everywhere. `phase-00`, not `phase-0`. `story-03-06`, not `story-3-6`. This keeps `ls` output sorted.
