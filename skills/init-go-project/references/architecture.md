# Architecture Reference

Hexagonal layout used by `init-go-project`. The generated
`docs/ARCHITECTURE.md` is derived from this reference, customized with
the project's name, database choice, and auth setup.

## Layers

### Domain Ports (`pkg/domain/`)

The SDK boundary. External consumers depend only on this package.

- Domain types (entities, value objects)
- Port interfaces — contracts adapters implement
- Domain sentinel errors (`ErrNotFound`, `ErrAlreadyExists`)

**Rules:**
- No imports from `internal/`
- No imports from `cmd/`
- No HTTP, DB, validator, or telemetry imports
- Pure types and interfaces — no business logic

### Application Core (`internal/core/`)

Business logic. Pure functions of domain types and ports.

**Rules:**
- Imports `pkg/domain` only (plus stdlib and `slog`)
- No HTTP, no SQL, no driver-specific imports
- Returns domain errors; never HTTP status codes or DB errors

### Authentication (`internal/auth/`)

JWT/OAuth token validation. Separate package to keep the HTTP adapter
focused on HTTP concerns and to allow auth reuse from the CLI binary
or background jobs.

- `Authenticator` struct and constructor
- `RequireAuth` and `RequireScope` middleware
- `Claims` type and `ClaimsFromContext` helper
- JWKS support via `keyfunc/v3`

**Rules:**
- Imports `golang-jwt/jwt/v5` and `MicahParks/keyfunc/v3`
- Does NOT import `internal/adapters/http` (would be a cycle)
- Writes its own auth-error responses to keep dependency direction clean

### Adapters (`internal/adapters/`)

Implementations of domain ports for specific infrastructure.

- `adapters/http/` — REST handlers; HTTP ↔ domain translation
  - `dto.go` — request/response DTOs with `validate:` tags
  - `decode.go` — `decodeAndValidate` helper using
    `go-playground/validator`
  - `respond.go` — `respondJSON`, `respondError` (maps domain errors
    and validation errors to status codes)
  - `handlers.go` — handlers WITH `swag` annotations
  - `middleware.go` — RequestID, Logger, Recoverer, CORS
  - `routes.go` — route registration; wires `internal/auth` middleware
  - `swagger.go` — `httpSwagger.Handler` mount
  - `health.go` — `/healthz`, `/readyz`
  - `server.go` — `*http.Server` setup
- `adapters/store/` — DB implementation of repository ports
- `adapters/telemetry/` — OTel + slog setup

**Rules:**
- Each adapter directory imports `pkg/domain` and `internal/core`
- HTTP adapter additionally imports `internal/auth`
- Adapters do NOT import each other (e.g., `http` never imports `store`)
- Service injection happens at `cmd/server/main.go`

### Application Entry (`cmd/`)

The composition root. Server and CLI are **separate binaries** in the
same repo, each with its own `main.go`. They share `pkg/` and `internal/`
packages but compile independently.

- `cmd/server/` — HTTP service binary (always present)
- `cmd/{cli_name}/` — Optional operator CLI binary (only when
  `include_cli=true`)

**Rules:**
- The ONLY place where adapters and core are wired
- Imports everything; nothing imports `cmd/`
- The server's `main.go` holds the package-level swag metadata
- The CLI binary is built and deployed separately from the server.
  See `binary-separation.md` for the security rationale.

### Configuration (`internal/config/`)

Env loading and validation.

**Rules:**
- Imported by `cmd/` only
- Returns a single `Config` struct with `HTTP`, `Logging`, `OTel`, `DB`,
  and `Auth` sub-structs

## Sample Domain Pattern

> **NOTE:** The examples below use `Widget` as a placeholder entity name.
> When generating code, replace `Widget` with the actual domain entity
> derived from the project description (e.g., `Task`, `Certificate`,
> `Order`). Adapt struct fields to match the real entity's attributes.

The scaffold ships with one domain entity end-to-end:

```
HTTP request → middleware chain → handler → service → port → store → DB
                       ↓               ↓
                  internal/auth   pkg/domain (types, port)
                  decodeAndValidate
                  respond
```

- `pkg/domain/types.go` — `Widget` struct (no validation tags)
- `pkg/domain/ports.go` — `WidgetRepository` interface
- `internal/core/service.go` — `WidgetService`
- `internal/adapters/store/{db}.go` — implements `WidgetRepository`
- `internal/adapters/http/dto.go` — `CreateWidgetRequest` (with
  `validate:` tags), `WidgetResponse`
- `internal/adapters/http/handlers.go` — handler functions (with swag
  annotations)

## Why this shape

- **Testability** — Core has no infra; tests use the in-memory adapter
- **Swappability** — Change DB by swapping the store adapter; core unchanged
- **SDK boundary** — `pkg/domain` is publishable as a client SDK
- **Validation isolation** — `validate:` tags on DTOs only, not domain types
- **Auth isolation** — `internal/auth` is independent of HTTP adapter
- **Clear blast radius** — Adapter changes never break domain tests

## What does NOT belong where

| Mistake | Why wrong | Where it should go |
|---------|-----------|-------------------|
| SQL strings in `internal/core/` | Core must be infra-free | `internal/adapters/store/` |
| HTTP status codes in `pkg/domain/` | Domain errors are framework-agnostic | Returned from core; HTTP adapter maps to status |
| `validate:` tags on `pkg/domain/` types | Domain stays free of validation library | DTO types in `internal/adapters/http/dto.go` |
| Swag annotations on domain types | Spec is HTTP-layer concern | Handler functions in `internal/adapters/http/` |
| JWT parsing in handler functions | Auth concerns belong in middleware | `internal/auth/` middleware |
| `database/sql` imports in `internal/core/` | Core is port-only | Adapter implements port |
| OTel imports in `internal/core/` | Core is telemetry-free | Context propagation only; spans created in adapters |
