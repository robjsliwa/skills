# Auth Middleware Reference

> **NOTE:** Route and scope examples below use `widgets` as a placeholder
> resource name. Replace with the actual domain entity's plural form
> (e.g., `tasks`, `certificates`, `orders`) and adapt scope names
> accordingly (e.g., `tasks:read`, `tasks:write`).

Defines the JWT/OAuth validation middleware shipped in
`internal/auth/`. The middleware validates tokens issued by an external
identity provider (Auth0, Cognito, Keycloak, custom IdP) — it is NOT an
OAuth server.

## Capabilities

- HMAC (HS256) — single shared secret, suitable for development
- RSA (RS256) and ECDSA (ES256) — via JWKS URL with automatic key rotation
- Issuer (`iss`) and Audience (`aud`) validation
- Expiry (`exp`) and Not-Before (`nbf`) validation
- Scope-based authorization (claim `scope` or `scp`)
- Claims extraction helper for handlers
- Skip-list for unauthenticated paths (`/healthz`, `/readyz`, `/docs/*`)
- Hard disable via `AUTH_ENABLED=false`

## Dependencies

```go
github.com/golang-jwt/jwt/v5
github.com/MicahParks/keyfunc/v3   // JWKS fetching with cache + rotation
```

## Config (env vars)

```
AUTH_ENABLED=true
AUTH_ALGORITHM=RS256              # RS256 | ES256 | HS256
AUTH_ISSUER=https://my-idp.example.com/
AUTH_AUDIENCE=https://api.{{PROJECT_NAME}}.example.com
AUTH_JWKS_URL=https://my-idp.example.com/.well-known/jwks.json
AUTH_JWKS_REFRESH_INTERVAL=10m
AUTH_HMAC_SECRET=                 # Required ONLY if algorithm=HS256
AUTH_REQUIRED_SCOPES=             # Optional comma-separated default scopes
AUTH_CLOCK_SKEW=30s
AUTH_SKIP_PATHS=/healthz,/readyz,/docs
```

`Config.Validate()` rules:

- `AUTH_ENABLED=false` → no other auth fields required
- `AUTH_ENABLED=true` AND `AUTH_ALGORITHM` in [RS256, ES256] → `AUTH_JWKS_URL` required
- `AUTH_ENABLED=true` AND `AUTH_ALGORITHM=HS256` → `AUTH_HMAC_SECRET` required
- `AUTH_ISSUER` and `AUTH_AUDIENCE` required if `AUTH_ENABLED=true`

## File: `internal/auth/auth.go`

```go
package auth

import (
    "context"
    "errors"
    "fmt"
    "log/slog"
    "net/http"
    "strings"
    "time"

    "github.com/MicahParks/keyfunc/v3"
    "github.com/golang-jwt/jwt/v5"
)

// Config holds auth middleware configuration. Built from env in
// internal/config; the struct lives here to keep the auth package
// self-contained.
type Config struct {
    Enabled              bool
    Algorithm            string
    Issuer               string
    Audience             string
    JWKSURL              string
    JWKSRefreshInterval  time.Duration
    HMACSecret           string
    RequiredScopes       []string
    ClockSkew            time.Duration
    SkipPaths            []string
}

// Claims is what we extract from a validated token and inject into context.
// Extend as your IdP requires.
type Claims struct {
    Subject string   `json:"sub"`
    Issuer  string   `json:"iss"`
    Audience []string `json:"aud"`
    Scopes  []string `json:"-"`        // Parsed from "scope" or "scp" claim
    Email   string   `json:"email,omitempty"`
    Raw     jwt.MapClaims              // Full claims for app-specific access
}

// Authenticator validates tokens.
type Authenticator struct {
    cfg     Config
    keyfunc jwt.Keyfunc
    log     *slog.Logger
}

// New constructs an Authenticator. If cfg.Enabled is false, the returned
// Authenticator is a no-op that always allows requests through.
func New(cfg Config, log *slog.Logger) (*Authenticator, error) {
    a := &Authenticator{cfg: cfg, log: log}
    if !cfg.Enabled {
        return a, nil
    }
    switch cfg.Algorithm {
    case "HS256":
        secret := []byte(cfg.HMACSecret)
        a.keyfunc = func(t *jwt.Token) (any, error) {
            if t.Method.Alg() != "HS256" {
                return nil, fmt.Errorf("unexpected alg %q", t.Method.Alg())
            }
            return secret, nil
        }
    case "RS256", "ES256":
        kf, err := keyfunc.NewDefaultCtx(context.Background(), []string{cfg.JWKSURL})
        if err != nil {
            return nil, fmt.Errorf("auth: jwks init: %w", err)
        }
        a.keyfunc = kf.Keyfunc
    default:
        return nil, fmt.Errorf("auth: unsupported algorithm %q", cfg.Algorithm)
    }
    return a, nil
}

// RequireAuth is the middleware that validates the bearer token and
// injects Claims into the request context.
func (a *Authenticator) RequireAuth(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if !a.cfg.Enabled || a.shouldSkip(r.URL.Path) {
            next.ServeHTTP(w, r)
            return
        }
        token, err := a.extractAndValidate(r)
        if err != nil {
            a.log.WarnContext(r.Context(), "auth failed",
                slog.String("path", r.URL.Path),
                slog.String("error", err.Error()))
            writeAuthError(w, http.StatusUnauthorized, "invalid_token", err.Error())
            return
        }
        claims, err := claimsFromToken(token, a.cfg)
        if err != nil {
            writeAuthError(w, http.StatusUnauthorized, "invalid_token", err.Error())
            return
        }
        if err := a.checkRequiredScopes(claims); err != nil {
            writeAuthError(w, http.StatusForbidden, "insufficient_scope", err.Error())
            return
        }
        ctx := context.WithValue(r.Context(), claimsContextKey{}, claims)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// RequireScope returns middleware that enforces a specific scope on top
// of RequireAuth. Apply this to handlers that need fine-grained checks:
//
//   mux.Handle("DELETE /widgets/{id}",
//       auth.RequireAuth(auth.RequireScope("widgets:write")(handler)))
func (a *Authenticator) RequireScope(scope string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            claims, ok := ClaimsFromContext(r.Context())
            if !ok {
                writeAuthError(w, http.StatusUnauthorized, "missing_claims", "no claims in context")
                return
            }
            if !hasScope(claims.Scopes, scope) {
                writeAuthError(w, http.StatusForbidden, "insufficient_scope",
                    fmt.Sprintf("required scope %q not granted", scope))
                return
            }
            next.ServeHTTP(w, r)
        })
    }
}

// extractAndValidate pulls the bearer token, parses it, and validates
// signature + standard claims.
func (a *Authenticator) extractAndValidate(r *http.Request) (*jwt.Token, error) {
    h := r.Header.Get("Authorization")
    if h == "" {
        return nil, errors.New("missing Authorization header")
    }
    if !strings.HasPrefix(h, "Bearer ") {
        return nil, errors.New("malformed Authorization header")
    }
    raw := strings.TrimPrefix(h, "Bearer ")
    parser := jwt.NewParser(
        jwt.WithIssuer(a.cfg.Issuer),
        jwt.WithAudience(a.cfg.Audience),
        jwt.WithLeeway(a.cfg.ClockSkew),
        jwt.WithValidMethods([]string{a.cfg.Algorithm}),
    )
    token, err := parser.Parse(raw, a.keyfunc)
    if err != nil {
        return nil, fmt.Errorf("token validation: %w", err)
    }
    if !token.Valid {
        return nil, errors.New("token invalid")
    }
    return token, nil
}

func claimsFromToken(t *jwt.Token, cfg Config) (*Claims, error) {
    mc, ok := t.Claims.(jwt.MapClaims)
    if !ok {
        return nil, errors.New("unexpected claim type")
    }
    c := &Claims{Raw: mc}
    if v, ok := mc["sub"].(string); ok { c.Subject = v }
    if v, ok := mc["iss"].(string); ok { c.Issuer = v }
    if v, ok := mc["email"].(string); ok { c.Email = v }
    // aud may be string or []string per RFC 7519
    switch v := mc["aud"].(type) {
    case string:
        c.Audience = []string{v}
    case []any:
        for _, item := range v {
            if s, ok := item.(string); ok {
                c.Audience = append(c.Audience, s)
            }
        }
    }
    // Scopes: try "scope" (space-separated) then "scp" (array)
    if s, ok := mc["scope"].(string); ok {
        c.Scopes = strings.Fields(s)
    } else if arr, ok := mc["scp"].([]any); ok {
        for _, item := range arr {
            if s, ok := item.(string); ok {
                c.Scopes = append(c.Scopes, s)
            }
        }
    }
    return c, nil
}

func (a *Authenticator) checkRequiredScopes(c *Claims) error {
    for _, req := range a.cfg.RequiredScopes {
        if !hasScope(c.Scopes, req) {
            return fmt.Errorf("missing required scope %q", req)
        }
    }
    return nil
}

func (a *Authenticator) shouldSkip(path string) bool {
    for _, p := range a.cfg.SkipPaths {
        if path == p || (strings.HasSuffix(p, "/") && strings.HasPrefix(path, p)) ||
           strings.HasPrefix(path, p+"/") {
            return true
        }
    }
    return false
}

func hasScope(have []string, want string) bool {
    for _, s := range have {
        if s == want { return true }
    }
    return false
}

// --- context plumbing ---

type claimsContextKey struct{}

// ClaimsFromContext returns the claims attached by RequireAuth, if any.
func ClaimsFromContext(ctx context.Context) (*Claims, bool) {
    c, ok := ctx.Value(claimsContextKey{}).(*Claims)
    return c, ok
}

// --- error response (kept here to avoid importing http adapter) ---

type authErr struct {
    Error            string `json:"error"`
    ErrorDescription string `json:"error_description,omitempty"`
}

func writeAuthError(w http.ResponseWriter, status int, code, desc string) {
    w.Header().Set("WWW-Authenticate", fmt.Sprintf(`Bearer error="%s"`, code))
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    _ = jsonEncode(w, authErr{Error: code, ErrorDescription: desc})
}

func jsonEncode(w http.ResponseWriter, v any) error {
    return json.NewEncoder(w).Encode(v)
}
```

(Replace `json.NewEncoder` with the appropriate import — `encoding/json`.
Kept inline above for brevity; the generated file imports it properly.)

## Wiring in `cmd/server/main.go`

```go
authenticator, err := auth.New(cfg.Auth, logger)
if err != nil {
    return fmt.Errorf("auth init: %w", err)
}

// In routes.go, wire it into the chain:
//   protected := authenticator.RequireAuth(handler)
//   mux.Handle("GET /api/v1/widgets", protected)
```

## Wiring in `internal/adapters/http/routes.go`

```go
func RegisterRoutes(mux *http.ServeMux, h *Handlers, a *auth.Authenticator) {
    // Public
    mux.Handle("GET /healthz", http.HandlerFunc(h.Healthz))
    mux.Handle("GET /readyz",  http.HandlerFunc(h.Readyz))
    mux.Handle("GET /docs/", SwaggerHandler())

    // Protected
    requireAuth := a.RequireAuth
    mux.Handle("GET /api/v1/widgets",          requireAuth(http.HandlerFunc(h.ListWidgets)))
    mux.Handle("GET /api/v1/widgets/{id}",     requireAuth(http.HandlerFunc(h.GetWidget)))
    mux.Handle("POST /api/v1/widgets",         requireAuth(a.RequireScope("widgets:write")(http.HandlerFunc(h.CreateWidget))))
    mux.Handle("DELETE /api/v1/widgets/{id}",  requireAuth(a.RequireScope("widgets:write")(http.HandlerFunc(h.DeleteWidget))))
}
```

## Test pattern (`internal/auth/auth_test.go`)

```go
func TestAuthenticator_RequireAuth_HS256(t *testing.T) {
    secret := "test-secret-must-be-long-enough"
    cfg := Config{
        Enabled: true, Algorithm: "HS256", HMACSecret: secret,
        Issuer: "test-issuer", Audience: "test-aud",
        ClockSkew: 30 * time.Second,
    }
    a, err := New(cfg, slog.Default())
    require.NoError(t, err)

    // Build a valid HS256 token
    tok := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
        "iss": "test-issuer", "aud": "test-aud",
        "sub": "user-1", "exp": time.Now().Add(time.Hour).Unix(),
        "scope": "widgets:read widgets:write",
    })
    signed, _ := tok.SignedString([]byte(secret))

    handler := a.RequireAuth(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        c, ok := ClaimsFromContext(r.Context())
        require.True(t, ok)
        require.Equal(t, "user-1", c.Subject)
        require.Contains(t, c.Scopes, "widgets:write")
        w.WriteHeader(200)
    }))

    req := httptest.NewRequest("GET", "/api/v1/widgets", nil)
    req.Header.Set("Authorization", "Bearer "+signed)
    rr := httptest.NewRecorder()
    handler.ServeHTTP(rr, req)
    require.Equal(t, 200, rr.Code)
}
```

Add table-driven cases for: missing header, malformed header, expired
token, wrong issuer, wrong audience, wrong algorithm, missing scope.
