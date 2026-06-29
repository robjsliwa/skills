# Database Adapter Reference

Per-database guidance for the `internal/adapters/store/` package.

> **NOTE:** Code examples below use `Widget`/`WidgetRepository` as a
> placeholder. Replace with the actual domain entity derived from the
> project description (e.g., `Task`/`TaskRepository`, `Order`/`OrderRepository`).
> Adapt table/collection names and column/field definitions accordingly.

The chosen adapter implements the domain repository interface (e.g.,
`domain.{Entity}Repository`).

The in-memory adapter (`memory.go`) is **always** generated regardless of
the database choice — used in unit tests and as the implementation when
`database=none`.

## Common Pattern

Every adapter exposes:

```go
type Store struct {
    // driver-specific fields
}

func New(cfg Config) (*Store, error) { ... }

func (s *Store) Close() error { ... }
func (s *Store) Ping(ctx context.Context) error { ... }

// domain.WidgetRepository implementation:
func (s *Store) Create(ctx context.Context, w *domain.Widget) error
func (s *Store) Get(ctx context.Context, id string) (*domain.Widget, error)
func (s *Store) List(ctx context.Context) ([]*domain.Widget, error)
func (s *Store) Delete(ctx context.Context, id string) error
```

Domain errors:
- Not found → `domain.ErrNotFound`
- Already exists → `domain.ErrAlreadyExists`
- Other errors wrapped: `fmt.Errorf("store: create widget: %w", err)`

## none

No driver. Only `memory.go` is generated. `cmd/server/main.go` instantiates
the in-memory store directly.

```go
store := memory.New()
```

`.env.example` has no DB section.

## postgres

**Driver:** `github.com/jackc/pgx/v5/stdlib` used with `database/sql`.
**Migrations:** `golang-migrate` with `file://migrations`.

**Config (env):**
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=<project_name>
DB_USER=<project_name>
DB_PASSWORD=
DB_SSLMODE=disable
DB_MAX_OPEN_CONNS=25
DB_MAX_IDLE_CONNS=5
DB_CONN_MAX_LIFETIME=5m
```

**DSN in `internal/config/`:**
```go
func (c *Config) DSN() string {
    return fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
        c.DBHost, c.DBPort, c.DBUser, c.DBPassword, c.DBName, c.DBSSLMode)
}
```

**Initial migration `migrations/001_create_widgets.up.sql`:**
```sql
CREATE TABLE widgets (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_widgets_name ON widgets(name);
```

Down migration drops the table.

**Compose service:**
```yaml
postgres:
  image: postgres:16-alpine
  environment:
    POSTGRES_DB: ${DB_NAME}
    POSTGRES_USER: ${DB_USER}
    POSTGRES_PASSWORD: ${DB_PASSWORD}
  ports: ["5432:5432"]
  volumes: ["pgdata:/var/lib/postgresql/data"]
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
    interval: 5s
```

## mysql

**Driver:** `github.com/go-sql-driver/mysql`. `database/sql` interface.
**Migrations:** `golang-migrate` with `mysql://` URL.

**Config (env):** same shape as postgres but `DB_PORT=3306` and
`DB_PARAMS=parseTime=true&charset=utf8mb4`.

**DSN:**
```go
fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?%s", user, pwd, host, port, name, params)
```

**Initial migration:** `id CHAR(36)` for readability. Switch to
`BINARY(16)` later for storage efficiency.

**Compose:** `mysql:8.0` with healthcheck `mysqladmin ping`.

## sqlite

**Driver:** `modernc.org/sqlite` (pure Go, no CGO). Friendlier for
cross-compilation and Docker.

**Config (env):**
```
DB_PATH=./data/<project_name>.db
```

**Connection:**
```go
db, err := sql.Open("sqlite", cfg.DBPath)
```

Migrations: `golang-migrate` with `sqlite://` URL.

**Initial migration:**
```sql
CREATE TABLE widgets (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

No compose service; data lives at `DB_PATH`. Add `data/` to `.gitignore`.

## mongodb

**Driver:** `go.mongodb.org/mongo-driver/v2`.

**Config (env):**
```
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=<project_name>
MONGO_TIMEOUT=10s
```

**Connection:**
```go
client, err := mongo.Connect(options.Client().ApplyURI(cfg.MongoURI))
```

No migrations — define indexes programmatically in `New()`:

```go
func New(cfg Config) (*Store, error) {
    client, err := mongo.Connect(options.Client().ApplyURI(cfg.URI))
    if err != nil { return nil, err }
    coll := client.Database(cfg.Database).Collection("widgets")
    _, err = coll.Indexes().CreateOne(ctx, mongo.IndexModel{
        Keys: bson.D{{"name", 1}},
    })
    // ...
}
```

**Compose:**
```yaml
mongo:
  image: mongo:7
  ports: ["27017:27017"]
  volumes: ["mongodata:/data/db"]
```

## Integration Test Pattern (SQL DBs)

`internal/adapters/store/store_test.go` uses `testcontainers-go`:

```go
//go:build integration

func TestStore(t *testing.T) {
    ctx := context.Background()
    container, err := postgres.Run(ctx, "postgres:16-alpine",
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
    )
    // ... run migrations ...
    // ... exercise store methods ...
}
```

Run via `make test-integration` (`go test -tags=integration ./...`).

For MongoDB, use `testcontainers-go/modules/mongodb`.
For SQLite, no container needed — use `t.TempDir()` for the DB file.
