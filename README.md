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
  productivity/       # general workflow tools (reserved — no skills yet)
  gamedev/            # game development skills (reserved — no skills yet)
  deprecated/         # superseded skills, kept for reference
    init-go-project/
```

| Category | Purpose | Skills |
|---|---|---|
| `engineering` | Code-focused skills for day-to-day development | `go-boilerplate`, `let-me-code` |
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
