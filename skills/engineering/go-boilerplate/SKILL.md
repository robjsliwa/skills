---
name: go-boilerplate
description: Scaffold a new Go REST API service from the boilerplate (Chi, OpenTelemetry, Swagger).
allowed-tools: Bash(bash ~/.claude/skills/go-boilerplate/scripts/apply.sh *)
---

Gather the required parameters, then run the script. Do not perform any replacements yourself.

## Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `project_name` | yes | — | Project name in kebab-case (e.g. `my-service`) |
| `github_user` | yes | — | GitHub username or org that will own the repo (e.g. `acme`) |
| `description` | yes | — | One-sentence description of the service |
| `dest_dir` | no | `.` (current directory) | Directory to install the project files into |
| `module_path` | no | `github.com/{github_user}/{project_name}` | Full Go module path (override if not on GitHub) |

## Steps

1. Ask the user for `project_name`, `github_user`, and `description` if not already provided.
2. Run:
   ```
   bash ~/.claude/skills/go-boilerplate/scripts/apply.sh \
     --project-name "<project_name>" \
     --github-user  "<github_user>" \
     --description  "<description>" \
     [--dest        "<dest_dir>"] \
     [--module      "<module_path>"]
   ```
3. Report the script output and next steps.
