# CI/CD Reference

Defines the GitHub Actions workflow and the native git pre-commit hook
shipped with the scaffold.

## GitHub Actions

The workflow file lives at `.github/workflows/ci.yml` (template at
`assets/github-workflow-ci.yml.tmpl`). Jobs:

| Job | Triggers | Purpose |
|-----|----------|---------|
| `lint` | push, PR | golangci-lint |
| `test` | push, PR | unit tests with race detector |
| `swagger-check` | push, PR | regenerate spec, fail on diff |
| `test-integration` | push to main, manual | testcontainer-backed integration tests |
| `build` | push, PR | `go build ./...` |
| `docker-build` | push to main | `docker build` (no push by default) |

Notes on the design:

- **No registry push** by default. Pushing to ghcr.io or another registry
  requires per-project credentials and is outside scaffold scope. The
  workflow includes a commented stub showing where to add it.
- **Integration tests run on main and on demand** to avoid burning Docker
  resources on every PR.
- **`actions/cache`** keeps the Go build and module cache warm.
- **`actions/setup-go@v5`** with `cache: true` handles the `~/go/pkg/mod`
  cache automatically.
- **golangci-lint** uses `golangci/golangci-lint-action@v6` for caching.

## Pre-commit hook

Native git hook installed via `git config core.hooksPath .githooks`.
The hook script lives at `.githooks/pre-commit` (template at
`assets/pre-commit-hook.sh.tmpl`).

Stages:

1. List staged Go files (`git diff --cached --name-only`)
2. Skip if no Go files
3. `gofmt -l` on staged files (fails if any need formatting)
4. `go vet ./...`
5. `go test -short -count=1 ./...` (unit tests only, no integration)
6. `golangci-lint run --new-from-rev=HEAD~1` if installed (incremental)
7. Print success or fail with clear remediation

## Why native hooks instead of pre-commit.com?

Trade-offs:

| | Native (`.githooks/`) | pre-commit.com framework |
|---|---|---|
| Setup | `git config core.hooksPath` | `pip install pre-commit && pre-commit install` |
| Deps | None — bash only | Python + the framework |
| Configuration | Edit shell script | `.pre-commit-config.yaml` |
| Cross-language hooks | Manual | Built-in plugin ecosystem |
| Per-project versioning | None | Hooks pinned by SHA |

For a single-language Go project starter, native hooks are simpler and
zero-deps. If you later need multi-repo standardization or Python/JS
hooks too, switch to pre-commit.com — the migration is mechanical
(translate the shell script into `.pre-commit-config.yaml` entries
or call the script from a `local` hook).

## Installation

After scaffolding, the user runs:

```bash
make install-hooks
```

Which executes:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
echo "Pre-commit hook installed."
```

The `git_init` step in the scaffold workflow runs this automatically.

## Bypassing the hook

Per-commit override: `git commit --no-verify`. Use sparingly — the hook
catches mistakes that CI would otherwise catch a minute later.

## Hook updates and team adoption

The hook script is committed to the repo. When the team pulls a new
version with hook changes, contributors need to re-run `make install-hooks`
only if they didn't have it set already. The `git config` is per-clone,
not per-commit, so it persists.

For mandatory enforcement across a team without relying on contributors
running `make install-hooks`, add a server-side check (GitHub branch
protection requiring CI to pass). Server-side enforcement is more
reliable than client-side hooks.
