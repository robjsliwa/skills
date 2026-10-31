#!/usr/bin/env python3
"""Repo checks for skills: frontmatter, duplicate names, independence.

Usage: python3 scripts/check-skills.py [--root DIR]

1. Every skills/**/SKILL.md (outside skills/deprecated) starts with YAML
   frontmatter whose `name` equals its folder name and whose `description`
   is non-empty.
   Column-zero lines inside the frontmatter must be keys, which catches a block
   scalar that lost its indent (invalid YAML: installers skip the skill).
2. No two skills share a name.
3. Independence: no file under skills/ (outside deprecated) mentions a v1
   dependency, except on lines that say "replaces", "v1", "migrat..." or
   "attribution".
4. Every skills/deprecated/*/SKILL.md sets `metadata.internal: true`, which
   hides it from `npx skills`.

Exits 1 if any check fails. Python 3 standard library only.
"""

import argparse
import os
import re
import sys

DEPENDENCY_RE = re.compile(
    r"mattpocock|grill-with-docs|setup-matt-pocock-skills|domain-modeling|"
    r"diagnosing-bugs|design-interview|docs/agents/issue-tracker\.md"
)
PERMITTED_RE = re.compile(r"replaces|v1|migrat|attribution", re.IGNORECASE)
TEXT_EXTS = {".md", ".py", ".sh", ".js", ".mjs", ".ts", ".json", ".yaml", ".yml",
             ".toml", ".txt", ".html", ".css", ".go"}


def parse_frontmatter(text):
    """Minimal YAML frontmatter reader for top-level scalar keys.

    Handles `key: value`, quoted values, and block scalars (`>-`, `|`, etc.).
    Returns a dict, or None when there is no frontmatter.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None
    data, key, block = {}, None, None
    for line in lines[1:end]:
        if block is not None:
            if line.startswith((" ", "\t")) or not line.strip():
                block.append(line.strip())
                continue
            data[key] = " ".join(s for s in block if s).strip()
            block = None
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            if line.strip() and not line.startswith((" ", "\t", "#")):
                data["__invalid__"] = line.strip()
            continue
        key, value = m.group(1), m.group(2).strip()
        if re.fullmatch(r"[>|][+-]?", value):
            block = []
        else:
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                value = value[1:-1]
            data[key] = value
    if block is not None:
        data[key] = " ".join(s for s in block if s).strip()
    return data


def walk(root):
    for dirpath, dirs, files in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        dirs[:] = sorted(d for d in dirs
                         if not d.startswith(".") and d != "node_modules"
                         and not (rel == "." and d == "deprecated"))
        for f in sorted(files):
            yield os.path.join(dirpath, f)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    opts = ap.parse_args()
    root = os.path.realpath(opts.root)
    skills_dir = os.path.join(root, "skills")
    if not os.path.isdir(skills_dir):
        print(f"no skills/ directory under {root}")
        return 1

    problems = {"frontmatter": [], "duplicates": [], "independence": [], "deprecated": []}
    names = {}
    skill_count = 0

    for path in walk(skills_dir):
        rel = os.path.relpath(path, root)
        if os.path.basename(path) == "SKILL.md":
            skill_count += 1
            folder = os.path.basename(os.path.dirname(path))
            with open(path, encoding="utf-8") as fh:
                fm = parse_frontmatter(fh.read())
            if fm is None:
                problems["frontmatter"].append(f"{rel}: no YAML frontmatter")
            else:
                if "__invalid__" in fm:
                    problems["frontmatter"].append(f"{rel}: not a YAML key: {fm['__invalid__'][:60]}")
                name = fm.get("name", "")
                if not name:
                    problems["frontmatter"].append(f"{rel}: missing name")
                elif name != folder:
                    problems["frontmatter"].append(f"{rel}: name '{name}' != folder '{folder}'")
                if not fm.get("description"):
                    problems["frontmatter"].append(f"{rel}: missing or empty description")
                if name:
                    names.setdefault(name, []).append(rel)

        if os.path.splitext(path)[1].lower() not in TEXT_EXTS:
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                for n, line in enumerate(fh, start=1):
                    if DEPENDENCY_RE.search(line) and not PERMITTED_RE.search(line):
                        hit = DEPENDENCY_RE.search(line).group(0)
                        problems["independence"].append(f"{rel}:{n}: '{hit}': {line.strip()[:100]}")
        except UnicodeDecodeError:
            continue

    deprecated_dir = os.path.join(skills_dir, "deprecated")
    for entry in sorted(os.listdir(deprecated_dir)) if os.path.isdir(deprecated_dir) else []:
        path = os.path.join(deprecated_dir, entry, "SKILL.md")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                if not re.search(r"^metadata:\n  internal: true$", fh.read(), re.M):
                    problems["deprecated"].append(f"{os.path.relpath(path, root)}: missing metadata.internal: true")

    for name, paths in sorted(names.items()):
        if len(paths) > 1:
            problems["duplicates"].append(f"'{name}' in " + ", ".join(paths))

    labels = {
        "frontmatter": "Frontmatter (name matches folder, description present)",
        "duplicates": "Unique skill names",
        "independence": "Independence (no v1 dependency references)",
        "deprecated": "Deprecated skills hidden from installers",
    }
    failed = False
    print(f"Checked {skill_count} skills under {os.path.relpath(skills_dir, os.getcwd())} (skipping deprecated)\n")
    for key, label in labels.items():
        items = problems[key]
        print(f"{'PASS' if not items else 'FAIL'}  {label}" + (f": {len(items)} problem(s)" if items else ""))
        for item in items:
            print(f"      {item}")
        failed = failed or bool(items)
    print("\nAll checks passed." if not failed else "\nChecks failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
