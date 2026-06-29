# Installing the init-go-project Skill (v3)

A manually-invoked Claude Code skill that scaffolds a production-ready
Go REST service. v3 separates deterministic file operations (shell
scripts) from LLM-judgment work (Go code generation), making the skill
substantially more reliable than earlier versions.

## What's new in v3

- **Deterministic shell scripts** handle directory creation, asset
  installation, and verification. Files no longer get silently skipped.
- **Server and CLI are separate binaries** in the same repo, with
  separate Dockerfiles. The production runtime image contains only the
  server binary; the CLI ships in a separate `*-ops` image meant for
  operator jumpboxes. See `references/binary-separation.md`.
- **`non_interactive=true`** replaces v2's confusing `yes=true` flag.
- **Verify step** checks every expected file exists before completing
  and fails loudly with a list if anything is missing.
- **`bypassPermissions`** is now the recommended permission mode for
  headless use — `acceptEdits` doesn't cover bash commands like
  `git init` and `go mod init`.

## Install

Skills live in `~/.claude/skills/` (user-scope) or `.claude/skills/`
(project-scope). For a project scaffolder, user-scope is right.

```bash
mkdir -p ~/.claude/skills
tar xzf init-go-project-v3.tar.gz -C ~/.claude/skills/

# Or copy directly:
cp -r init-go-project ~/.claude/skills/

# Verify:
ls ~/.claude/skills/init-go-project/
# Expected:
#   SKILL.md
#   INSTALL.md
#   references/      (~10 reference docs)
#   assets/          (~10 asset templates)
#   scripts/         (4 shell scripts: bootstrap, install-static, verify, finalize)
```

The shell scripts must be executable. The tarball preserves this, but if
you copy manually:

```bash
chmod +x ~/.claude/skills/init-go-project/scripts/*.sh
```

Restart Claude Code (or start a new session). The skill is manual-only
(`disable-model-invocation: true`).

## Interactive use

```bash
mkdir my-new-service && cd my-new-service
claude
```

In the prompt:

```
Run the init-go-project skill.
```

The skill asks in order: project_name, module, database, description,
include_cli (and cli_name if include_cli=true). Then summary and
confirmation before scaffolding.

To pre-supply parameters:

```
Run init-go-project with project_name=widget-svc,
module=github.com/robjsliwa/widget-svc, database=postgres,
include_cli=true, cli_name=widgetctl, auth_enabled=true.
Description coming next.
```

## Headless use (Backstage / CI)

Use `bypassPermissions` (NOT `acceptEdits`):

```bash
mkdir my-new-service && cd my-new-service

claude -p --permission-mode bypassPermissions \
  "Run init-go-project skill non-interactively:
   project_name=widget-svc
   module=github.com/robjsliwa/widget-svc
   database=postgres
   include_cli=true
   cli_name=widgetctl
   auth_enabled=true
   description='Service for managing widgets across tenants.'
   non_interactive=true"
```

`bypassPermissions` auto-approves both file writes and bash commands.
The skill needs both: it runs `git init`, `go mod init`, `go mod tidy`,
`go build`, `go test`, and `swag init`, none of which `acceptEdits`
would approve automatically.

See `references/headless-invocation.md` for the full Backstage scaffolder
template.

## Post-scaffold setup

```bash
cp .env.example .env
# Edit .env — set AUTH_JWKS_URL, AUTH_ISSUER, AUTH_AUDIENCE for prod
# (or AUTH_ENABLED=false to skip auth wiring during early development)

make compose-up      # if database != none
make migrate-up      # if SQL DB
make install-hooks   # enable pre-commit
make run

open http://localhost:8080/docs/   # Swagger UI
```

For the CLI binary (if you scaffolded with `include_cli=true`):

```bash
make build-cli       # builds bin/{cli_name}
./bin/{cli_name} version
```

The CLI is intentionally NOT built into the production Docker image.
See `references/binary-separation.md` for why.

## Updating the skill

Edit files in:

- `assets/*.tmpl` — to change generated config files (Makefile, CI,
  Dockerfile, etc.)
- `references/*.md` — to change architectural guidance Claude follows
  when generating Go code
- `scripts/*.sh` — to change deterministic file operations
- `SKILL.md` — to change the orchestration flow

Adding a new asset (e.g., `.editorconfig`):

1. Add `assets/editorconfig.tmpl`
2. Add a line to `scripts/install-static.sh`
3. Add the file path to `scripts/verify.sh`

That's it. The skill picks up the new asset on the next invocation.

## Uninstalling

```bash
rm -rf ~/.claude/skills/init-go-project
```
