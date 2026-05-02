#!/usr/bin/env bash
# Lists all skills available in this repo.

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"

find "$REPO/skills" -name "SKILL.md" | while read -r skill_md; do
    dirname "$skill_md"
done | sort
