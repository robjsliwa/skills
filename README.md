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
    design-interview/
    vertical-slice-phasing/
    phased-implementation-plan/
  productivity/       # general workflow tools (reserved — no skills yet)
  gamedev/            # game development skills (reserved — no skills yet)
  deprecated/         # superseded skills, kept for reference
    init-go-project/
```

| Category | Purpose | Skills |
|---|---|---|
| `engineering` | Code-focused skills for day-to-day development | `go-boilerplate`, `let-me-code`, `design-interview`, `vertical-slice-phasing`, `phased-implementation-plan` |
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
