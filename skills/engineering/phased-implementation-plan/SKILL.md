---
name: phased-implementation-plan
description: Turn a software proposal or design document plus an MVP scope description into a phased, story-by-story implementation plan and bundle it as a .tar.gz. Use this whenever the user has a proposal/spec/RFC/design doc and wants a TDD-style build plan with phase folders and one story file per task — phrases like "phased plan", "implementation plan", "break this into stories", "build plan for this proposal", "turn this proposal into something Claude Code can execute", or "give me a plan I can hand to an agent" should all trigger this skill, even if they don't say the word "phased". Also trigger when a user has uploaded a proposal-shaped document (architecture, design, product spec, RFC) and asks anything about how to actually build it. The output is a directory tree with CLAUDE.md, README.md, one folder per phase, and one Markdown file per story, archived as .tar.gz.
---

# Phased implementation plan from a proposal

Take a proposal or design document plus an MVP scope description and produce a phased build plan: a directory tree with `CLAUDE.md`, top-level `README.md`, one folder per phase, and one Markdown file per story, packaged as a `.tar.gz` the user can extract into a repo.

The goal is a plan where:

- Each story is small enough to land as a single PR.
- Each story is **self-contained**: narrative, TDD test plan, implementation hints, acceptance criteria, README updates, verification commands.
- Phases are **vertical slices** — each phase ends in something the user can run, not just code that compiles.
- The plan reads like notes from a senior engineer to themselves, not corporate ticket-speak.

## Workflow

### 1. Read the proposal completely

The proposal usually arrives as an uploaded file in `/mnt/user-data/uploads/` or as inline content. Read all of it before drafting anything — proposals frequently put critical architectural detail late in the document (auth model, persistence rules, deployment shape).

If the proposal is long, do multiple `view` calls covering the whole file. Don't skim. Pay particular attention to:

- The data model and persistence rules (especially multi-tenancy, RLS, encryption requirements).
- Auth and authz model (token format, RBAC, IdP integration).
- External surfaces (CLI, REST API, UI, MCP, anything the user or another system touches).
- Explicit "out of scope" or "post-MVP" markers — these define what the plan must *not* include.

### 2. Confirm or extract the MVP scope

The user supplies an MVP description. It should answer:

- What can the user **do** with the MVP at the end? (run a workload, ship a payment, etc.)
- What hard constraints apply from day 1? (multi-tenant, encrypted at rest, single binary, etc.)
- Which surfaces ship in MVP? (CLI only? CLI + UI? + MCP?)
- What's explicitly post-MVP?

If the user's description is fuzzy on any of these, ask one focused clarifying question via `ask_user_input_v0` — but only if it would meaningfully change the plan. Don't interrogate. If you can infer a sensible default from the proposal, do that and surface the assumption inline in the plan.

### 3. Decompose into phases

Aim for 4–7 phases. Decomposition rules:

- **Phase 0 is always foundations**: project bootstrap, schema, dev tooling, CI. No user-visible behavior — that's fine, it's the only phase that gets that pass.
- **Each later phase is a vertical slice** that ends in an observable capability. "Login works." "Workloads can be created." "A workload runs." "It runs in the browser."
- **Order phases so each one builds something demoable** on top of the previous. The user should be able to stop after any phase and have a coherent sub-product.
- **The final phase is often external integration**: MCP, public API, integration docs, plugins.
- **Stack horizontally inside a phase**: e.g. Phase 2 might cover the domain model + repo + REST + CLI for one resource, top to bottom. Don't split "all REST routes" and "all CLI commands" into separate phases — that creates phases nobody can use independently.

For deeper guidance on how to split phases and order stories within them, read `references/decomposition-principles.md`.

### 4. Decompose phases into stories

Each phase contains 3–7 stories. Story rules:

- **One story = one PR.** If it would obviously need to ship in two PRs, it's two stories.
- **Order stories so each one runs/tests on top of the previous.** Tests should be runnable mid-phase.
- **Front-load the contract.** Define interfaces (ports, schemas) before adapters that implement them. Define the domain before the storage.
- **Defer polish.** Error messages, output formatting, observability come at the end of the relevant phase, not in the middle.

### 5. Write the files

The plan writes to a working directory like `/home/claude/<project>-mvp-plan/`. Files in this exact order:

1. `CLAUDE.md` — agent contract (template in `references/claude-md-template.md`).
2. `README.md` — top-level reading guide (template in `references/top-readme-template.md`).
3. `phase-NN-<slug>/README.md` for each phase (template in `references/phase-readme-template.md`).
4. `phase-NN-<slug>/story-NN-MM-<slug>.md` for each story (template in `references/story-template.md`).

Naming:
- Phases: `phase-00-bootstrap`, `phase-01-identity-and-rbac`, etc. Two-digit zero-padded.
- Stories: `story-NN-MM-<short-slug>.md` where `NN` matches the phase and `MM` is the story index in the phase.

### 6. Bundle and present

```bash
cd /home/claude && tar -czf /mnt/user-data/outputs/<project>-mvp-plan.tar.gz <project>-mvp-plan/
```

Then call `present_files` with the tar.gz path.

## What each file looks like

The four templates in `references/` are authoritative — read them before writing the corresponding file. Brief structural reminders:

**CLAUDE.md** — the contract another agent (Claude Code) will read on every turn. Stack constraints, layering rules, persistence contract (especially RLS / multi-tenant rules), auth contract, public CLI/API surface enumeration, definition of done.

**Top-level README.md** — reading guide for the human reviewer. What MVP means, prerequisites, file layout, recommended workflow, why this ordering, definition of done as an end-to-end shell script.

**Phase README.md** — what this phase delivers, why this story ordering, table of stories, exit criteria, what's deferred from this phase to a later one (or post-MVP).

**Story file** — narrative (the why, ties to proposal sections), pre-requisites, description with code/SQL/YAML samples, numbered TDD plan (RED-first), implementation hints, acceptance criteria as checkboxes, README updates (what to add to phase/top-level README when this lands), verification commands with expected output.

## Style guide

The plan is read by both a human reviewer and a coding agent. Both benefit from the same things:

- **Direct and practitioner-grounded.** "Use Postgres RLS — set `app.tenant_id` inside the transaction, never write `WHERE tenant_id = ?` in app code." Not "Implement comprehensive multi-tenancy isolation strategy."
- **Concrete code/SQL/YAML samples** in fenced blocks. A 30-line SQL migration sketch is more useful than three paragraphs of prose about it.
- **Out-of-scope items explicitly named.** Every story should list what it deliberately does *not* do. This prevents scope creep and tells the agent it doesn't need to invent anything beyond the brief.
- **Verifiable acceptance criteria.** Checkbox items that can each be checked individually. "All 12 tests pass." "Migration applies cleanly on a fresh database." "`faktotum login` exits 0 with a credentials file."
- **Verification commands at the end of every story** with expected output. The agent should know what success looks like before it starts.

Avoid:

- Hype framing ("revolutionary", "powerful", "best-in-class").
- Long preambles before the substance.
- Defensive hedging ("ideally", "if possible", "consider", "you might want to"). Be specific. If a thing is genuinely optional, mark it so.
- Bullet salad. Prose where prose works; bullets only for genuinely list-shaped content.

## Length targets

These are guidelines, not hard limits — go longer if the content needs it.

- `CLAUDE.md`: 100–200 lines.
- Top-level `README.md`: 80–150 lines.
- Phase `README.md`: 40–90 lines.
- Story file: 150–350 lines. Stories with significant SQL, schema, or protocol detail can run 350–450; stories that are purely "wire X to Y" can be 100–150.

If a story is approaching 500 lines, consider whether it's actually two stories.

## Common decompositions

These aren't prescriptive — they're patterns that show up often and are useful as starting points. Adapt to the proposal's actual shape.

**For a backend service with CLI + UI + agent integration** (the canonical case):

1. Phase 0 — Bootstrap (project skeleton, schema, dev tooling, CI).
2. Phase 1 — Identity and RBAC (login, tenant model, authz).
3. Phase 2 — Core domain CRUD (the primary resource: store, REST, CLI).
4. Phase 3 — Execution / behavior (whatever the service actually does at runtime).
5. Phase 4 — Web UI.
6. Phase 5 — Agent / external integration (MCP, public API, etc.).

**For a library or framework**:

1. Phase 0 — Bootstrap and core types.
2. Phase 1 — The minimal end-to-end happy path.
3. Phase 2 — Surface area expansion (more types, edge cases).
4. Phase 3 — Performance / hardening.
5. Phase 4 — Documentation and examples.

**For a data pipeline**:

1. Phase 0 — Bootstrap, infra, observability stubs.
2. Phase 1 — Source ingestion.
3. Phase 2 — Transformation layer.
4. Phase 3 — Sink / output.
5. Phase 4 — Monitoring, alerting, ops.

## Decomposition rules of thumb

- **If a phase has only one story, it's probably part of the next phase.** Combine.
- **If a phase has more than 8 stories, it's probably two phases.** Split — usually along a "what the user can demo" line.
- **A phase that produces nothing demoable is suspicious.** Either it's truly foundational (Phase 0) or it should be merged into the phase whose demo it enables.
- **Cross-cutting concerns** (logging, OTel, error formatting) belong in the phase that *first* needs them, not in a phase of their own. Reference back to that phase from later stories.

## Example proposals to plans

For a worked example of the output style, read `references/example-mini.md`. It's a tiny end-to-end illustration showing what a single phase looks like for a hypothetical project — useful as a pattern to imitate.

## Output checklist

Before bundling, verify:

- [ ] `CLAUDE.md` exists and enumerates stack, layering, persistence/auth contracts, and the public surface.
- [ ] Top-level `README.md` includes the "definition of done" end-to-end shell script.
- [ ] Every phase folder has a `README.md` and at least one story.
- [ ] Every story has all 7 sections from the template.
- [ ] Story numbering is consistent: `story-NN-MM-<slug>.md` where NN matches the phase number.
- [ ] No story references a future story without saying "(post-MVP)" or "(story NN-MM)".
- [ ] The tar.gz extracts to a single top-level folder (not loose files).

Then `present_files` the tar.gz.
