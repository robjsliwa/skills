#!/usr/bin/env bash
set -euo pipefail

# ---------- arg parse --------------------------------------------------------
PROJECT_NAME=""
GITHUB_USER=""
DESCRIPTION=""
DEST_DIR=""
MODULE_PATH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-name) PROJECT_NAME="$2"; shift 2 ;;
    --github-user)  GITHUB_USER="$2";  shift 2 ;;
    --description)  DESCRIPTION="$2";  shift 2 ;;
    --dest)         DEST_DIR="$2";     shift 2 ;;
    --module)       MODULE_PATH="$2";  shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

# ---------- validate required ------------------------------------------------
if [[ -z "$PROJECT_NAME" ]]; then
  echo "Error: --project-name is required" >&2; exit 1
fi
if [[ -z "$GITHUB_USER" ]]; then
  echo "Error: --github-user is required" >&2; exit 1
fi
if [[ -z "$DESCRIPTION" ]]; then
  echo "Error: --description is required" >&2; exit 1
fi

# ---------- defaults for optional params ------------------------------------
if [[ -z "$DEST_DIR" ]]; then
  DEST_DIR="."
fi
if [[ -z "$MODULE_PATH" ]]; then
  MODULE_PATH="github.com/$GITHUB_USER/$PROJECT_NAME"
fi

# ---------- locate assets ----------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARBALL="$SCRIPT_DIR/../assets/boilerplate.tar.gz"

if [[ ! -f "$TARBALL" ]]; then
  echo "Error: asset not found: $TARBALL" >&2; exit 1
fi

# ---------- extract ----------------------------------------------------------
mkdir -p "$DEST_DIR"
tar -xzf "$TARBALL" -C "$DEST_DIR"
echo "Extracted boilerplate to: $DEST_DIR"

# ---------- helper: in-place perl replace (safe for special chars) -----------
preplaceall() {
  local old="$1"; local new="$2"; shift 2
  OLD="$old" NEW="$new" perl -i -pe 's{\Q$ENV{OLD}\E}{$ENV{NEW}}g' "$@"
}

# ---------- build replacement strings ----------------------------------------
OLD_MODULE="github.com/OWNER/boilerplate"
NEW_MODULE="$MODULE_PATH"

# swaggo encodes module path slashes and dots as underscores in $ref keys
OLD_MODULE_US=$(echo "$OLD_MODULE" | tr '/.' '_')
NEW_MODULE_US=$(echo "$NEW_MODULE" | tr '/.' '_')

# ---------- 1. go.mod --------------------------------------------------------
preplaceall "$OLD_MODULE" "$NEW_MODULE" "$DEST_DIR/go.mod"

# ---------- 2. All .go files: import paths -----------------------------------
find "$DEST_DIR" -name "*.go" | while read -r f; do
  preplaceall "$OLD_MODULE" "$NEW_MODULE" "$f"
done

# ---------- 3. swaggo $ref keys in docs files --------------------------------
preplaceall "$OLD_MODULE_US" "$NEW_MODULE_US" "$DEST_DIR/docs/docs.go"
preplaceall "$OLD_MODULE_US" "$NEW_MODULE_US" "$DEST_DIR/docs/swagger.json"
preplaceall "$OLD_MODULE_US" "$NEW_MODULE_US" "$DEST_DIR/docs/swagger.yaml"

# ---------- 4. Bare "boilerplate" Go string literals (OTel, config) ----------
find "$DEST_DIR" -name "*.go" | while read -r f; do
  preplaceall '"boilerplate"' "\"$PROJECT_NAME\"" "$f"
done

# ---------- 5. Title-cased "Boilerplate API" ---------------------------------
preplaceall "Boilerplate API" "$PROJECT_NAME API" \
  "$DEST_DIR/cmd/server/main.go" \
  "$DEST_DIR/docs/docs.go" \
  "$DEST_DIR/docs/swagger.json" \
  "$DEST_DIR/docs/swagger.yaml"

# ---------- 6. Package comment in main.go ------------------------------------
preplaceall "the boilerplate HTTP service" "the $PROJECT_NAME HTTP service" \
  "$DEST_DIR/cmd/server/main.go"

# ---------- 7 & 8. Description string in main.go and docs files --------------
# Replaces the known old description text everywhere it appears (annotation line,
# docs.go string literal, swagger JSON/YAML info block)
OLD_DESC="A production-ready Go REST API boilerplate with CRUD for items."
preplaceall "$OLD_DESC" "$DESCRIPTION" \
  "$DEST_DIR/cmd/server/main.go" \
  "$DEST_DIR/docs/docs.go" \
  "$DEST_DIR/docs/swagger.json" \
  "$DEST_DIR/docs/swagger.yaml"

# ---------- 9. README.md -----------------------------------------------------
# Line 1: title
perl -i -pe "s{^# boilerplate\$}{# $PROJECT_NAME} if \$. == 1" "$DEST_DIR/README.md"

# Line 3: description prose
PROJECT_NAME_ESC="$PROJECT_NAME" DESCRIPTION_ESC="$DESCRIPTION" \
  perl -i -pe 'if ($. == 3) { s/.*/'"$DESCRIPTION"'/ }' "$DEST_DIR/README.md"

# SERVICE_NAME default in env-var table
preplaceall '`boilerplate`' "\`$PROJECT_NAME\`" "$DEST_DIR/README.md"

# Any remaining "boilerplate" word in README (e.g. prose references)
preplaceall "boilerplate" "$PROJECT_NAME" "$DEST_DIR/README.md"

# ---------- 9b. .env.example + Makefile docker tag ---------------------------
if [[ -f "$DEST_DIR/.env.example" ]]; then
  preplaceall "boilerplate" "$PROJECT_NAME" "$DEST_DIR/.env.example"
fi
if [[ -f "$DEST_DIR/Makefile" ]]; then
  preplaceall "boilerplate" "$PROJECT_NAME" "$DEST_DIR/Makefile"
fi

# ---------- 9c. LICENSE copyright line ---------------------------------------
if [[ -f "$DEST_DIR/LICENSE" ]]; then
  preplaceall "[yyyy]" "$(date +%Y)" "$DEST_DIR/LICENSE"
  preplaceall "[name of copyright owner]" "$GITHUB_USER" "$DEST_DIR/LICENSE"
fi

# ---------- 10. go mod tidy --------------------------------------------------
echo "Running go mod tidy..."
(cd "$DEST_DIR" && go mod tidy)

# ---------- done -------------------------------------------------------------
echo ""
echo "Project created:  $DEST_DIR"
echo "Module path:      $MODULE_PATH"
echo ""
echo "Next steps:"
echo "  make run        # start the server"
echo "  make swagger    # regenerate docs after editing handlers"
echo "  make build      # compile to bin/server"
