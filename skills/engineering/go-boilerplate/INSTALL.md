# go-boilerplate

Scaffold a new Go REST API service from a production-ready boilerplate: Chi router, OpenTelemetry tracing/metrics, Swagger/OpenAPI docs, in-memory CRUD store.

## Install

```bash
cp -r /path/to/go-boilerplate ~/.claude/skills/go-boilerplate
chmod +x ~/.claude/skills/go-boilerplate/scripts/apply.sh
```

Requires: Go toolchain (`go mod tidy`), perl (ships with macOS and Linux).

## Usage in Claude Code

```
/go-boilerplate
```

Claude will ask for project name, GitHub user, and description, then scaffold the project.

## Direct script usage

```bash
bash ~/.claude/skills/go-boilerplate/scripts/apply.sh \
  --project-name  my-service \
  --github-user   acme \
  --description   "Order management API for the warehouse team" \
  --dest          ~/projects/my-service \
  --module        github.com/acme/my-service
```

`--dest` and `--module` are optional. `--dest` defaults to `./{project_name}`. `--module` defaults to `github.com/{github_user}/{project_name}`.

## What it does

1. Extracts the frozen boilerplate snapshot into the destination directory
2. Replaces the module path in `go.mod` and all `.go` imports
3. Replaces service name string literals (OTel tracer/meter names, config default)
4. Updates Swagger `@title` / `@description` annotations and generated docs
5. Updates `README.md` title and description
6. Runs `go mod tidy`

## After scaffolding

```bash
cd <dest_dir>
make run        # start the server (default port 8080)
make swagger    # regenerate docs after editing handler annotations
make build      # compile to bin/server
```
