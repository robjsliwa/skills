#!/usr/bin/env bash
# verify.sh — Verify all expected files exist and the project builds + tests.
# Run as the final step. Fails with a clear list if anything is missing.
#
# Usage:
#   verify.sh \
#     --target-dir=/path/to/scaffold \
#     --database=postgres|mysql|sqlite|mongodb|none \
#     --include-cli=true|false \
#     --cli-name=NAME \
#     --auth-enabled=true|false

set -uo pipefail

TARGET_DIR=""
DATABASE=""
INCLUDE_CLI=""
CLI_NAME=""
AUTH_ENABLED=""

for arg in "$@"; do
    case "$arg" in
        --target-dir=*) TARGET_DIR="${arg#*=}" ;;
        --database=*) DATABASE="${arg#*=}" ;;
        --include-cli=*) INCLUDE_CLI="${arg#*=}" ;;
        --cli-name=*) CLI_NAME="${arg#*=}" ;;
        --auth-enabled=*) AUTH_ENABLED="${arg#*=}" ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

[ -n "$TARGET_DIR" ] || TARGET_DIR="$(pwd)"
cd "$TARGET_DIR"

MISSING=()
require() {
    if [ ! -e "$1" ]; then
        MISSING+=("$1")
    fi
}

echo "==> Verifying scaffold completeness..."

# Required regardless of options
require "go.mod"
require "Makefile"
require ".gitignore"
require ".golangci.yml"
require ".env.example"
require "deploy/Dockerfile"
require "deploy/docker-compose.yml"
require ".github/workflows/ci.yml"
require ".githooks/pre-commit"
require "cmd/server/main.go"
require "pkg/domain/types.go"
require "pkg/domain/ports.go"
require "pkg/domain/errors.go"
require "internal/core/service.go"
require "internal/config/config.go"
require "internal/adapters/http/server.go"
require "internal/adapters/http/routes.go"
require "internal/adapters/http/handlers.go"
require "internal/adapters/http/middleware.go"
require "internal/adapters/http/dto.go"
require "internal/adapters/http/decode.go"
require "internal/adapters/http/respond.go"
require "internal/adapters/http/health.go"
require "internal/adapters/http/swagger.go"
require "internal/adapters/store/memory.go"
require "internal/adapters/telemetry/otel.go"
require "internal/adapters/telemetry/slog.go"
require "README.md"
require "CLAUDE.md"
require "docs/ARCHITECTURE.md"
require "docs/MODULE_MAP.md"

# Conditional requirements
if [ "$INCLUDE_CLI" = "true" ]; then
    require "cmd/$CLI_NAME/main.go"
    require "deploy/Dockerfile.cli"
fi

if [ "$AUTH_ENABLED" = "true" ]; then
    require "internal/auth/auth.go"
    require "internal/auth/auth_test.go"
fi

case "$DATABASE" in
    postgres|mysql|sqlite)
        if ! ls migrations/001_*.up.sql >/dev/null 2>&1; then
            MISSING+=("migrations/001_*.up.sql (initial migration)")
        fi
        if ! ls migrations/001_*.down.sql >/dev/null 2>&1; then
            MISSING+=("migrations/001_*.down.sql (initial migration)")
        fi
        require "internal/adapters/store/sql.go"
        ;;
    mongodb)
        require "internal/adapters/store/mongo.go"
        ;;
esac

# Report missing files (don't exit yet — gather more info first)
if [ ${#MISSING[@]} -gt 0 ]; then
    echo "" >&2
    echo "❌ MISSING FILES:" >&2
    for f in "${MISSING[@]}"; do
        echo "   - $f" >&2
    done
    echo "" >&2
    echo "Re-run the corresponding install step or generate the missing files." >&2
    exit 1
fi

echo "✓ All required files present"

# --- Swagger generation (must run BEFORE go mod tidy/build) ---
# swag init generates docs/docs.go which imports github.com/swaggo/swag.
# If we run go mod tidy first, it won't know about that import and will
# pull the wrong version. Running swag first ensures go mod tidy resolves
# the correct swag library version matching the generated code.
echo ""
echo "==> Generating OpenAPI spec..."
if ! command -v swag >/dev/null 2>&1; then
    echo "Installing swag..."
    go install github.com/swaggo/swag/cmd/swag@v1.16.4
fi
if ! swag init -g cmd/server/main.go -o docs --parseInternal --parseDependency --quiet 2>&1; then
    echo "❌ swag init failed (likely missing or malformed annotations)" >&2
    echo "  Check handler comments and re-run: make swagger" >&2
    exit 1
fi

# --- Build verification ---
echo ""
echo "==> Running go mod tidy..."
if ! go mod tidy 2>&1; then
    echo "❌ go mod tidy failed" >&2
    exit 1
fi

echo "==> Running go build ./..."
if ! go build ./... 2>&1; then
    echo "❌ go build failed" >&2
    exit 1
fi

echo "==> Running go test ./..."
if ! go test -count=1 ./... 2>&1; then
    echo "❌ go test failed" >&2
    exit 1
fi

echo ""
echo "✅ Scaffold verified successfully"
