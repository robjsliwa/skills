# Production Readiness Checklist

> **NOTE:** Examples below use `widgets` as a placeholder resource name.
> The actual scaffolded code uses the domain entity derived from the
> project description.

The features below are scaffolded by `init-go-project`. This document is
the source of truth for what "production-ready" means in the generated
service.

## HTTP Server

- Timeouts on `*http.Server`:
  - `ReadHeaderTimeout: 5 * time.Second`
  - `ReadTimeout: 10 * time.Second`
  - `WriteTimeout: 30 * time.Second`
  - `IdleTimeout: 120 * time.Second`
- Graceful shutdown via `signal.NotifyContext(SIGINT, SIGTERM)` and
  `srv.Shutdown(ctx)` with configurable drain timeout (default 30s)
- Server runs in goroutine; main goroutine waits on signal context

## Middleware Chain

Applied in this order (outermost first):

1. **Recoverer** — recovers panics, logs stack with trace, returns 500
2. **RequestID** — assigns `X-Request-Id` if absent; injects into context
3. **Tracer** — `otelhttp.NewHandler` for span creation
4. **Logger** — slog access log with method, path, status, duration,
   request_id, trace_id, span_id
5. **CORS** — configurable allowed origins via `CORS_ORIGINS` env
6. **Auth** (per-route) — JWT validation via `internal/auth.RequireAuth`,
   applied selectively to protected route groups in `routes.go`

## Authentication

Full JWT validation middleware in `internal/auth/`:

- HS256 (development), RS256 / ES256 (production with JWKS)
- JWKS fetching with caching and automatic key rotation via `keyfunc/v3`
- Issuer (`iss`) and Audience (`aud`) validation
- Expiry (`exp`) and Not-Before (`nbf`) validation with configurable clock skew
- Scope-based authorization via `RequireScope("widgets:write")`
- Claims extraction via `auth.ClaimsFromContext(ctx)`
- Skip-list for unauthenticated paths (`/healthz`, `/readyz`, `/docs/*`)
- Hard disable via `AUTH_ENABLED=false`
- `WWW-Authenticate` header on 401 responses per RFC 6750

See `references/auth-middleware.md`.

## Request Validation

Field-level validation via `go-playground/validator/v10`:

- Request DTOs in `internal/adapters/http/dto.go` carry `validate:` tags
- Single shared `validator.Validate` instance (cached reflection)
- `decodeAndValidate(r, &dst)` helper handles JSON decoding +
  validation + body-size limit in one call
- Validation errors mapped to HTTP 400 with field-level error details
  (`ErrorResponse{Fields: [...]}`)
- `DisallowUnknownFields()` rejects unexpected JSON keys
- Body size capped via `http.MaxBytesReader` (default 1MB, configurable)
- 413 response if body exceeds limit

See `references/validation.md`.

## API Documentation

Code-first OpenAPI via `swaggo/swag`:

- Spec generated from comments on handlers and DTOs
- Generated artifacts in `docs/`: `docs.go`, `swagger.json`, `swagger.yaml`
- Spec committed to repo (changes appear in PR review)
- CI validates spec is up-to-date by running `swag init` and failing
  on diff
- Swagger UI served at `/docs/` via `swaggo/http-swagger/v2`
  (self-contained, no CDN)
- Bearer auth security scheme declared at the spec level

See `references/openapi-annotations.md`.

## Health Checks

- `GET /healthz` — Liveness; always returns 200 if process is up
- `GET /readyz` — Readiness; pings the store with a 1s timeout;
  returns 503 if store unreachable
- Both endpoints skip auth middleware

## Observability

### Logging (slog)

- JSON handler in production, text in development (env-controlled)
- Trace and span IDs auto-injected via custom handler wrapper
- Log levels via `LOG_LEVEL` (debug/info/warn/error)

### Tracing (OpenTelemetry)

- OTLP gRPC exporter; endpoint via `OTEL_EXPORTER_OTLP_ENDPOINT`
- Resource attributes: `service.name`, `service.version`, `deployment.environment`
- `OTEL_TRACES_EXPORTER=none` disables for local dev

### Metrics (OpenTelemetry)

- OTLP gRPC; standard HTTP metrics via `otelhttp` instrumentation
- Custom metrics ready via `otel.Meter("service-name")`

### Logs (OpenTelemetry)

- slog records bridged to OTel log pipeline
- Same OTLP endpoint

## Configuration

- All config via env vars; `.env` loaded if present (stdlib only)
- `Config.Validate()` called at startup; service refuses to start on
  invalid config (e.g., `AUTH_ENABLED=true` but missing `AUTH_JWKS_URL`)
- Sensitive values never logged
- `--version` flag prints build info from `-ldflags`

## Build Info

```go
var (
    Version   = "dev"
    Commit    = "unknown"
    BuildTime = "unknown"
)
```

Injected at build time via Makefile `LDFLAGS`.

## CI/CD

- **GitHub Actions** workflow at `.github/workflows/ci.yml`:
  lint, test (race), swagger drift check, integration (on main), build,
  docker-build (no push)
- **Pre-commit hook** at `.githooks/pre-commit` (native git hook,
  zero deps): gofmt, go vet, fast tests, incremental golangci-lint
- `make install-hooks` configures `core.hooksPath`
- See `references/ci-cd.md`

## Database (when chosen)

- Connection pool sized via env (`DB_MAX_OPEN_CONNS`, `DB_MAX_IDLE_CONNS`)
- `db.PingContext(ctx)` at startup with timeout; service refuses to
  start if DB unreachable
- Connection close in shutdown sequence
- All queries take `context.Context` first
- Migrations run separately via `make migrate-up` (never auto-run)
- For PostgreSQL: `pgx/v5` via `database/sql` interface

## Security baseline

- TLS termination at proxy/ingress (configurable to enable TLS via
  `TLS_CERT` / `TLS_KEY`)
- DB credentials only from env; never in code
- Request size limits via `http.MaxBytesReader` (1MB default)
- Auth middleware in production mode validates against external IdP via
  JWKS — no local secret needed
- `WWW-Authenticate` headers on 401
- Unknown JSON fields rejected by default (defense against parameter
  injection)
- CORS configurable per origin (no `*` default)

## Container

- Multi-stage Dockerfile: `golang:1.23-alpine` builder → `gcr.io/distroless/static-debian12:nonroot` runtime
- Runs as non-root user
- Single binary, no shell, minimal attack surface
- Healthcheck handled by Kubernetes probes (distroless has no curl)

## Local Development

- `docker-compose.yml` brings up the chosen DB
- `make run` runs the service against the compose stack
- `make test` runs unit tests
- `make test-integration` runs testcontainer-based integration tests
  (SQL DBs only)
- `make lint` runs golangci-lint
- `make swagger` regenerates the OpenAPI spec
- `make codemap` regenerates `docs/MODULE_MAP.md`
- `make install-hooks` enables the pre-commit hook
