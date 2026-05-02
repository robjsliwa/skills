#!/usr/bin/env bash
# Links all skills from this repo into ~/.claude/skills/ as symlinks.
# Run after cloning: bash scripts/link-skills.sh

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

mkdir -p "$SKILLS_DIR"

find "$REPO/skills" -name "SKILL.md" | while read -r skill_md; do
    skill_dir="$(dirname "$skill_md")"
    skill_name="$(basename "$skill_dir")"
    target="$SKILLS_DIR/$skill_name"
    ln -sfn "$skill_dir" "$target"
    echo "Linked: $skill_name → $target"
done

echo ""
echo "Done. Restart Claude Code (or start a new session) to pick up the skills."
