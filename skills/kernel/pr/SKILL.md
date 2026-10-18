---
name: pr
description: >-
  Write and open the pull request for a finished change, in every flow: a
  body with why, a Mermaid picture of the change in the type that fits it
  (sequence, before/after, state, data), a what, why, and how row for every
  concern, the rationale journal with its dead ends, decisions, and evidence.
  Builds from the journal (a pairing slice's or a story's), the ADRs, and the
  diff, never from memory of the chat. Use whenever a PR or merge request is
  opened or its description written or refreshed: when the user says "open a
  PR," "create a pull request," "write the PR description," "ship this," after
  tdd or code-along finishes a story, or when pair-ship reaches its PR stage.
argument-hint: "Optional: the story or slice file. Inferred from the branch when omitted."
---

# PR

The PR is the permanent record of why the code is the way it is. A reviewer
who was not in the room should be able to agree or disagree with every
choice, and someone reading `git blame` in a year should find the reason.
That only works if the body is built from notes written while the work
happened, so this skill reads the journal first and the chat never.

Template: [assets/pr-template.md](assets/pr-template.md). Every flow uses it;
`pair-ship` calls this skill for its PR stage.

## 1. Find the sources

Read, in this order:

1. **The journal.** Whichever exists for this branch:
   - a pairing slice, `docs/pairing/slices/NNNN-<slug>.md`, `## Journal`
     (format in the `pairing` skill's MEMORY-BANK.md);
   - a story file's `## Journal` and `## As built` (written by `tdd`);
   - a `code-along` debrief for the story (`docs/code-along/`).
2. **The spec**: the story's Scenario, Demo, Acceptance, or the slice's
   goal and acceptance.
3. **Decisions**: ADRs added or changed on the branch, `GLOSSARY.md` and
   `CONTEXT.md` diffs.
4. **The change**: `git log --reverse <base>..HEAD` and
   `git diff <base>...HEAD`, where `<base>` is `git merge-base <default> HEAD`.
5. **Evidence**: the review reports if `review-change` ran, and the last
   full check run.

**No journal?** Reconstruct one before writing: walk the commits oldest
first and, for each, write a journal entry (What, Why, How, Evidence,
Considered) into the story file, or into the PR scratch file when there is
no story. Ask the user one question at a time for any Why the commits and
diff cannot answer. Mark reconstructed entries `(reconstructed)` so the
reviewer knows they were written after the fact. Never invent a reason.

## 2. Draw the picture

One Mermaid diagram in `## Summary`, drawn per the `visualize` skill's
NOTATION.md (glossary terms as labels, about 12 nodes, a caption sentence).
Pick the type from what the change did to the system:

| The change | Diagram |
|---|---|
| Alters who calls whom, in what order, or adds a hop (API, queue, retry, auth) | `sequenceDiagram`, changed messages marked with `rect` or a note |
| Moves, adds, or removes components or dependencies | before/after `flowchart`, changed parts with a class |
| Changes a lifecycle, status, or workflow | `stateDiagram-v2`, new transitions marked |
| Changes a schema or data shape | `erDiagram` of the touched entities |
| Changes a calculation or decision rule | `flowchart` of the rule, before and after |
| Changes what a user sees, step to step | `journey` or a screen flow |

When two apply, draw the one the reviewer most needs to judge the risk,
usually the sequence. Validate it with `mmdc` as `visualize` says before it
goes in the body.

Skip the diagram only when the change has no shape to draw: a typo, a
version bump, a config value, a dependency update with no code change. Then
write one line in its place saying why: "No diagram: copy change only."

## 3. Write the body

Fill [assets/pr-template.md](assets/pr-template.md). Write it to a scratch
file outside the repo (under `$TMPDIR`), or where the caller says (local
mode in `pair-ship`). Map each journal entry to its commit from the log.

Done when every section is filled or removed, every row in `What changed`
has all of What, Why, and How, the rationale journal keeps the dead ends,
and every claim traces to a journal entry, a commit, or a run.

## 4. Open it

Show the user the title, the diagram, and the body. On their yes: push the
branch and run
`gh pr create --base <default> --head <branch> --title <title> --body-file <file>`
(or `glab mr create`; add `--draft` or reviewers per the working agreement or
the profile). To refresh the body of an existing PR after more work or a
review round, regenerate it and `gh pr edit <n> --body-file <file>`.

Report the PR URL. The caller (`pair-ship`, `tdd`, `light`) records it where
its own state lives.

## Rules

- **The journal is the source.** If the PR needs a reason the journal lacks,
  add the journal entry first, then the PR line.
- **Every concern gets What, Why, and How.** A row without a Why is a
  question for the user, not a blank.
- **Keep the dead ends.** They answer "why didn't you just...".
- **A diagram unless there is nothing to draw**, and then say so.
- **Opening a PR needs a yes in chat**, each time.
- **No em dashes** in the body.
