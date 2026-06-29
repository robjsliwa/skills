# Headless Invocation Reference

The skill is designed to run both interactively (in a Claude Code
session) and non-interactively (CI, Backstage scaffolder, scripts).

## Headless mode requirements

Non-interactive invocation requires:

1. **All required parameters** in the invocation message
2. **`non_interactive=true`** to skip the confirmation step
3. **`--permission-mode bypassPermissions`** to auto-approve both file
   writes AND bash commands. The skill runs `git init`, `go mod init`,
   `go build`, `swag init`, etc., all of which are bash invocations.
   `acceptEdits` only covers file edits; `bypassPermissions` covers both.
4. Optionally **`--allowed-tools`** to restrict which tools Claude has

> **Warning:** `bypassPermissions` removes Claude Code's safety prompts
> for tool execution. Use it only when invoking trusted skills in
> trusted environments. The `init-go-project` skill is one such case
> (you wrote it, you trust it). Don't use this mode by default for
> arbitrary AI tasks.

## Command-line invocation

```bash
claude -p \
  --permission-mode bypassPermissions \
  "Run the init-go-project skill non-interactively with these parameters:
   project_name=widget-service
   module=github.com/robjsliwa/widget-service
   database=postgres
   include_cli=true
   cli_name=widgetctl
   auth_enabled=true
   description='Service for managing widgets across tenants.'
   non_interactive=true"
```

For longer descriptions, use a description file:

```bash
claude -p \
  --permission-mode bypassPermissions \
  "Run init-go-project: project_name=widget-service
   module=github.com/robjsliwa/widget-service
   database=postgres
   include_cli=true
   cli_name=widgetctl
   auth_enabled=true
   description_file=./PROJECT_DESCRIPTION.md
   non_interactive=true"
```

## Backstage scaffolder action

### Template (`template.yaml`):

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: go-service
  title: Go REST Service
  description: Production-ready Go service with hexagonal architecture
spec:
  parameters:
    - title: Service identity
      properties:
        project_name:
          type: string
          title: Project name (server binary name)
          pattern: '^[a-z][a-z0-9-]*$'
        module:
          type: string
          title: Go module path
        owner:
          type: string
          title: GitHub org or user
          default: robjsliwa
    - title: Architecture
      properties:
        database:
          type: string
          title: Database
          enum: [none, postgres, mysql, sqlite, mongodb]
          default: postgres
        include_cli:
          type: boolean
          title: Include CLI binary (operator tool — separate binary)
          default: false
        cli_name:
          type: string
          title: CLI binary name
          description: 'Required when include_cli=true. E.g. "fakctl" for project "faktotum".'
          pattern: '^[a-z][a-z0-9-]*$'
        auth_enabled:
          type: boolean
          title: Enable JWT auth middleware
          default: true
        description:
          type: string
          title: One-paragraph description
          ui:widget: textarea
  steps:
    - id: scaffold
      name: Scaffold via init-go-project
      action: run:command
      input:
        command: claude
        args:
          - "-p"
          - "--permission-mode"
          - "bypassPermissions"
          - |
            Run init-go-project skill non-interactively:
            project_name=${{ parameters.project_name }}
            module=${{ parameters.module }}
            database=${{ parameters.database }}
            include_cli=${{ parameters.include_cli }}
            cli_name=${{ parameters.cli_name }}
            auth_enabled=${{ parameters.auth_enabled }}
            description='${{ parameters.description }}'
            non_interactive=true
    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        repoUrl: github.com?owner=${{ parameters.owner }}&repo=${{ parameters.project_name }}
        defaultBranch: main
```

## Required environment for the runner

The Backstage runner (or CI environment) executing `claude` needs:

- `claude` CLI installed
- `ANTHROPIC_API_KEY` set (or other configured auth)
- `go` 1.22+ on PATH
- `git` on PATH
- Permission to write to the scaffolding target directory

## Output format for machine consumption

```bash
claude -p --output-format json --permission-mode bypassPermissions "..."
```

## Failure modes

The skill aborts (non-zero exit through Claude's error) if:

- Required parameters missing in non_interactive mode
- `go` version < 1.22
- Target directory contains existing source files (bootstrap.sh refuses)
- `verify.sh` finds missing files (lists them and exits 1)
- `go build ./...` fails after scaffolding
- `go test ./...` fails after scaffolding

In Backstage, failures bubble up through the action and the template
run fails. Always check Backstage logs for the actual stdout from the
skill — verify.sh output is particularly informative.

## Local testing of headless mode

```bash
mkdir -p /tmp/scaffold-test && cd /tmp/scaffold-test

claude -p --permission-mode bypassPermissions \
  "Run init-go-project non-interactively:
   project_name=test-svc
   module=github.com/robjsliwa/test-svc
   database=postgres
   include_cli=true
   cli_name=tsvcctl
   auth_enabled=true
   description='Test scaffold for headless mode validation.'
   non_interactive=true"

# Verify
ls -la                           # Should see Makefile, .github, deploy/, etc.
ls .github/workflows/            # ci.yml should exist
ls deploy/                       # Both Dockerfile and Dockerfile.cli
ls cmd/                          # server/ and tsvcctl/
go build ./...                   # Should compile
go test ./...                    # Should pass
make swagger                     # Should generate spec
```

## Post-scaffold setup

After Backstage publishes the repo, the new repo's owner runs:

```bash
git clone <repo-url> && cd <repo-name>
cp .env.example .env
# Edit .env — set AUTH_JWKS_URL, AUTH_ISSUER, AUTH_AUDIENCE
make compose-up         # if database != none
make migrate-up         # if SQL database
make install-hooks      # enable pre-commit
make run
open http://localhost:8080/docs/
```
