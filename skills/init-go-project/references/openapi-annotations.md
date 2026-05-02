# OpenAPI Annotations Reference (swaggo/swag)

> **NOTE:** Code examples below use `Widget`/`CreateWidgetRequest`/`WidgetResponse`
> as placeholders. Replace with the actual domain entity from the project
> description (e.g., `Task`/`CreateTaskRequest`/`TaskResponse`). Adapt
> route paths, tags, and descriptions accordingly.

The OpenAPI spec is generated from comment annotations on Go declarations
via `swaggo/swag`. The generated artifacts live under `docs/`:

- `docs/docs.go` — Go source registering the spec at runtime
- `docs/swagger.json` — JSON spec
- `docs/swagger.yaml` — YAML spec

Regenerate via `make swagger` after editing handlers.

## Top-level metadata (in `cmd/server/main.go`)

Place above `package main`:

```go
// Package main provides the {{Project}} HTTP service.
//
// @title           {{Project}} API
// @version         1.0
// @description     {{description first line}}
// @termsOfService  http://swagger.io/terms/
//
// @contact.name   {{ContactName or "API Support"}}
// @contact.email  {{ContactEmail or "support@example.com"}}
//
// @license.name  Apache 2.0
// @license.url   http://www.apache.org/licenses/LICENSE-2.0.html
//
// @host          localhost:8080
// @BasePath      /api/v1
// @schemes       http https
//
// @securityDefinitions.apikey  BearerAuth
// @in                          header
// @name                        Authorization
// @description                 Bearer JWT token from the configured IdP.
package main

import (
    // Required for swag to find the docs package
    _ "{{module}}/docs"
)
```

The first line under `@description` should reflect the project description
gathered at scaffold time.

## Handler annotations

Each handler function gets a comment block ABOVE the function. The format
is rigid — `swag` parses these by structure.

```go
// CreateWidget creates a new widget.
//
// @Summary      Create a widget
// @Description  Creates a new widget owned by the authenticated user.
// @Tags         widgets
// @Accept       json
// @Produce      json
// @Param        widget  body      CreateWidgetRequest  true  "Widget payload"
// @Success      201     {object}  WidgetResponse
// @Failure      400     {object}  ErrorResponse  "validation failed or malformed body"
// @Failure      401     {object}  ErrorResponse  "missing or invalid token"
// @Failure      403     {object}  ErrorResponse  "insufficient scope"
// @Failure      500     {object}  ErrorResponse  "internal error"
// @Security     BearerAuth
// @Router       /widgets [post]
func (h *Handlers) CreateWidget(w http.ResponseWriter, r *http.Request) { ... }
```

### Required annotations on every handler

| Annotation | Purpose |
|------------|---------|
| `@Summary` | One-line summary (shown in UI list) |
| `@Description` | Longer description (shown in expanded view) |
| `@Tags` | Group in UI; use one tag per resource (`widgets`, `health`) |
| `@Accept` | `json` for request body endpoints; omit for GET/DELETE |
| `@Produce` | Always `json` for this scaffold |
| `@Success` | Primary success response with code, type, optional description |
| `@Failure` | One per error code returned (400, 401, 403, 404, 409, 500) |
| `@Router` | Path AND method, e.g., `/widgets/{id} [get]` |
| `@Security` | `BearerAuth` for protected endpoints; omit for public |

### Path and query parameters

```go
// @Param   id      path    string  true   "Widget ID"  Format(uuid)
// @Param   limit   query   int     false  "Max results"  default(50) minimum(1) maximum(500)
// @Param   cursor  query   string  false  "Pagination cursor"
```

### Body parameter

```go
// @Param   widget  body  CreateWidgetRequest  true  "Widget payload"
```

The type referenced (`CreateWidgetRequest`) must be a Go struct in a
package `swag` can find. Run `swag init` with `--parseInternal` so it
walks `internal/`. Struct fields use standard `json:` tags for field
names and an `example:` tag for swagger examples:

```go
type CreateWidgetRequest struct {
    Name        string `json:"name"        example:"My Widget"  validate:"required,min=1,max=200"`
    Description string `json:"description" example:"Optional description"  validate:"max=2000"`
}
```

### Header parameter

```go
// @Param   X-Tenant-ID  header  string  true  "Tenant identifier"
```

### Multiple success codes

If an endpoint can return multiple success codes, declare each:

```go
// @Success  200  {object}  WidgetResponse  "widget found"
// @Success  304  "not modified"
```

## Health endpoints

```go
// Healthz reports liveness.
//
// @Summary  Liveness probe
// @Tags     health
// @Produce  plain
// @Success  200  {string}  string  "ok"
// @Router   /healthz [get]
func (h *Handlers) Healthz(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(200)
    _, _ = w.Write([]byte("ok"))
}
```

Note: health endpoints typically live OUTSIDE `/api/v1` so their `@Router`
path is the full path. To handle this, omit `@BasePath` impact by using
the full path with a leading `/` — `swag` respects either form, but for
endpoints that should appear at root rather than under `/api/v1`, register
them on a separate spec section. Simplest: keep health endpoints in the
same spec but use `@Router /healthz [get]` and accept that the UI shows
them under the configured BasePath. For separating, see `swag` multi-API
docs.

## DTO documentation

Document DTO fields with `swag`-aware tags. Combine `validate`, `json`,
and `example`:

```go
// CreateWidgetRequest is the JSON body for POST /api/v1/widgets.
type CreateWidgetRequest struct {
    // Name is the human-readable widget name.
    Name string `json:"name" validate:"required,min=1,max=200" example:"Sample Widget"`

    // Description is an optional free-form description.
    Description string `json:"description" validate:"max=2000" example:"Used in tests"`
}
```

Field-level Go doc comments (`// Name is the...`) become field
descriptions in the generated spec.

## Common annotations cheat sheet

| Annotation | Where | Example |
|-----------|-------|---------|
| `@Summary` | Handler | `@Summary  Get widget` |
| `@Description` | Handler | `@Description  Returns the widget if it exists.` |
| `@Tags` | Handler | `@Tags  widgets` |
| `@Accept` | Handler | `@Accept  json` |
| `@Produce` | Handler | `@Produce  json` |
| `@Param` | Handler | See above |
| `@Success` | Handler | `@Success  200  {object}  WidgetResponse` |
| `@Failure` | Handler | `@Failure  404  {object}  ErrorResponse` |
| `@Router` | Handler | `@Router  /widgets/{id} [get]` |
| `@Security` | Handler | `@Security  BearerAuth` |
| `@Deprecated` | Handler | `@Deprecated  true` |
| `example:"..."` | DTO field | `example:"foo"` |
| `format:"..."` | Path/query param | `Format(uuid)` |

## CLAUDE.md note for contributors

Add this to the generated CLAUDE.md so future Claude Code sessions know
the convention:

> **OpenAPI is code-first.** Every new HTTP handler MUST have swag
> annotations above it (see existing handlers for examples). Run
> `make swagger` to regenerate `docs/swagger.json`, `docs/swagger.yaml`,
> and `docs/docs.go` before committing. The CI pipeline runs
> `swag init` and fails if the committed spec is stale.

## Stale spec detection in CI

The CI workflow runs:

```bash
swag init -g cmd/server/main.go -o docs --parseInternal --parseDependency
git diff --exit-code -- docs/
```

If a developer modified handler annotations without regenerating, the
diff is non-empty and CI fails. This forces the spec to stay in sync
with the code.
