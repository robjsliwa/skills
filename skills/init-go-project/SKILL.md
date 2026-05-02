---
name: init-go-project
description: >
  Manually-invoked installer that scaffolds a production-ready Go REST API
  service in the current directory using hexagonal architecture, standard
  library net/http, slog, OpenTelemetry (traces/metrics/logs), JWT/OAuth
  validation middleware (JWKS-aware), request-payload validation via
  go-playground/validator, code-first OpenAPI/Swagger via swaggo/swag,
  and a port/adapter database layer supporting none, postgres, mysql,
  sqlite, or mongodb. Architecture: deterministic shell scripts handle
  directory creation and asset installation; Claude focuses on Go code
  generation. Server and CLI build into separate binaries from the same
  repo. Generates CLAUDE.md with rationale journal workflow, ARCHITECTURE.md,
  MODULE_MAP.md, GitHub Actions CI, and a native git pre-commit hook.
  Usable interactively or non-interactively (e.g., from Backstage via
  `claude -p --permission-mode bypassPermissions`).
disable-model-invocation: true
---

# init-go-project — Go Service Scaffolder (v3)

A manually-invoked installer that creates a production-ready Go REST API
service skeleton.

**Architecture principle:** deterministic work runs in shell scripts;
LLM judgment goes into Go code generation only. This makes the skill
reliable and reduces the chance that files get silently skipped.

**When invoked, immediately begin the Workflow at Step 1.**

## Workflow

### Step 1: Gather Parameters

Accept parameters from the invocation message OR ask interactively.

**Required:**
- `project_name` — short name (binary name for server, default service ID)
- `module` — Go module path (e.g., `github.com/owner/{project_name}`)
- `database` — `none` | `postgres` | `mysql` | `sqlite` | `mongodb`
- `description` — one-paragraph project description (or `description_file`)
- `include_cli` — `true` or `false`

**Conditional:**
- `cli_name` — name for the CLI binary (required when `include_cli=true`).
  This becomes the directory `cmd/{cli_name}/` and the binary name
  `bin/{cli_name}`. Suggested: keep it distinct from `project_name` to
  make it obvious which binary is which (e.g. `project_name=faktotum`,
  `cli_name=fakctl`). If the user says `include_cli=true` but doesn't
  provide a name, ask.

**Optional:**
- `target_dir` — default: current working directory
- `non_interactive` — set to `true` for headless/automated use; skips
  the confirmation prompt. (Replaces v2's `yes=true`.)
- `git_init` — default `true`
- `auth_enabled` — default `true` (set `false` to disable JWT middleware
  out of the box; can be toggled later via env)

**Collection logic:**

1. Parse the invocation for `key=value` pairs and natural-language
   equivalents ("use postgres", "with cli named fakctl", etc.)
2. If `description_file` is given, read it and use its contents
3. For any required parameter still missing, ask **one question at a
   time** in this order: project_name, module, database, description,
   include_cli, cli_name (only if include_cli=true)
4. **Derive the primary domain entity** from the `description`. The
   entity is the core resource the API manages. Examples:
   - "Service for managing inventory items" → entity = `Item`
   - "Task management API" → entity = `Task`
   - "Certificate lifecycle management" → entity = `Certificate`
   - "User notification service" → entity = `Notification`
   If the description is ambiguous, ask. Use PascalCase for the struct
   (`Item`), camelCase for variables (`item`), snake_case for tables
   (`items`), and kebab-case for URL paths (`/api/v1/items`).
5. Move to Step 2 with summary

For headless invocation, ALL required parameters must be provided plus
`non_interactive=true`. See `references/headless-invocation.md`.

### Step 2: Confirm

Print a summary table:

```
About to scaffold:
  Project name:    <project_name>
  Module path:     <module>
  Target dir:      <target_dir>
  Database:        <database>
  Domain entity:   <Entity> (plural: <entities>)
  Include CLI:     <include_cli>
  CLI name:        <cli_name or N/A>
  Auth enabled:    <auth_enabled>
  Description:     <first 80 chars>...
```

If `non_interactive=true`, proceed. Otherwise wait for explicit confirmation.

### Step 3: Run bootstrap.sh

Locate the skill directory (typically `~/.claude/skills/init-go-project/`).
Then invoke:

```bash
{SKILL_DIR}/scripts/bootstrap.sh \
  --project-name="$PROJECT_NAME" \
  --module="$MODULE" \
  --database="$DATABASE" \
  --include-cli="$INCLUDE_CLI" \
  --cli-name="${CLI_NAME:-}" \
  --auth-enabled="$AUTH_ENABLED" \
  --target-dir="$TARGET_DIR" \
  --git-init="$GIT_INIT"
```

This creates the directory tree, validates Go version, runs `go mod init`,
and (optionally) initializes git. If it fails, surface the error and stop.

### Step 4: Run install-static.sh

```bash
{SKILL_DIR}/scripts/install-static.sh \
  --skill-dir="{SKILL_DIR}" \
  --target-dir="$TARGET_DIR" \
  --project-name="$PROJECT_NAME" \
  --module="$MODULE" \
  --include-cli="$INCLUDE_CLI" \
  --cli-name="${CLI_NAME:-}" \
  --database="$DATABASE" \
  --description="$DESCRIPTION"
```

This copies the Makefile, Dockerfile, docker-compose, GitHub Actions
workflow, pre-commit hook, golangci config, env example, gitignore,
and README.md.
All `{{PLACEHOLDER}}` substitutions happen here, deterministically.

### Step 5: Generate Go Code (the LLM-judgment part)

This is where Claude's actual reasoning is needed. Read these references
in order:

1. `references/architecture.md` — hexagonal layout rules
2. `references/database-adapters.md` — code for the chosen DB
3. `references/auth-middleware.md` — JWT middleware (if `auth_enabled=true`)
4. `references/validation.md` — request validation pattern
5. `references/openapi-annotations.md` — swag annotations
6. `references/binary-separation.md` — server vs CLI binary split

Then generate ALL of the following Go files. Do not skip any. The verify
step will catch omissions, but it's better to get them right the first time.

**IMPORTANT — Domain Entity:** Throughout the generated code, use the
domain entity name derived in Step 1 (e.g., `Task`, `Certificate`,
`Order`). The reference docs use `Widget` as a pattern placeholder —
do NOT generate Widget/WidgetRepository/WidgetService unless the user's
description actually calls for widgets. Replace every occurrence:
- `Widget` → `{Entity}` (e.g., `Task`)
- `WidgetRepository` → `{Entity}Repository` (e.g., `TaskRepository`)
- `WidgetService` → `{Entity}Service` (e.g., `TaskService`)
- `CreateWidgetRequest` → `Create{Entity}Request` (e.g., `CreateTaskRequest`)
- `widgets` (table/collection) → `{entities}` (e.g., `tasks`)
- `/api/v1/widgets` → `/api/v1/{entities}` (e.g., `/api/v1/tasks`)
- `widgets:read`/`widgets:write` → `{entities}:read`/`{entities}:write`

Also adapt the struct fields to match the entity. For example, a
`Certificate` entity would have fields like `SerialNumber`, `Issuer`,
`ExpiresAt` rather than generic `Name`/`Description`. Use the project
description to infer appropriate fields.

**Required (always):**

- `pkg/domain/types.go` — `{Entity}` struct (no validation tags)
- `pkg/domain/ports.go` — `{Entity}Repository` interface
- `pkg/domain/errors.go` — `ErrNotFound`, `ErrAlreadyExists`
- `internal/core/service.go` — `{Entity}Service`
- `internal/core/service_test.go` — table-driven tests using memory store
- `internal/config/config.go` — Config struct with HTTP, Logging, OTel,
  DB, and Auth sub-structs; `Load()` and `Validate()`
- `internal/adapters/http/server.go` — `*http.Server` setup
- `internal/adapters/http/routes.go` — route registration
- `internal/adapters/http/handlers.go` — handlers WITH swag annotations
- `internal/adapters/http/middleware.go` — RequestID, Logger, Recoverer, CORS
- `internal/adapters/http/dto.go` — DTOs with `validate:` tags
- `internal/adapters/http/decode.go` — `decodeAndValidate` helper
- `internal/adapters/http/respond.go` — `respondJSON`, `respondError`
- `internal/adapters/http/health.go` — `/healthz`, `/readyz`
- `internal/adapters/http/swagger.go` — Swagger UI mount
- `internal/adapters/http/handlers_test.go` — handler tests
- `internal/adapters/store/memory.go` — in-memory repository
- `internal/adapters/store/memory_test.go` — table-driven tests
- `internal/adapters/telemetry/otel.go` — OTel setup
- `internal/adapters/telemetry/slog.go` — slog with trace correlation
- `cmd/server/main.go` — entry point with full lifecycle and swag metadata

**Conditional:**

- `cmd/{cli_name}/main.go` — cobra root with `version` subcommand
  (only if `include_cli=true`). See
  `references/binary-separation.md` for the security boundary —
  the CLI binary is built independently and the server's Dockerfile
  does NOT include it.
- `internal/auth/auth.go` — JWT middleware (if `auth_enabled=true`)
- `internal/auth/auth_test.go` — table-driven HS256 tests
- DB-specific store: `internal/adapters/store/sql.go` (postgres/mysql/sqlite)
  OR `internal/adapters/store/mongo.go` (mongodb). For SQL DBs, also
  generate `migrations/001_create_{entities}.up.sql` and `down.sql`.

### Step 6: Generate Documentation

Note: `README.md` is installed by `install-static.sh` in Step 4
(deterministic template). Do not regenerate it here.

- `docs/ARCHITECTURE.md` — derived from `references/architecture.md`,
  customized to project name and DB
- `docs/MODULE_MAP.md` — initial map of generated packages
- `CLAUDE.md` — see Step 7

### Step 7: Generate CLAUDE.md

Read `references/workflow-template.md`. The generated CLAUDE.md must contain:

1. Project header (name, module, one-line description)
2. Doc imports at top:
   ```
   @docs/ARCHITECTURE.md
   @docs/MODULE_MAP.md
   ```
3. Project structure tree (reflecting the actual scaffolded directories,
   including `cmd/server/` and `cmd/{cli_name}/` if CLI was requested)
4. Architectural Layers section
5. Coding conventions (slog only, error wrapping, decodeAndValidate for
   bodies, swag annotations on all handlers, regenerate spec via
   `make swagger`)
6. Test commands (`make test`, `make test-integration`)
7. Story Implementation Workflow (from workflow-template.md)
8. Keeping Docs Current section

### Step 8: Run verify.sh (with fix-and-retry)

```bash
{SKILL_DIR}/scripts/verify.sh \
  --target-dir="$TARGET_DIR" \
  --database="$DATABASE" \
  --include-cli="$INCLUDE_CLI" \
  --cli-name="${CLI_NAME:-}" \
  --auth-enabled="$AUTH_ENABLED"
```

This script:
1. Checks every expected file exists (fails loudly with a list if any missing)
2. Runs `swag init` to generate the OpenAPI spec (must happen first so
   `docs/docs.go` exists before build resolves dependencies)
3. Runs `go mod tidy`
4. Runs `go build ./...`
5. Runs `go test ./...`
6. Smoke-tests `go run ./cmd/server` to verify the server starts

**You MUST NOT stop on failure.** Instead, follow this retry loop
(up to 3 attempts total):

1. If verify.sh reports **missing files**: generate the missing files
   and re-run verify.sh.
2. If `go build` fails: read the compiler errors, fix the offending
   Go files (import paths, type mismatches, missing methods, etc.),
   and re-run verify.sh.
3. If `go test` fails: read the test output, fix either the test or
   the implementation (whichever is wrong), and re-run verify.sh.
4. If `swag init` fails: check that handler annotations are well-formed
   (see `references/openapi-annotations.md`), fix them, and re-run.

After each fix, re-run the FULL verify.sh (not just the failing step),
because fixes can introduce new issues.

**Only stop and report to the user if all 3 attempts fail.** In that
case, show the final error output and explain what you tried.

**Do NOT delete or skip files that were created by the scripts**
(README.md, Makefile, .env.example, docker-compose.yml, etc.). If
verify.sh reports a script-installed file as missing, something went
wrong in an earlier step — investigate and re-run the install step,
do not regenerate those files from scratch.

### Step 9: Run finalize.sh

```bash
{SKILL_DIR}/scripts/finalize.sh --target-dir="$TARGET_DIR"
```

Installs the pre-commit hook (sets `core.hooksPath`), stages all files,
and creates the initial git commit.

### Step 10: Print Summary

Print:
- File count from `git ls-files | wc -l`
- Path to scaffolded project
- Next steps:
  ```
  cd {target_dir}
  cp .env.example .env
  # Edit .env (set AUTH_JWKS_URL or AUTH_HMAC_SECRET if AUTH_ENABLED=true)
  make compose-up      # if database != none
  make migrate-up      # if SQL database
  make run
  open http://localhost:8080/docs/
  ```
- Pointer to `CLAUDE.md` for the rationale journal workflow

## Constraints

- Never overwrite existing source files (bootstrap.sh enforces this)
- Never write `.env` (only `.env.example`)
- Never delete files created by the scripts (README.md, Makefile,
  .env.example, .gitignore, .golangci.yml, deploy/*, .github/*, etc.)
- Stick to the chosen DB (don't pull multiple DB drivers)
- The OpenAPI spec is generated, not hand-written
- Auth middleware must support `AUTH_ENABLED=false`
- Server and CLI are independent binaries; the server's runtime image
  must not contain CLI code (see `references/binary-separation.md`)
- Do NOT hardcode `Widget`/`Todo` as the domain entity — derive the
  entity name from the project description. The reference docs use
  `Widget` only as a pattern illustration.

## Why scripts?

Earlier versions of this skill asked Claude to perform every step,
including rote work like "create directory `.github/workflows/`" and
"copy file X to Y." That worked most of the time, but files would
occasionally get skipped under the cognitive load of generating
hundreds of lines of Go code in the same response.

v3 separates concerns:
- **Shell scripts** handle file operations, directory creation, template
  substitution, and verification. These are deterministic and testable.
- **Claude** handles Go code generation, architectural reasoning, and
  the parts of CLAUDE.md/README.md that need genuine adaptation to the
  project description.

If you want to add a new asset (say, a `.editorconfig` or a Helm chart),
you put it in `assets/` and add a line to `install-static.sh`. You don't
edit a long instruction document and hope Claude remembers.
