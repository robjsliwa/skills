---
name: pair-setup
description: >-
  First-time setup for pair programming in a repo: interview the user one
  decision at a time on tech stack, layout, coding style, testing, git flow,
  PR policy, and pairing preferences, then write the working agreement, the
  memory bank skeleton, the CLAUDE.md pointer, and ADRs for lock-in choices.
  Use once per repo before the first slice, when the user says "set up
  pairing," "decide the stack," "how should we work," or when pair finds no
  working agreement.
argument-hint: "Optional: the spec or idea file, so stack questions are grounded in the product."
---

# Pair Setup

Pairing works when both people already agree how the repo works: what the
stack is, how to run the tests, how code should look, how a change reaches
`main`. This skill settles those once and writes them into
`docs/pairing/WORKING-AGREEMENT.md`, which every later pair-* skill reads
first and obeys.

Call the Skill tool with `pairing` and read its MEMORY-BANK.md for the files
this skill creates. The agreement's template is
[assets/working-agreement-template.md](assets/working-agreement-template.md).

## 1. Explore before asking

Read whatever exists; every answer found here is a question not asked.

- The spec or idea the user pointed at, in full. It is the root of the stack
  decisions.
- The repo: languages and manifests (`go.mod`, `package.json`,
  `pyproject.toml`, `Cargo.toml`), build files (`Makefile`, `justfile`), lint
  and format configs, test layout, CI under `.github/workflows/` or
  `.gitlab-ci.yml`, `CLAUDE.md` or `AGENTS.md`, `GLOSSARY.md` or
  `CONTEXT.md`, `docs/adr/`, and `docs/agents/` from
  `setup-matt-pocock-skills`.
- Git and hosting: `git rev-parse --is-inside-work-tree`, `git log -1`,
  `git remote -v`, the default branch, `gh auth status` (or `glab auth
  status`), and on GitHub
  `gh repo view --json defaultBranchRef,squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed,deleteBranchOnMerge`.

Classify the repo: **greenfield** (no code yet), **brownfield** (code with
conventions to infer), or **partial**. Done when you can list what the repo
already settles and what is still open.

## 2. Interview

Run the `design-interview` contract (call that skill if installed): one
decision per turn, a recommendation with its trade-off every time, the soft
spot named, dependency order. In a brownfield repo, most turns become
confirmations: "the code uses X; keep it?" Skip any branch the repo or the
spec already settles, and say you skipped it.

Lay out the tree first, then walk it in this order:

1. **Product shape**: what runs where (CLI, service, library, web app), from
   the spec. Everything below inherits from it.
2. **Language and runtime**, with versions.
3. **Framework and key libraries**, and the dependency policy (stdlib first,
   or a short closed list).
4. **Persistence and external services**, if the product has any.
5. **Layout**: the top-level directories and the one rule that keeps them
   apart.
6. **Testing**: framework, where tests live, the seams worth testing, the TDD
   stance, the fast command and the full command.
7. **Coding style**: formatter and linter, plus the few rules no tool
   enforces (error handling, naming, comments, file size).
8. **Git flow**: default branch, branch naming, commit convention, who
   commits (agent or user), commit cadence, whether checkpoints push, merge
   strategy, deleting branches after merge, CI gate.
9. **PR and review**: PR or local-merge mode (local when there is no remote),
   draft or ready on open, the agent's review axes, whether review findings
   are posted as a PR comment, human reviewers, who may merge.
10. **Pairing preferences**: default mode (driver, navigator, ping-pong,
    dictation), step size, how much explanation, checkpoint cadence, and any
    hard rules ("never touch the migrations folder").

Recommend from the spec and the user's stated habits; if they keep a
boilerplate skill such as `go-boilerplate`, recommend its stack and note that
the scaffold itself becomes slice 0001. Done when every branch is settled or
explicitly deferred, and the user agrees the interview is over.

## 3. Draft and confirm

Show the user, before writing anything:

- the filled working agreement,
- the `## Pairing` block for `CLAUDE.md` (below),
- the list of ADRs you propose: one per choice that clears the bar (hard to
  reverse, surprising without context, a real trade-off). Usually the
  language, the persistence, and any deliberate deviation. Not the formatter.

Let them edit. Done when they approve.

## 4. Write, on a branch

Everything reaches `main` through a PR, including this.

1. If the repo has no commits, ask before creating an initial commit on the
   default branch with only `.gitignore` and a one-line `README.md`. If there
   is no repo, ask before `git init`.
2. Create the branch `chore/0000-pairing-setup` (or the agreement's naming).
3. Write `docs/pairing/WORKING-AGREEMENT.md`, the ADRs in
   `docs/adr/NNNN-<slug>.md` (domain-modeling format, numbered after any that
   exist), and `docs/pairing/ROADMAP.md` with the spec as source S1 (copy it
   to `docs/pairing/sources/` if it lives outside the repo or was pasted).
   Setup is itself slice 0000, so `pair-ship` can carry it like any other:
   write `docs/pairing/slices/0000-pairing-setup.md` per MEMORY-BANK.md with
   goal "agree how this repo is built," acceptance "A1. The user approved the
   working agreement in chat. Check: done during setup" (ticked), a plan of
   two ticked steps (interview, write), and a `Decision: Working agreement`
   journal entry listing every settled decision with its one-line reason and
   every deferred one. Write `docs/pairing/STATE.md` with slice 0000 active,
   `Phase: building`, and `Next step: /pair-ship the setup`.
4. Seed `GLOSSARY.md` only with terms the interview actually settled.
5. Add or update the `## Pairing` block in whichever of `CLAUDE.md` or
   `AGENTS.md` exists (ask which to create if neither). Update an existing
   block in place; leave every other section alone.
6. Commit with the agreement's convention, e.g.
   `chore(pairing): working agreement and memory bank`.

The `CLAUDE.md` block:

```markdown
## Pairing

This repo is built by pair programming with an agent. Before any change, read
`docs/pairing/WORKING-AGREEMENT.md` (it outranks defaults) and
`docs/pairing/STATE.md`. Run `/pair` to resume.

- Stack: <one line>. Fast tests: `<cmd>`. Full check: `<cmd>`.
- Every change: slice branch, small green commits with a journal, PR whose
  body carries the rationale journal, review, merge. Never commit to `main`.
- Domain language: `GLOSSARY.md`. Decisions: `docs/adr/`.
```

Done when the branch has one commit containing all of the above and the tree
is clean.

## 5. Ship it and hand off

Tell the user setup is on its branch, and offer `/pair-ship` to open and merge
the setup PR (slice 0000), so the first real slice starts from a `main` that
has the agreement. Then name the first piece: for greenfield work, slice 0001 is a
walking skeleton (the stack scaffolded, one end-to-end path, CI green), via
`pair-slice`.

## Rules

- **One decision per turn**, always with a recommendation.
- **Infer, then confirm** in a brownfield repo. Do not ask what the code
  already answers.
- **The agreement is a contract, not an essay.** Rules and commands only; the
  reasons go in ADRs.
- **No scaffolding here.** Code arrives through slices, starting with 0001.
- **Re-running is an edit.** If an agreement exists, show what would change
  and update it in place on a new `chore/` branch.
