---
name: repo-setup
description: >-
  Set a repo up for these skills, once: explore what is already there, ask only
  what remains (one question per turn, with a recommendation), and write
  docs/agents/profile.md with the tracker, docs locations, test and run
  commands, and diagram settings every other skill reads. Migrates v1 repos
  (the v1 docs/agents/issue-tracker.md, a glossary-style CONTEXT.md). Re-running edits
  the profile in place. Use when the user says "set up this repo," "configure
  the skills," "/repo-setup," or when a skill finds no profile and the user
  wants one.
argument-hint: "Nothing. Re-run any time to change an answer; the profile is edited in place."
---

# Repo Setup

Every skill in this repo needs the same handful of facts: where issues go, where
docs live, how to run the fast tests, the full check, and the app, and whether
Mermaid diagrams get validated. This skill finds them once and writes them to
`docs/agents/profile.md`. Everything else reads that file.

Run it once per repo. Running it again is safe: it reads the existing profile,
shows what it holds, and edits only what changes. Never delete fields the user
filled in by hand.

## The rules

1. **Explore first, ask second.** Anything the repo already answers is not a
   question. Read the manifest before asking for the test command.
2. **One question per turn, with a recommendation.** State what you found, what
   you recommend, and why. The user confirms or overrides. No questionnaires.
3. **Edit in place, never clobber.** `CLAUDE.md`, `AGENTS.md`, `.gitignore`, and
   an existing profile keep everything you did not write.

## Step 1: Explore

Read, quietly, before saying anything:

- **Manifests and build files:** `package.json` scripts, `pyproject.toml`,
  `go.mod`, `Cargo.toml`, `Makefile`, `justfile`, `Taskfile.yml`, `build.gradle`,
  `pom.xml`, `*.csproj`. These give the test, check, and run commands.
- **CI:** `.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`, and similar. CI
  usually holds the real full check (lint, typecheck, tests) in one place.
- **Remote:** `git remote -v`. A `github.com` remote suggests GitHub, a GitLab
  host suggests GitLab. Check whether `gh` or `glab` is installed and logged in
  (`gh auth status`, `glab auth status`).
- **Existing agent docs:** `docs/agents/profile.md` (a re-run), the v1
  `docs/agents/issue-tracker.md` (v1), `CLAUDE.md`, `AGENTS.md`.
- **The spine:** `CONTEXT.md`, `GLOSSARY.md`, `docs/adr/`, `docs/planning/`,
  `docs/pairing/`, `docs/code-along/`.
- **Diagram tooling:** `node --version`, `npx --version`, and `mmdc --version`.

Then give the user a short summary: what you found, what you will propose, and
how many questions remain. A typical repo needs three to five.

## Step 2: Ask what remains

Walk these in order and skip any the exploration settled beyond doubt. Even then,
show the value you will write so the user can catch a wrong guess.

1. **Tracker.** Kind: `github`, `gitlab`, `jira`, `linear`, `local`, or `other`
   (described freeform). Recommend from the remote and the installed CLIs: a
   GitHub remote with `gh` logged in means `github`. No remote, or the user
   does not want issues, means `local` (stories stay as files under the
   planning folder). For `jira`, `linear`, or `other`, ask how they file an
   issue today (CLI, MCP tool, web only) and write that down as the Notes.
2. **How to file, link, and label.** Propose the Notes recipe for the chosen
   kind from [PROFILE-FORMAT.md](PROFILE-FORMAT.md): how to create an issue,
   how to mark one blocked by another, how to apply a label. Confirm it works
   if you can do so read-only (`gh label list`, `glab label list`).
3. **Triage labels.** Recommend `ready-for-agent, in-progress, done`. If the
   tracker already has labels that mean the same, use those names instead and
   say which maps to which.
4. **Docs locations.** Recommend the defaults: `docs/planning`, `docs/adr`,
   `docs/pairing`, `docs/code-along`, `docs/research`, `docs/spikes`,
   `docs/detours`. Only ask
   if the repo already keeps
   planning or ADRs somewhere else.
5. **Commands.** Fast tests (seconds, run after every change), full check (what
   CI runs), and run the app (what a person uses to see a story's Demo). Propose
   each from the manifest and CI. If there is no app to run (a library), say so
   and recommend the command that best shows behaviour to a person, such as an
   example script or a REPL line.
6. **Diagram validation.** If `npx` works, recommend
   `npx -y @mermaid-js/mermaid-cli`, or `mmdc` if it is already installed. If
   Node is missing, recommend `off` and say diagrams will be written and marked
   unvalidated. Viewer port defaults to `4178`; ask only if that port is taken.

## Step 3: Migrate v1 artifacts

Do this between the questions above where it fits, still one question per turn.

**docs/agents/issue-tracker.md (v1).** If it exists, its content becomes the Tracker
section: kind, the commands it describes as Notes, labels. Write the profile,
then replace the old file's content with one line:

```markdown
Moved to [profile.md](profile.md) (Tracker section).
```

**A glossary-style CONTEXT.md.** v1 wrote term definitions to `CONTEXT.md`. If
it is mostly bold terms with definitions and has no picture of the system, its
actors, or its boundary, offer the split (ADR 0002 in this repo's design):

- Move the terms into `GLOSSARY.md` in the format owned by `glossary`
  (the `glossary` skill's `GLOSSARY-FORMAT.md`). Merge with an existing
  `GLOSSARY.md` rather than overwrite; flag any term defined differently in the
  two files and settle it with the user.
- Redraw `CONTEXT.md` as system context in `glossary`'s CONTEXT format, with the
  C4 level 1 diagram drawn through `visualize`. You will need the actors and the
  external systems: propose them from the code and the old file, then use a
  "show, then ask" turn (see `interview`) to correct the picture.

Recommend doing the split now when the file is small, and deferring it to the
first `interview` align session when the system context is unclear. Either way,
record the choice in the summary.

## Step 4: Write

1. **`docs/agents/profile.md`**, exactly in the format in
   [PROFILE-FORMAT.md](PROFILE-FORMAT.md). On a re-run, change only the fields
   that changed.
2. **`.gitignore`**: append `.viewer/` if it is not already there. Create the
   file if the repo has none.
3. **The agent contract file.** Use `CLAUDE.md` if it exists, else `AGENTS.md`
   if that exists, else create `CLAUDE.md`. Add or replace one block, matched by
   its heading, and leave everything else byte for byte:

   ```markdown
   ## Agent skills

   - Profile (tracker, commands, diagrams): [docs/agents/profile.md](docs/agents/profile.md)
   - System context: [CONTEXT.md](CONTEXT.md)
   - Language, terms to use and avoid: [GLOSSARY.md](GLOSSARY.md)
   - Decisions: [docs/adr/](docs/adr/)
   ```

   Keep the links even if a target does not exist yet; the next skills create
   them.
4. If diagram validation is on and the repo already has Mermaid blocks, offer to
   run `python3 the visualize skill's scripts/mermaid_check.py` over them and
   report failures. Do not fix them unasked.

Do not commit. Show the user the diff of every file you touched.

## Step 5: Hand off

End with a short recap of the profile (one line per section) and the next step:
run `/start`, which reads the repo state and recommends a mode.

## When another skill finds no profile

Skills fall back to the defaults in the profile format and say once that
`/repo-setup` would make them explicit. If the user says yes, run this skill,
then return to the caller.
