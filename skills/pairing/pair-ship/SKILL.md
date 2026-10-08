---
name: pair-ship
description: >-
  Ship the active slice: verify acceptance and the full check, update from
  main, open a PR whose body carries the rationale journal and a what, why,
  and how of every change, run a three-axis review (standards, spec,
  decisions), address findings, close out the memory bank, merge on an
  explicit yes, and wrap up. Resumable at any stage. Use when the slice's
  plan is done, or the user runs /pair-ship.
argument-hint: "Nothing. The stage is read from the slice and the PR."
---

# Pair Ship

Every change reaches `main` the same way: slice branch, PR, review, merge. The
PR is the permanent record of the pairing, so its body is built from the
slice's journal: why this piece exists, what changed and why, the path we took
including the dead ends, the decisions, and the evidence. A reviewer who was
not in the room should be able to agree or disagree with every choice.

Call the Skill tool with `pairing` and read its MEMORY-BANK.md. The PR body
template is [assets/pr-template.md](assets/pr-template.md); the review is
[REVIEW.md](REVIEW.md).

`WORKING-AGREEMENT.md` decides the PR mode (GitHub, GitLab, or local), draft
or ready, the merge strategy, whether reviews are posted, and who merges. In
GitLab mode use the `glab` equivalents of each `gh` command. In local mode
there is no remote: the PR body is the file `slices/NNNN-<slug>.pr.md`, the
review is journaled, and the merge is `git merge --no-ff` with the body as the
message. In the stage table below, local mode reads "PR open" as: the
`.pr.md` file exists and the branch is not merged; "PR merged" as:
`git branch --merged <default>` lists the branch.

After any rebase onto the default branch, push with
`git push --force-with-lease`, to the slice branch only.

## Which stage

Read the slice, `STATE.md`, and (when the slice has a `pr`) `gh pr view`.
Start at the first stage that is not done; each stage is safe to re-enter.

| State | Start at |
|---|---|
| No PR, plan steps open | Stop. Back to `pairing`; name what is open |
| No PR, plan done | 1. Preflight |
| PR open, no review round journaled | 4. Review |
| PR open, findings without dispositions, unresolved human threads, or the default branch moved | 5. Address |
| PR open, every finding settled, close-out commit not yet made | 6. Close out and merge |
| PR open, close-out commit made (`Phase: merging`) | 6, from step 2 (checks, then ask) |
| PR merged | 7. Wrap |

## 1. Preflight

1. Run every acceptance check in the slice and tick each one that passes,
   with its evidence noted. A check that fails sends the work back to the
   `pairing` loop. Set the slice and `STATE.md` to `shipping` and commit,
   e.g. `chore(pairing): acceptance verified`, so the tree is clean for the
   update in step 3.
2. Run the agreement's full check (tests, lint, format, typecheck).
3. Update from the default branch per the agreement (`git fetch`, then rebase
   or merge), set `base` to the new merge base, and run the full check
   again. Resolve conflicts as a pairing step, journaled.
4. Sweep: no `[DEBUG-` tags, no stray files, every `Parked` item copied to
   `ROADMAP.md` as a `later` row, glossary and ADR changes on this branch.
5. If the agreement squashes, leave `wip` commits; otherwise offer to tidy
   them with the user before pushing.

Done when the full check is green at HEAD on top of the current default
branch, and every acceptance box is ticked.

## 2. Write the PR body

Build it from [assets/pr-template.md](assets/pr-template.md), using the
journal, the ADRs, and `git diff <default>...HEAD`. The journal is the
source, not the chat. Write it to a scratch file outside the repo (e.g. under
`$TMPDIR`), or to `slices/NNNN-<slug>.pr.md` in local mode. Done when every
template section is filled or removed, and every claim in it traces to a
journal entry, a commit, or a run.

## 3. Open the PR

Show the user the title and body. On their yes: push the branch, then
`gh pr create --base <default> --head <branch> --title <title> --body-file <file>`
(add `--draft` if the agreement says so, and `--reviewer` for listed humans).
Record the PR number in the slice's `pr` and in `STATE.md` (`Phase:
in-review`), commit that as `chore(pairing): record PR #N`, and push. Done
when the PR exists and the memory bank points at it.

## 4. Review

Follow [REVIEW.md](REVIEW.md): standards, spec, and decisions, as parallel
sub-agents against `<base>...HEAD`. Present the three reports side by side,
unmerged. If the agreement says to post reviews, post the combined report with
`gh pr comment <n> --body-file <file>`. Done when the reports are in front of
the user.

## 5. Address

Gather the findings: the agent review's, plus every unresolved human review
thread, which `gh pr view` cannot tell apart from resolved ones. Query them:

```
gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){pullRequest(number:$n){reviewThreads(first:100){nodes{isResolved path line comments(first:20){nodes{author{login} body}}}}}}}' -F o=<owner> -F r=<repo> -F n=<n>
```

If the default branch moved since preflight, updating from it is the first
finding: rerun preflight step 3.

Take each finding one at a time. The user picks a disposition:

- **Fix now**: run it through the `pairing` step loop (propose, build, prove,
  journal, commit), and push.
- **Defer**: a `later` row in `ROADMAP.md`, linked from the PR.
- **Dismiss**: one line of reason.

Journal one `Review round N` entry listing every finding and its disposition.
Then regenerate the PR body so its journal and review sections include the
round, and update it with `gh pr edit <n> --body-file <file>`. If waiting on a
human reviewer, run `pair-checkpoint` and stop; `/pair` resumes here later.
Done when every finding has a disposition and every fix is pushed.

## 6. Close out and merge

1. **Close-out commit**, so `main` receives the finished memory bank with the
   merge: slice `status: merging` with its `pr`, roadmap row `merging` with
   the PR number, `STATE.md` with `Phase: merging`, and `Next step` naming
   the next roadmap piece if one is agreed. Commit as
   `chore(pairing): close slice NNNN` and push. `merging` stays honest if the
   merge is delayed; once the PR shows merged, every skill reads it as
   shipped, and the next `pair-slice` records it as `merged`. If fixes land
   after this commit, keep it; the state is still true.
2. Wait for checks: `gh pr checks <n> --watch` when CI exists.
3. **Ask, explicitly**: "Merge #N into main with <strategy>?" Merge only on a
   clear yes in chat, and only if the agreement lets the agent merge;
   otherwise hand the user the command.
4. `gh pr merge <n> --delete-branch` with `--squash`, `--merge`, or
   `--rebase` for the agreement's squash, merge commit, or rebase. For
   squash or merge, add `--subject "<PR title> (#<n>)"` so the commit on
   `main` points at the PR, whose body keeps the full rationale.

Done when the PR shows merged.

## 7. Wrap

`git checkout <default> && git pull --ff-only`, delete the local branch if it
remains, and confirm `STATE.md` on the default branch shows `Phase: merging`
for this slice. If the close-out commit was missed, nothing breaks: the next
`pair-slice` reconciles the memory bank from the PR state in its first commit.
Never commit to `main`. Tell the user in two lines: what merged, and the
next piece from `ROADMAP.md`, with `/clear` then `/pair-slice` (or `/pair`).

## Rules

- **The journal is the source of the PR body.** If the PR needs a reason the
  journal lacks, add the journal entry first, then the PR line.
- **Every claim has evidence**: a run, a commit, or a link.
- **Merging and opening PRs need a yes in chat.** Each time, not once per
  session.
- **Never commit to the default branch**, and never force-push it.
- **Review findings are dispositioned, not argued.** Fix, defer, or dismiss
  with a reason; the user decides.
