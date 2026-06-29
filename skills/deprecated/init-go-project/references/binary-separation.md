# Binary Separation: Server vs CLI

When `include_cli=true`, the scaffold generates two independent binaries
in the same repository:

- `cmd/server/main.go` → builds to `bin/{project_name}` — the HTTP service
- `cmd/{cli_name}/main.go` → builds to `bin/{cli_name}` — the operator CLI

Both share the same `pkg/` and `internal/` packages, but they are compiled
into separate binaries with separate entry points.

## Why separate binaries instead of subcommands

A common (and tempting) pattern is to ship one binary with subcommands:

```bash
faktotum server     # starts the HTTP service
faktotum cli ...    # operator commands
```

This is convenient locally. It is also a security problem in production.

Operator CLIs typically expose capabilities the HTTP layer does not:
direct database surgery, secret rotation, user provisioning, debugging
dumps, raw cache flushes. These operations are not in the HTTP API
*because they're dangerous* — there's no authorization model around
them, no audit trail, no rate limiting. They exist for human operators
running locally with privileged credentials.

If you ship those capabilities inside the same binary you deploy to
production, then anyone who gains shell access to the running container
(through a remote code execution bug, a misconfigured sidecar, a
compromised CI runner) immediately gets a turnkey administration tool.
The "principle of least privilege" gets violated by convenience.

The fix is structural: the production runtime image contains only the
server binary. The CLI binary lives elsewhere — distributed to operators
via Homebrew, an internal artifact server, a separate Docker image used
only for ops jumpboxes, or simply built locally from source. It is not
in the production container, full stop.

## Repository layout

Same repo, separate `cmd/` subdirectories:

```
cmd/
├── server/
│   └── main.go        # HTTP service entry point
└── {cli_name}/
    └── main.go        # cobra-based CLI entry point
```

Both `main.go` files are independent `package main`. They import shared
code from `pkg/` and `internal/`, but they don't import each other.

## Build separation in the Makefile

```makefile
.PHONY: build
build: swagger
	@mkdir -p bin
	go build -ldflags "$(LDFLAGS)" -o bin/$(PROJECT_NAME) ./cmd/server

.PHONY: build-cli
build-cli:
	@mkdir -p bin
	go build -ldflags "$(LDFLAGS)" -o bin/$(CLI_NAME) ./cmd/$(CLI_NAME)

.PHONY: build-all
build-all: build build-cli
```

Note that `make build` (the default) only builds the server. `make build-cli`
is opt-in. CI runs both to catch breakage in either, but the production
Docker image only contains the server output.

## Dockerfile separation

`deploy/Dockerfile` (the default, used for cloud deployment):

```dockerfile
FROM golang:1.23-alpine AS builder
# ... copy source, run `go build ./cmd/server`, output single binary

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /out/{{PROJECT_NAME}} /app/{{PROJECT_NAME}}
ENTRYPOINT ["/app/{{PROJECT_NAME}}"]
```

The CLI binary is never copied into this image. Even if an attacker
gets shell access (which they can't easily on distroless, but assume
they do), there is no `{cli_name}` binary to invoke.

`deploy/Dockerfile.cli` (only generated when `include_cli=true`, intended
for ops use only):

```dockerfile
FROM golang:1.23-alpine AS builder
# ... copy source, run `go build ./cmd/{{CLI_NAME}}`, output single binary

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /out/{{CLI_NAME}} /app/{{CLI_NAME}}
ENTRYPOINT ["/app/{{CLI_NAME}}"]
```

Tag this image differently in your registry (e.g.,
`registry.example.com/faktotum-ops:v1.0.0` vs
`registry.example.com/faktotum:v1.0.0`) so it's obvious which is which.
Run the ops image only on operator workstations or jumpbox containers
that have appropriate IAM credentials. Do NOT deploy it to your
production cluster.

## CLI structure

`cmd/{cli_name}/main.go` is a cobra root with subcommands. It does NOT
share code with the server entry point — it's a separate binary that
loads its own config and connects to its own resources.

Conventions:

- Subcommands: `version`, plus whatever ops actions the project needs
  (e.g., `migrate`, `seed`, `tenant create`, `dump-config`).
- Do NOT include a `serve` subcommand. The server is its own binary
  invoked directly. Adding `cli serve` re-introduces the convenience
  that this whole pattern exists to avoid.
- Use the same `internal/config` package for config loading, but expose
  flags for overriding individual fields when convenient for ops use
  (e.g., `--db-host` to point at a different database).
- The CLI may use credentials with broader privileges than the server.
  Make sure the CLI binary's distribution channel is appropriately
  restricted (private artifact registry, internal only, etc.).

## Initial CLI scaffold

```go
// cmd/{cli_name}/main.go
package main

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
)

var (
    Version   = "dev"
    Commit    = "unknown"
    BuildTime = "unknown"
)

func main() {
    root := &cobra.Command{
        Use:   "{cli_name}",
        Short: "{project_name} operator CLI",
        Long: `Operator CLI for {project_name}.

This tool is intended for operators with privileged credentials.
Do NOT deploy this binary to production runtime environments;
deploy cmd/server only.`,
    }

    root.AddCommand(&cobra.Command{
        Use:   "version",
        Short: "Print build info",
        Run: func(cmd *cobra.Command, args []string) {
            fmt.Printf("{cli_name} %s (%s, built %s)\n", Version, Commit, BuildTime)
        },
    })

    // Add ops subcommands here as you build them.
    // Examples for a typical service:
    //   migrate      — run/rollback DB migrations
    //   tenant       — create/delete/list tenants
    //   keys         — rotate signing keys
    //   dump-config  — print effective config (with secrets redacted)

    if err := root.Execute(); err != nil {
        os.Exit(1)
    }
}
```

## CI considerations

The GitHub Actions workflow builds BOTH binaries (so breakage is caught),
but only the server image is built and pushed to the registry by
default. To also publish the CLI image:

```yaml
- name: Build CLI image
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  uses: docker/build-push-action@v6
  with:
    context: .
    file: deploy/Dockerfile.cli
    push: false   # or true with separate registry credentials
    tags: |
      {{PROJECT_NAME}}-ops:${{ github.sha }}
      {{PROJECT_NAME}}-ops:latest
```

Note the `-ops` suffix in the tag, which makes the distinction obvious
in your registry browser.

## Summary

| Concern | Implementation |
|---------|---------------|
| Server entry | `cmd/server/main.go` |
| CLI entry | `cmd/{cli_name}/main.go` |
| Server binary | `bin/{project_name}` |
| CLI binary | `bin/{cli_name}` |
| Server image | `deploy/Dockerfile` (always generated) |
| CLI image | `deploy/Dockerfile.cli` (only if `include_cli=true`) |
| Production deployment | Server binary only |
| CLI distribution | Separate channel (registry, Homebrew, internal artifact) |

When in doubt: if a capability would be dangerous in the hands of an
attacker who got shell on a production pod, it belongs in the CLI
binary, not the server.
