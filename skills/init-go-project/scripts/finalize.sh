#!/usr/bin/env bash
# finalize.sh — install hooks, stage, and commit the scaffold.
#
# Usage: finalize.sh --target-dir=/path/to/scaffold

set -euo pipefail

TARGET_DIR=""
for arg in "$@"; do
    case "$arg" in
        --target-dir=*) TARGET_DIR="${arg#*=}" ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done
[ -n "$TARGET_DIR" ] || TARGET_DIR="$(pwd)"
cd "$TARGET_DIR"

# Only run if git repo exists
if [ ! -d .git ]; then
    echo "Not a git repo; skipping finalize"
    exit 0
fi

echo "==> Installing pre-commit hook"
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit

echo "==> Staging scaffold"
git add .

echo "==> Initial commit"
git -c user.email="scaffold@local" -c user.name="init-go-project" \
    commit -q -m "Initial scaffold from init-go-project skill" || {
    echo "(commit may have been skipped if user already committed)"
}

echo "✓ Repository finalized"
git log --oneline -1 2>/dev/null || true
