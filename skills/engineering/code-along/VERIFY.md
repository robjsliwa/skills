# Verify the Reference

Every code block and every expected output in a lesson comes from a real run.
The reference solution is built step by step in a throwaway git worktree at
the lesson's base commit, so the user's working tree is never touched, and
then saved as a patch beside the lesson. A block the user pastes will compile;
a failure the lesson predicts is the failure they will see.

## 1. Create the worktree

From the repo root, with a clean tree (SKILL.md step 2 checked this):

```bash
repo=$(git rev-parse --show-toplevel)
base=$(git rev-parse HEAD)
wt=$(mktemp -d)/code-along-NN-MM
git worktree add --detach "$wt" "$base"
```

`--detach` means no branch is created, so nothing appears in the user's
`git branch` list.

### Untracked things the build needs

A worktree has only tracked files. If the build or tests need ignored
directories or files (`node_modules/`, `.venv/`, `.env`, generated code,
`vendor/` when ignored), then, in order of preference:

1. Run the project's own setup (`make deps`, `npm ci`, `uv sync`) in the
   worktree, if `CLAUDE.md` or the README names one and it is quick.
2. Symlink the directory from the repo (`ln -s "$repo/node_modules"
   "$wt/node_modules"`), for read-only dependencies.
3. Copy small config files such as `.env`, and never print their contents.

If tests need a service (a database, a container), start it the way
`CLAUDE.md` or the Makefile says. If you cannot, ask the user how they run it.

## 2. Confirm the baseline

Run the full test command in the worktree before changing anything. It must
pass. If it does not, stop: the user's base is red, and the lesson would teach
against a broken floor. Tell them what fails.

## 3. Build step by step

For each planned step, in order:

1. Write the step's test exactly as the lesson will show it.
2. Run the narrowest command that exercises it (the one the lesson will tell
   the user to run) and save the output: `... > "$wt/../step-N-red.txt" 2>&1`.
   Confirm it fails, **for the reason the step says**. A test that fails for
   the wrong reason (a typo, a missing import) is a bad step; fix the step.
   A test that passes before the implementation teaches nothing; rethink the
   step.
3. Write the minimal implementation.
4. Run the same command, save `step-N-green.txt`, confirm it passes. Then run
   the full suite to confirm nothing else broke.
5. Commit in the worktree: `git -C "$wt" add -A && git -C "$wt" commit -qm
   "step N"`. These commits live only in the detached worktree; nothing
   references them after it is removed, and git collects them later.

Per-step commits let you cut each block exactly: `git -C "$wt" show HEAD --
<file>` for what the step changed, or read the whole function from the file at
that commit when the lesson shows a full function after an edit.

For attempt-first mode nothing changes here; the implementation is still built
and verified, then folded behind `<details>` in the lesson.

## 4. Run the story's verification

After the last step, run every command in the story's `## Verification`
section in the worktree, including the manual smoke, and save the output for
the lesson's Verify section. Every acceptance criterion should now be
checkable. If one is not, the step plan is missing a step.

## 5. Save the reference patch

```bash
git -C "$wt" diff "$base" HEAD > "$repo/docs/planning/<slug>/lessons/NN-MM-<slug>.ref.patch"
```

This is a docs artifact, not source; writing it into the user's repo is
allowed. The debrief compares the user's work against it.

## 6. Clean output for the lesson

Before pasting captured output into the lesson:

- Replace the worktree path with the repo-relative path.
- Drop timing noise (`0.012s`) or replace it with `…`, and drop random ids.
- Trim to the lines that matter: the test name, the assertion or compiler
  message, the summary line. Keep enough that the user can match it against
  their screen.

Never paraphrase an error message. If the real one is ugly, show it and
explain it.

## 7. Remove the worktree

```bash
git worktree remove --force "$wt"
git worktree prune
```

Always remove it, including when a step failed and you are rethinking the
plan; create a fresh one to start over.

## When something cannot be run

If a step cannot be executed here (it needs hardware, credentials, a paid
API), build and verify everything else, and at that step in the lesson write
plainly: "I could not run this step; the expected output below is what the
library documents, not a captured run." Link the documentation. Never present
an unrun output as a captured one.
