#!/usr/bin/env bash
# bootstrap.sh — Create directory structure and initialize git/Go module
#
# Usage:
#   bootstrap.sh \
#     --project-name=NAME \
#     --module=github.com/owner/repo \
#     --database=postgres|mysql|sqlite|mongodb|none \
#     --include-cli=true|false \
#     --cli-name=NAME \
#     --auth-enabled=true|false \
#     --target-dir=/path/to/scaffold \
#     --git-init=true|false

set -euo pipefail

# --- Parse args ---
PROJECT_NAME=""
MODULE=""
DATABASE=""
INCLUDE_CLI=""
CLI_NAME=""
AUTH_ENABLED=""
TARGET_DIR=""
GIT_INIT="true"

for arg in "$@"; do
    case "$arg" in
        --project-name=*) PROJECT_NAME="${arg#*=}" ;;
        --module=*) MODULE="${arg#*=}" ;;
        --database=*) DATABASE="${arg#*=}" ;;
        --include-cli=*) INCLUDE_CLI="${arg#*=}" ;;
        --cli-name=*) CLI_NAME="${arg#*=}" ;;
        --auth-enabled=*) AUTH_ENABLED="${arg#*=}" ;;
        --target-dir=*) TARGET_DIR="${arg#*=}" ;;
        --git-init=*) GIT_INIT="${arg#*=}" ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

# --- Validate ---
[ -n "$PROJECT_NAME" ] || { echo "Missing --project-name" >&2; exit 1; }
[ -n "$MODULE" ] || { echo "Missing --module" >&2; exit 1; }
[ -n "$DATABASE" ] || { echo "Missing --database" >&2; exit 1; }
[ -n "$INCLUDE_CLI" ] || { echo "Missing --include-cli" >&2; exit 1; }
[ -n "$AUTH_ENABLED" ] || { echo "Missing --auth-enabled" >&2; exit 1; }
[ -n "$TARGET_DIR" ] || TARGET_DIR="$(pwd)"

if [ "$INCLUDE_CLI" = "true" ] && [ -z "$CLI_NAME" ]; then
    echo "Missing --cli-name (required when --include-cli=true)" >&2
    exit 1
fi

case "$DATABASE" in
    none|postgres|mysql|sqlite|mongodb) ;;
    *) echo "Invalid --database=$DATABASE (must be: none|postgres|mysql|sqlite|mongodb)" >&2; exit 1 ;;
esac

# --- Pre-flight ---
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# Reject if existing source files (allow dotfiles only)
shopt -s nullglob
existing_source=$(find . -maxdepth 2 -type f \
    \( -name '*.go' -o -name 'go.mod' -o -name 'Makefile' \) 2>/dev/null | head -1)
if [ -n "$existing_source" ]; then
    echo "Target dir contains existing source files (e.g. $existing_source); refusing to overwrite" >&2
    exit 1
fi

# Verify Go version >= 1.22
if ! command -v go >/dev/null 2>&1; then
    echo "go not found on PATH" >&2
    exit 1
fi
GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//' | cut -d. -f1,2)
GO_MAJOR=$(echo "$GO_VERSION" | cut -d. -f1)
GO_MINOR=$(echo "$GO_VERSION" | cut -d. -f2)
if [ "$GO_MAJOR" -lt 1 ] || { [ "$GO_MAJOR" -eq 1 ] && [ "$GO_MINOR" -lt 22 ]; }; then
    echo "Go 1.22+ required (found $GO_VERSION)" >&2
    exit 1
fi

# --- Create directory tree ---
echo "==> Creating directory structure..."

mkdir -p \
    .github/workflows \
    .githooks \
    cmd/server \
    pkg/domain \
    internal/adapters/http \
    internal/adapters/store \
    internal/adapters/telemetry \
    internal/core \
    internal/config \
    deploy \
    docs \
    scripts

if [ "$INCLUDE_CLI" = "true" ]; then
    mkdir -p "cmd/$CLI_NAME"
fi

if [ "$AUTH_ENABLED" = "true" ]; then
    mkdir -p internal/auth
fi

case "$DATABASE" in
    postgres|mysql|sqlite) mkdir -p migrations ;;
esac

# --- Initialize Go module ---
echo "==> Initializing Go module: $MODULE"
go mod init "$MODULE" >/dev/null

# --- Initialize git repo ---
if [ "$GIT_INIT" = "true" ]; then
    if [ ! -d .git ]; then
        echo "==> Initializing git repository"
        git init -q
        git config core.hooksPath .githooks 2>/dev/null || true
    fi
fi

# --- Output state for the orchestrator ---
cat <<EOF

✓ bootstrap complete
  project_name:  $PROJECT_NAME
  module:        $MODULE
  database:      $DATABASE
  include_cli:   $INCLUDE_CLI
  cli_name:      ${CLI_NAME:-<none>}
  auth_enabled:  $AUTH_ENABLED
  target_dir:    $TARGET_DIR

Next: run install-static.sh to install non-Go assets.
EOF
