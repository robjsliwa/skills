# Profile format

`docs/agents/profile.md` is the one file every skill reads for repo facts. It is
plain markdown so a person can edit it by hand. Skills parse it loosely: a
section heading, then `Key: value` lines. Text after `#` on a line is a comment.

## The file

```markdown
# Agent profile

## Tracker
Kind: local | github | gitlab | jira | linear | other
Notes: <how to create an issue, link blockers, label; or "files under docs/planning">
Labels: ready-for-agent, in-progress, done   # triage vocabulary

## Docs
Planning: docs/planning
ADRs: docs/adr
Pairing: docs/pairing
Code-along: docs/code-along
Research: docs/research
Spikes: docs/spikes
Detours: docs/detours

## Commands
Fast tests: <cmd>
Full check: <cmd>
Run the app: <cmd>      # used for story demos

## Diagrams
Validate: npx -y @mermaid-js/mermaid-cli   # or "off"
Viewer port: 4178

## Review
Security: auto   # auto, a command or skill, or "off"
Depth: auto      # auto, quick, standard, or deep
```

Write exactly these sections and keys, in this order. `Notes` may run to several
lines: indent continuation lines by two spaces, or use a short fenced block
directly under the `Notes:` line.

## Field meanings

| Field | Meaning | Default when missing |
|---|---|---|
| Tracker / Kind | Where stories and issues are published. `local` means story files only. | `local` |
| Tracker / Notes | The recipe a skill follows to create an issue, link a blocker, and apply a label. Commands, not prose. | `files under docs/planning` |
| Tracker / Labels | The triage vocabulary, in lifecycle order. Skills map story Status onto these: `ready` to the first, `in-progress` to the second, `done` to the third. | `ready-for-agent, in-progress, done` |
| Docs / Planning | Root of `<slug>/requirements.md`, `design.md`, `phases.md`, `stories/`, `mockups/`. | `docs/planning` |
| Docs / ADRs | Folder of numbered ADRs. | `docs/adr` |
| Docs / Pairing | Pairing memory bank. | `docs/pairing` |
| Docs / Code-along | Learner state for code-along. | `docs/code-along` |
| Docs / Research | Trails (`<topic>/map.md`, nodes, findings, spikes, prototypes) and standalone research notes. | `docs/research` |
| Docs / Spikes | Spike briefs not tied to a trail, numbered. | `docs/spikes` |
| Docs / Detours | Detour briefs: a gap taken to a clean context and the answer brought back, numbered. | `docs/detours` |
| Commands / Fast tests | Runs in seconds; `tdd` runs it after every red and green. | none; ask once |
| Commands / Full check | What CI runs: lint, typecheck, all tests. Run before review. | none; ask once |
| Commands / Run the app | What a person uses to see a story's Demo. | none; Demo is described, not run |
| Diagrams / Validate | Command prefix for `mmdc`, or `off`. When off, diagrams are marked unvalidated. | `npx -y @mermaid-js/mermaid-cli` |
| Diagrams / Viewer port | Port for `visualize`'s docs viewer. | `4178` |
| Review / Security | How `review-change` fills its Security axis. `auto`: the agent's own security review if it has one, otherwise the built-in brief. A command or skill name: run that as well as the built-in brief, for example `semgrep scan --config auto` or `/security-review`. `off`: skip the axis, and the report says so. | `auto` |
| Review / Depth | How hard `review-change` looks. `auto` sets it per change from the paths touched and the size; a fixed value applies to every change. | `auto` |

## Notes recipes

Pick the one for the tracker kind and adjust names to the repo. Replace `<...>`
placeholders at use time, not in the profile.

### github (gh)

```text
Create: gh issue create --title "<title>" --body-file <story.md> --label ready-for-agent
Label:  gh issue edit <n> --add-label in-progress --remove-label ready-for-agent
Close:  gh issue close <n> --comment "Done in #<pr>"
Sub-issue (story under an epic/phase issue):
  gh api -X POST repos/{owner}/{repo}/issues/<parent>/sub_issues -F sub_issue_id=<child issue id, not number>
  (get the id with: gh api repos/{owner}/{repo}/issues/<n> --jq .id)
Blocked by:
  gh api -X POST repos/{owner}/{repo}/issues/<n>/dependencies/blocked_by -F issue_id=<blocker id>
  If the API refuses (feature not enabled), write "Blocked by #<m>" as the first body line instead.
```

Sub-issues and issue dependencies are newer GitHub features. Try them once
during setup on a read-only call (`gh api repos/{owner}/{repo}/issues/1/sub_issues`)
and write the fallback into Notes if they are unavailable.

### gitlab (glab)

```text
Create: glab issue create --title "<title>" --description "$(cat <story.md>)" --label ready-for-agent
Label:  glab issue update <n> --label in-progress --unlabel ready-for-agent
Close:  glab issue close <n>
Blocked by (Premium and up):
  glab api -X POST projects/:id/issues/<n>/links -f target_project_id=:id -f target_issue_iid=<m> -f link_type=is_blocked_by
  Otherwise: "Blocked by #<m>" as the first description line.
Epic/parent: epics need Premium; otherwise use a "phase::<n>" scoped label.
```

### jira

Write whatever the user actually uses: a CLI (`jira issue create -t Story -s "<title>" -b "<body>"`
with go-jira or jira-cli), an MCP tool name, or "web only: the agent prints the
story and the user files it". Record the project key, the issue type for a
story, the link type for blockers (usually "is blocked by"), and the label or
status names that map to the triage vocabulary.

### linear

Record the tool (Linear MCP tool name, or the `linear` CLI), the team key, how a
blocker is expressed (relation "blocked by"), and the workflow states that map
to the triage vocabulary. Linear uses states more than labels; say so in Notes.

### local

```text
Notes: files under docs/planning
  Stories: docs/planning/<slug>/stories/NN-MM-<slug>.md
  Blocked by: the story's **Blocked by:** line, story ids
  Labels: the story's **Status:** line (ready, in-progress, done)
```

No issues are created. Status lives in the story file and `phases.md`.

### other

Freeform: the user's own words on how to create, link, and label, plus any
command they gave. If they file by hand, the recipe is "print the story; the
user files it and replies with the id".
