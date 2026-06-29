# Engineering Skills

Engineering skills for Claude Code and other AI coding agents. Each skill is a
self-contained directory with a `SKILL.md` that Claude Code loads as an on-demand
slash command.

## Install

```bash
npx skills@latest add robjsliwa/skills
```

This symlinks every skill into `~/.claude/skills/` and makes it available in
any Claude Code session. Restart Claude Code after installing.

**Requirements:** [Claude Code](https://claude.ai/code), Node.js (for `npx`)

## Repository layout

Skills are grouped under `skills/` by functional category. New skills slot into
the category that best fits them.

```
skills/
  engineering/        # code-focused skills for day-to-day development
    go-boilerplate/
    let-me-code/
    planning-loop/
    write-requirements/
    design-interview/
    solution-design/
    vertical-slice-phasing/
    elaborate-current-phase/
    phased-implementation-plan/
  productivity/       # general workflow tools (reserved — no skills yet)
  gamedev/            # game development skills (reserved — no skills yet)
  deprecated/         # superseded skills, kept for reference
    init-go-project/
```

| Category | Purpose | Skills |
|---|---|---|
| `engineering` | Code-focused skills for day-to-day development | `go-boilerplate`, `let-me-code`, `planning-loop`, `write-requirements`, `design-interview`, `solution-design`, `vertical-slice-phasing`, `elaborate-current-phase`, `phased-implementation-plan` |
| `productivity` | General workflow tools not specific to coding | _(reserved — none yet)_ |
| `gamedev` | Game development skills | _(reserved — none yet)_ |
| `deprecated` | Superseded skills, kept for reference | `init-go-project` |

## Engineering

### `go-boilerplate`

Scaffolds a new Go REST API service from a fixed boilerplate using Chi, OpenTelemetry, and Swagger.

**What it generates:**

- Full Go module with Chi router and middleware
- OpenTelemetry tracing and metrics wiring
- Code-first Swagger/OpenAPI docs via swaggo
- Makefile, Dockerfile, and docker-compose
- GitHub Actions CI workflow

**Parameters:**

| Parameter | Required | Default | Description |
|---|---|---|---|
| `project_name` | Yes | — | Project name in kebab-case, e.g. `my-service` |
| `github_user` | Yes | — | GitHub username or org that will own the repo |
| `description` | Yes | — | One-sentence description of the service |
| `dest_dir` | No | `.` (current directory) | Directory to install the project files into |
| `module_path` | No | `github.com/{github_user}/{project_name}` | Full Go module path (override if not on GitHub) |

**Usage (interactive):**

```
# Inside a Claude Code session:
Run the go-boilerplate skill.
```

Claude will ask for any missing required parameters one at a time.

**Usage (with parameters):**

```
Run go-boilerplate with project_name=widget-svc,
github_user=acme, description="Service for managing inventory widgets."
```

**Headless / CI usage:**

```bash
mkdir my-service && cd my-service
claude -p --permission-mode bypassPermissions \
  "Run go-boilerplate skill non-interactively:
   project_name=my-service
   github_user=acme
   description='Service for tracking certificate lifecycles.'"
```

See `skills/engineering/go-boilerplate/INSTALL.md` for full installation details.

### `let-me-code`

Generates a TDD-structured tutorial markdown file that guides you to type each line of code yourself for learning and muscle memory.

**What it does:**

- Plans the feature with you, then produces a `TUTORIAL.md` (or `docs/tutorials/<feature>.md`) — no source files written
- Each step is one RED→GREEN cycle: type the failing test, watch it fail, type the minimal implementation, watch it pass
- Code blocks are sized for typing (10–30 lines), never for copy-pasting
- Ends with a refactor section and "what's next" suggestions

**When to use:**

```
# "Teach me to build X"
# "I want to code it myself"
# "Walk me through step by step"
# "Don't write the code for me"
```

**Usage:**

```
# Inside a Claude Code session:
/let-me-code
```

Claude will ask what feature or concept you want to learn, confirm the language and test framework, agree on which behaviors to cover and in what order, then write the tutorial.

### `planning-loop`

A user-invoked **orchestrator** that names the whole plan-to-build loop and tells you
which step to invoke next. It points; it never does the downstream step itself.

**What it does:**

- Explains the full loop and where the work currently sits
- Gives a light-path vs. heavy-path decision rule (judge by architectural weight, not
  diff size)
- Maps "where you probably are" to the single next skill to invoke, with a one-line reason
- Routes to the model-invoked planning skills (`write-requirements`, `solution-design`,
  `elaborate-current-phase`) and points at the user-invoked ones

**When to use:**

```
# "Where do I start? / what comes next?"
# "What skill do I use for this?"
# "How does the planning pipeline fit together?"
# A rough idea, unsure whether you need grilling, a PRD, a design, phasing, or just code
```

**Usage:**

```
# Inside a Claude Code session:
/planning-loop
```

For the full light-path / heavy-path guide, see
[How to use these skills](#how-to-use-these-skills) below.

### Planning workflow: `design-interview` → `vertical-slice-phasing` → `phased-implementation-plan`

These three skills form a pipeline that takes a rough idea all the way to a build
plan an agent can execute. Each one is also useful on its own — pick the stage
that matches where you actually are.

| Stage | Skill | Answers | Output |
|---|---|---|---|
| 1. Decide **what** to build | `design-interview` | What is the architecture / approach? | A findings document |
| 2. Decide **in what order** | `vertical-slice-phasing` | What do we build first, and how do we phase it? | A phased design document |
| 3. Decide **the exact tasks** | `phased-implementation-plan` | What are the per-story PRs? | A directory tree of phase/story files |

The boundary between them matters: `design-interview` resolves the architecture,
`vertical-slice-phasing` decides the build order assuming the architecture is
settled, and `phased-implementation-plan` mechanically explodes a settled plan
into story files. If you start at stage 2 or 3 you can skip the earlier ones, but
don't use a later skill to redo an earlier skill's job.

### `write-requirements`

Turns a finished grilling or `design-interview` session into a detailed,
template-driven requirements document (a PRD with teeth) — the **WHAT and the WHY**,
never the mechanism — then hands it to `to-prd` to file in the issue tracker.

**What it does:**

- Writes to a bundled `requirements-template.md` and fills every section, making the
  ones people skip (non-goals, non-functional rows, failure modes) visibly absent if
  omitted
- Forces the dimensions that later cause rewrites: latency budgets, failure behavior,
  trust boundaries, retention, the second caller
- Numbers behavioral requirements (R1, R2, …) so the design, phasing, and stories can
  all reference them by id
- Pairs every happy-path requirement with a failure requirement, and ties acceptance
  criteria to requirement ids
- Refuses to write from a cold start: if no grilling happened, it sends you to do that
  first

**When to use:**

```
# "Write the PRD / capture the requirements / write the spec"
# "Write up what we just decided"
# Requirements that keep coming out too thin or reach to-issues underspecified
```

This is model-invoked and runs **before** `to-prd`, not instead of it: it produces the
body, `to-prd` files it. It does not decide the technical approach — that is
`solution-design`, which comes after.

### `design-interview`

Drives a rigorous, **one-question-at-a-time** interview to nail down a design,
architecture, plan, or any decision-heavy problem before anything gets written
up, then captures the agreed design in a markdown findings document.

**What it does:**

- Reads every attachment, codebase, and prior decision first, so it only asks
  what genuinely needs your judgment
- Maps the decision tree, then walks it in dependency order — one coupled
  decision per turn
- Every question carries a **recommendation**, its reasoning, the tradeoff, and
  the soft spot where you might reasonably overrule it
- Tracks what's *settled*, what's *deferred*, and the *designed seams* (interfaces
  left in place so future work is additive)
- Ends by writing a findings document capturing the decisions **and the reasoning**

**When to use:**

```
# "Help me think this through / interview me"
# "Let's work out the requirements"
# "Walk the design tree / nail down the approach"
# A branching set of coupled decisions (auth, data model, API surface, infra)
```

Don't use it for a single well-posed question or when you want a fast one-shot
answer.

**Usage:**

```
# Inside a Claude Code session:
/design-interview
```

### `solution-design`

Turns an agreed requirements document into a detailed technical design document — the
**HOW** — and inserts the design artifact the Pocock chain skips between `to-prd` and
`to-issues`, so issues inherit a chosen mechanism instead of inventing one per agent.

**What it does:**

- Writes to a bundled `design-template.md`: ports and adapters, domain model, data,
  control flow, concurrency, observability, trust boundaries
- Makes the **deterministic-versus-probabilistic split** explicit and defends it —
  anything that can be deterministic should be, in compiled code
- Defines ports before adapters, and names the **designed seams** that make later phase
  deferrals safe (a swap, not a rewrite)
- Keeps a stdlib-first dependency policy: every new dependency justified against the
  standard library, or there are none
- Traces every decision back to a requirement id, and writes ADRs under `docs/adr/`
  only for hard-to-reverse, surprising commitments
- Invokes `design-interview` for genuinely coupled, branching decisions rather than
  guessing through the tree

**When to use:**

```
# "Design this / how should we build this"
# "Work out the architecture / write the design doc"
# Requirements are in hand and you're about to break work into issues, but there's no design yet
```

This is model-invoked and produces a design, not a build order. Phasing the design is
the next step (`vertical-slice-phasing`).

### `vertical-slice-phasing`

Turns settled requirements or design docs into a **phased implementation design**
built from thin vertical slices, by interviewing you about sequencing one decision
at a time. This decides **build order**, not the architecture.

**What it does:**

- Assumes the architecture is fixed input; extracts the core thesis, acceptance
  criteria, load-bearing seams, and constraints from the docs
- Walks the phase tree in dependency order, recommending where each cut line falls
- Applies a "walking skeleton first" philosophy: phase one is a thin end-to-end
  slice that proves the riskiest claim; every later phase thickens it with usable,
  demoable capability rather than completing horizontal layers
- Maps acceptance criteria to phase boundaries and names the designed seams
- Writes a phased design document a human reads (not story files)

**When to use:**

```
# "How should I build this? / what first?"
# "Phase the work / sequence it into milestones / work out a build order"
# You have a draft phase list you want pressure-tested
```

Run `design-interview` first if the architecture itself is still open.

**Usage:**

```
# Inside a Claude Code session:
/vertical-slice-phasing
```

### `elaborate-current-phase`

Details **exactly one phase** of a phased design down to implementable stories or
issues, leaves later phases as sketches, and re-derives the next phase against the real
codebase once the current one ships. This is progressive elaboration.

**What it does:**

- Detects the current phase (first unbuilt, or the one you name); treats built phases as
  ground-truth evidence and reads their real code, not just the original design
- Explodes only the current phase, delegating the actual work to
  `phased-implementation-plan` (a story-file bundle) or `to-issues` (tracker issues) —
  constrained to one phase
- Deliberately refuses to detail phases beyond the current one, because building the
  earlier ones changes what the later ones should be
- Doubles as the **re-entry point**: invoke it again when a phase ships to re-derive the
  next phase, flagging any drift from the original design — and recommending a re-run of
  `vertical-slice-phasing` if the drift is large

**When to use:**

```
# "Detail phase 1 / what do I build first / explode this phase"
# "Now do the next phase" (after a phase has shipped)
```

This is model-invoked and is the loop's return arrow — see
[How to use these skills](#how-to-use-these-skills). Pick **one** exploder
(`to-issues` or `phased-implementation-plan`), not both.

### `phased-implementation-plan`

Turns a proposal or design document plus an MVP scope into a phased,
**story-by-story** implementation plan — a directory tree with `CLAUDE.md`,
`README.md`, one folder per phase, and one Markdown file per story, packaged as a
`.tar.gz` you can extract into a repo.

**What it generates:**

- 4–7 phases (Phase 0 is foundations; every later phase is a demoable vertical slice)
- 3–7 stories per phase, each sized to land as a single PR
- Each story is self-contained: narrative, TDD test plan (RED-first), implementation
  hints, checkbox acceptance criteria, README updates, and verification commands
- A `CLAUDE.md` contract another agent reads on every turn (stack, layering,
  persistence/auth rules, public surface, definition of done)
- Bundled reference templates for each file type live in the skill's `references/`

**When to use:**

```
# "Break this into stories / give me a build plan"
# "Turn this proposal into something Claude Code can execute"
# "Give me a plan I can hand to an agent"
```

This is the mechanical explosion step — run it once the architecture and phasing
are settled.

**Usage:**

```
# Inside a Claude Code session:
/phased-implementation-plan
```

## How to use these skills

The planning skills compose into a single plan-to-build loop. `planning-loop` is the
router that names this loop and tells you what to invoke next; the guide below is that
same map in full.

> **External dependency.** This loop is built to extend the Matt Pocock skill chain.
> The steps `grill-me`, `to-prd`, `to-issues`, `tdd`, and `story-review` are **not**
> shipped in this repo — install them separately (e.g. `mattpocock/skills`). The
> in-repo skills the loop uses are `planning-loop`, `write-requirements`,
> `design-interview`, `solution-design`, `vertical-slice-phasing`,
> `elaborate-current-phase`, and `phased-implementation-plan`.

### Step 0: Pick the path

Judge by architectural weight, not diff size. If you could open the editor right now
and the only question is where the first test goes, take the light path. If you cannot
name the ports without thinking, or the work has an obvious phase-one-versus-later
split, or a wrong call now means a rewrite later, take the heavy path.

### Light path (a single vertical slice, no real design choice)

1. `grill-me` to align on what you are building.
2. `to-issues` to break it into vertical-slice issues.
3. `tdd` to build each, RED test first.

This is the stock Pocock chain. Do not add ceremony to it.

### Heavy path (architecture, a contract others depend on, or multiple phases)

1. **Align.** `grill-me` for a quick pass, or `design-interview` when the decisions are
   coupled and you want a durable findings doc.
2. **Requirements.** `write-requirements` to fill the requirements template, then
   `to-prd` to file it in the issue tracker. This is the WHAT.
3. **Design.** `solution-design` to turn the requirements into a design doc: ports,
   adapters, the deterministic/probabilistic split, seams, ADRs. It invokes
   `design-interview` for any coupled decisions. This is the HOW.
4. **Phase.** `vertical-slice-phasing` to turn the design into a build order of
   walking-skeleton-first phases. This is the ORDER.
5. **Elaborate the current phase only.** `elaborate-current-phase`. It governs scope to
   one phase and calls your chosen exploder (see below) to produce the issues or
   stories for that phase. Later phases stay sketches.
6. **Build.** `tdd` per issue or story, with `story-review` as the gate before you
   build anything risky.
7. **Re-derive the next phase.** Once the phase ships, invoke `elaborate-current-phase`
   again. It reads the phase's real code as ground truth, pulls the next phase's sketch,
   and re-derives it against what now exists, flagging any drift. If the drift is large,
   it tells you to re-run `vertical-slice-phasing` on the remaining phases rather than
   build to a stale map.

Repeat steps 5 through 7 until the last phase is done. That is the loop:

```
align → write-requirements → to-prd → solution-design → vertical-slice-phasing
   → elaborate-current-phase → to-issues → tdd → story-review
                  ▲                                      │
                  └──────── re-derive next phase ────────┘
```

### Pick one exploder, not both

`elaborate-current-phase` delegates the actual exploding. Choose one per project:

- `to-issues` if you want tracker issues tagged HITL or AFK for downstream autonomous
  execution.
- `phased-implementation-plan` if you want rich self-contained story files as a bundle.

Do not run both. With `vertical-slice-phasing` now doing the phase decomposition,
keeping two exploders is redundant.

### What is manual and what is automated

The planning steps (1 through 5) are you-in-the-loop by design. Requirements, design,
phasing, and judging whether the design has drifted are exactly the decisions you do
not want automated away. The re-derive in step 7 is also manual: you invoke it at the
phase boundary, because that boundary is the cheapest place to notice the design went
wrong.

The autonomy lives downstream and is stock Pocock. `to-issues` tags each issue AFK or
HITL. AFK issues feed a Ralph-style loop where an agent pulls an issue, runs `tdd`,
commits, and opens a PR with no involvement from you. So the planning loop's job is to
hand that loop a clean, dependency-sorted set of AFK-eligible issues for one phase at a
time.

### If a step keeps getting skipped

The self-check lists in these skills are descriptive, which an agent can rationalize
past. To harden a step you see getting cut, add this near the top of that skill:

> Before starting, create a tracked task for each item in the self-check below. Mark
> each complete or explicitly skipped before handing off. Do not hand off with an
> unresolved task.

That turns the checklist into materialized tasks the agent must account for. Apply it
only to the one or two steps that actually drift; gating every step gets annoying fast.

## Deprecated

These skills are superseded but kept for reference. Prefer the maintained
alternatives noted below.

### `init-go-project`

Scaffolds a production-ready Go REST API service with hexagonal architecture.
**Superseded by [`go-boilerplate`](#go-boilerplate)** — use that for new projects.

**What it generates:**

- Full directory tree and Go module setup
- Hexagonal architecture: domain ports, application core, HTTP adapter, store adapter, telemetry
- Database layer for `none`, `postgres`, `mysql`, `sqlite`, or `mongodb`
- JWT/OAuth middleware (JWKS-aware, toggleable via `AUTH_ENABLED`)
- Request validation via `go-playground/validator`
- Code-first OpenAPI/Swagger via `swaggo/swag`
- Makefile, Dockerfile (server + optional CLI), docker-compose, GitHub Actions CI
- Native git pre-commit hook (gofmt, go vet, fast tests, spec drift check)
- `CLAUDE.md` with rationale journal workflow + symlinks for other AI tools (see below)

**Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `project_name` | Yes | Short name; becomes the server binary name |
| `module` | Yes | Go module path, e.g. `github.com/owner/project` |
| `database` | Yes | `none` \| `postgres` \| `mysql` \| `sqlite` \| `mongodb` |
| `description` | Yes | One-paragraph description; drives domain entity derivation |
| `include_cli` | Yes | `true` \| `false` — generates a separate operator CLI binary |
| `cli_name` | If CLI | Name for the CLI binary, e.g. `myctl` |
| `auth_enabled` | No | Default `true`; set `false` to disable JWT middleware |
| `target_dir` | No | Default: current working directory |
| `non_interactive` | No | Set `true` for headless/CI use |

**Usage (interactive):**

```
# Inside a Claude Code session:
Run the init-go-project skill.
```

Claude will ask for any missing parameters one at a time.

**Usage (with parameters):**

```
Run init-go-project with project_name=widget-svc,
module=github.com/acme/widget-svc, database=postgres,
include_cli=true, cli_name=widgetctl, auth_enabled=true.
Description: Service for managing inventory widgets across tenants.
```

**Headless / CI usage:**

```bash
mkdir my-service && cd my-service
claude -p --permission-mode bypassPermissions \
  "Run init-go-project skill non-interactively:
   project_name=my-service
   module=github.com/acme/my-service
   database=postgres
   include_cli=false
   auth_enabled=true
   description='Service for tracking certificate lifecycles.'
   non_interactive=true"
```

See `skills/deprecated/init-go-project/INSTALL.md` for full installation and Backstage scaffolder template.

## AI Tool Support

Every project generated by `init-go-project` includes config files for all
major AI coding assistants:

| File | Tool |
|---|---|
| `CLAUDE.md` | Claude Code (with `@import` syntax) |
| `AGENTS.md` | OpenAI Codex CLI |
| `GEMINI.md` | Google Gemini Code Assist |
| `.github/copilot-instructions.md` | GitHub Copilot |

`AGENTS.md`, `GEMINI.md`, and `.github/copilot-instructions.md` are git-tracked
symlinks pointing to `CLAUDE.md`. Edit `CLAUDE.md` to update guidance for all
tools at once.

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- Go 1.22+
- git

## License

MIT
