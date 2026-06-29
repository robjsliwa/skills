#!/usr/bin/env bash
# install-static.sh — Copy static assets from skill bundle into target dir,
# performing {{PLACEHOLDER}} substitution and activating the selected database
# sections in docker-compose.yml and .env.example.
#
# Usage:
#   install-static.sh \
#     --skill-dir=/path/to/init-go-project \
#     --target-dir=/path/to/scaffold \
#     --project-name=NAME \
#     --module=github.com/owner/repo \
#     --include-cli=true|false \
#     --cli-name=NAME \
#     --database=postgres|mysql|sqlite|mongodb|none \
#     --description="Project description text"

set -euo pipefail

SKILL_DIR=""
TARGET_DIR=""
PROJECT_NAME=""
MODULE=""
INCLUDE_CLI=""
CLI_NAME=""
DATABASE=""
DESCRIPTION=""

for arg in "$@"; do
    case "$arg" in
        --skill-dir=*) SKILL_DIR="${arg#*=}" ;;
        --target-dir=*) TARGET_DIR="${arg#*=}" ;;
        --project-name=*) PROJECT_NAME="${arg#*=}" ;;
        --module=*) MODULE="${arg#*=}" ;;
        --include-cli=*) INCLUDE_CLI="${arg#*=}" ;;
        --cli-name=*) CLI_NAME="${arg#*=}" ;;
        --database=*) DATABASE="${arg#*=}" ;;
        --description=*) DESCRIPTION="${arg#*=}" ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

[ -n "$SKILL_DIR" ] || { echo "Missing --skill-dir" >&2; exit 1; }
[ -n "$TARGET_DIR" ] || { echo "Missing --target-dir" >&2; exit 1; }
[ -n "$PROJECT_NAME" ] || { echo "Missing --project-name" >&2; exit 1; }
[ -n "$MODULE" ] || { echo "Missing --module" >&2; exit 1; }
[ -n "$INCLUDE_CLI" ] || { echo "Missing --include-cli" >&2; exit 1; }
[ -n "$DESCRIPTION" ] || DESCRIPTION="$PROJECT_NAME — a Go REST API service"

ASSETS="$SKILL_DIR/assets"
[ -d "$ASSETS" ] || { echo "Assets dir not found: $ASSETS" >&2; exit 1; }

# Map database choice to golang-migrate driver build tag
case "${DATABASE:-none}" in
    postgres) DB_DRIVER_TAG="postgres" ;;
    mysql)    DB_DRIVER_TAG="mysql" ;;
    sqlite)   DB_DRIVER_TAG="sqlite3" ;;
    mongodb)  DB_DRIVER_TAG="mongodb" ;;
    *)        DB_DRIVER_TAG="" ;;
esac

# Detect installed Go version (major.minor) so Dockerfiles match go.mod
GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//' | cut -d. -f1,2)

cd "$TARGET_DIR"

# Helper: copy template file with {{PLACEHOLDER}} substitution
substitute() {
    local src="$1"
    local dst="$2"
    sed -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
        -e "s|{{MODULE}}|$MODULE|g" \
        -e "s|{{CLI_NAME}}|${CLI_NAME:-cli}|g" \
        -e "s|{{DB_DRIVER_TAG}}|$DB_DRIVER_TAG|g" \
        -e "s|{{GO_VERSION}}|$GO_VERSION|g" \
        "$src" > "$dst"
}

# Activate the selected database section in docker-compose.yml.
# Uncomments the chosen DB service, depends_on, and volume; removes the rest.
activate_db_compose() {
    local file="$1"
    local db="$2"

    if [ "$db" = "none" ] || [ -z "$db" ]; then
        # No database — remove all DB-related sections
        awk '
            /^## DEPENDS_ON$/   { skip=1; next }
            /^## \/DEPENDS_ON$/ { skip=0; next }
            /^## DB:/           { skip=1; next }
            /^## \/DB:/         { skip=0; next }
            /^## VOLUMES$/      { skip=1; next }
            /^## \/VOLUMES$/    { skip=0; next }
            !skip
        ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
    else
        awk -v db="$db" '
            /^## DEPENDS_ON$/   { in_dep=1; next }
            /^## \/DEPENDS_ON$/ { in_dep=0; next }
            /^## DB:/           { split($0, a, ":"); cur=a[2]; in_db=1; next }
            /^## \/DB:/         { in_db=0; cur=""; next }
            /^## VOLUMES$/      { in_vol_sec=1; next }
            /^## \/VOLUMES$/    { in_vol_sec=0; next }
            /^## VOL:/          { split($0, a, ":"); cur_vol=a[2]; in_vol=1; next }
            /^## \/VOL:/        { in_vol=0; cur_vol=""; next }

            # depends_on: uncomment for databases that run as a service
            in_dep && (db == "postgres" || db == "mysql" || db == "mongodb") {
                sub(/^    # /, "    "); print; next
            }
            in_dep { next }

            # DB service: uncomment selected, drop others
            in_db && cur == db { sub(/^  # /, "  "); print; next }
            in_db              { next }

            # volumes: header — uncomment when any DB needs a volume
            in_vol_sec && !in_vol { sub(/^# /, ""); print; next }

            # volume entries: uncomment selected, drop others
            in_vol && cur_vol == db { sub(/^# /, ""); print; next }
            in_vol                  { next }

            { print }
        ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
    fi
}

# Activate the selected database section in .env.example.
# Uncomments the chosen DB settings; removes the rest.
activate_db_env() {
    local file="$1"
    local db="$2"

    if [ "$db" = "none" ] || [ -z "$db" ]; then
        # No database — remove all DB sections
        awk '
            /^## DB:/   { skip=1; next }
            /^## \/DB:/ { skip=0; next }
            !skip
        ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
    else
        awk -v db="$db" '
            /^## DB:/ {
                split($0, a, ":"); cur=a[2]; in_db=1; next
            }
            /^## \/DB:/ { in_db=0; cur=""; next }
            in_db && cur == db {
                if (/^## /) { sub(/^## /, "# "); print; next }
                sub(/^# /, ""); print; next
            }
            in_db { next }
            { print }
        ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
    fi
}

echo "==> Installing static assets..."

# Top-level files
substitute "$ASSETS/Makefile.tmpl"            Makefile
substitute "$ASSETS/gitignore.tmpl"           .gitignore
substitute "$ASSETS/golangci.yml.tmpl"        .golangci.yml
substitute "$ASSETS/env.example.tmpl"         .env.example

# README — substitute standard placeholders, then description via perl (safe for special chars)
substitute "$ASSETS/README.md.tmpl"           README.md
export DESCRIPTION
perl -pi -e '
  BEGIN { $d = $ENV{"DESCRIPTION"}; $d =~ s/\\/\\\\/g; }
  s/\{\{DESCRIPTION\}\}/$d/g
' README.md

# Deploy
substitute "$ASSETS/Dockerfile.tmpl"          deploy/Dockerfile
substitute "$ASSETS/docker-compose.yml.tmpl"  deploy/docker-compose.yml

# CLI Dockerfile only if CLI requested (separate image for ops use)
if [ "$INCLUDE_CLI" = "true" ]; then
    substitute "$ASSETS/Dockerfile.cli.tmpl"  "deploy/Dockerfile.cli"
fi

# CI / hooks
substitute "$ASSETS/github-workflow-ci.yml.tmpl"   .github/workflows/ci.yml
substitute "$ASSETS/pre-commit-hook.sh.tmpl"       .githooks/pre-commit
chmod +x .githooks/pre-commit


# --- Activate selected database sections ---
echo "==> Activating database sections (${DATABASE:-none})..."
activate_db_compose deploy/docker-compose.yml "${DATABASE:-none}"
activate_db_env     .env.example              "${DATABASE:-none}"

echo "✓ Static assets installed"

# Sanity check: list what was created
echo ""
echo "Files created at top level and in deploy/.github/.githooks:"
ls -la Makefile .gitignore .golangci.yml .env.example README.md 2>/dev/null | awk '{print "  ", $NF}'
ls -la deploy/ 2>/dev/null | awk 'NR>1{print "  deploy/" $NF}'
ls -la .github/workflows/ 2>/dev/null | awk 'NR>1{print "  .github/workflows/" $NF}'
ls -la .githooks/ 2>/dev/null | awk 'NR>1{print "  .githooks/" $NF}'
