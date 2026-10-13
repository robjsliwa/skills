---
name: review-change
description: >-
  Review a change against a fixed base on three separate axes, each in its
  own sub-agent: Standards (the repo's rules and a short smell baseline),
  Spec (does it do what the story, slice, or PR promised), and Decisions
  (ADRs, glossary, system boundary, stack). Presents the three reports side
  by side, unmerged. Use when a story or slice is ready to ship, when
  pair-ship or the full loop reaches review, or when the user says "review
  this," "review the branch," or "check this PR."
argument-hint: "Optional: the spec source (story file, slice file, or PR number) and the base. Both are inferred when omitted."
---

# Review Change

Three axes, each in its own sub-agent so one cannot mask another: code that
follows every rule can build the wrong thing, code that builds the right
thing can break the conventions, and either can quietly contradict a decision
the repo already made.

This skill reviews and reports. It does not fix, and it does not decide what
happens to a finding. The caller does that: `pair-ship` takes each finding to
a disposition with the user; elsewhere, show the reports and let the user
pick.

## 1. Pin the inputs

**The spec source**, the first that applies:

- A **story file** in the v2 format (the `story` skill's `FORMAT.md`): its
  `Scenario`, `Demo`, `Acceptance`, `Out of scope`, and `Verification`, plus
  the requirement ids it serves.
- A **pairing slice file** (`docs/pairing/slices/NNNN-*.md`): its header
  (`Scenario`, `Demo`, `Picture`), `Goal`, `Scope`, `Acceptance`, `Drift`,
  and the source section it cites.
- A **PR description**: `gh pr view <n> --json title,body` (or `glab`), and
  any issue it links.

If none is given, look for a story or slice whose branch matches the current
one; failing that, ask for one. A review with no spec runs Standards and
Decisions only, and says so in the report.

**The base**, a fixed point, never "whatever main is now":

- a slice's `base` field (recompute with `git merge-base <default> HEAD` if
  the branch was rebased since it was written),
- the commit the story's work started from, when the story or its PR records
  one,
- otherwise `git merge-base <default> HEAD`.

Then pin the diff: `git diff <base>...HEAD` (three dots) and
`git log <base>..HEAD --oneline`. Confirm the diff is non-empty before
spawning anything. Done when the spec source, the base sha, and a non-empty
diff are named.

## 2. The axes

**Standards.** Does the code follow this repo's rules? Sources: `CLAUDE.md`
or `AGENTS.md`, the pairing working agreement's `Coding style`, `Testing`, and
`Hard rules` when one exists, and every config the tools read. Skip what a
linter or formatter already enforces. Then apply the smell baseline below as
judgement calls; a documented repo rule overrides any of them.

**Spec.** Does the code do what the spec source promised? Report what is
missing or partial, what was built that was not asked for (scope creep), and
what looks implemented but wrong. For a **story**, check every `Acceptance`
line against the diff, then run the story's `Verification` commands and
confirm the `Demo` actually works as written: a demo that cannot be performed
is a finding even when the tests pass. For a **slice**, run each acceptance
line's `Check`. A recorded `Drift` entry, or a story's `Out of scope` item,
is not a finding.

**Decisions.** Does the code respect what the repo has decided? Sources:
every ADR the spec lists plus any other ADR under `docs/adr/` the diff
touches; `GLOSSARY.md`; `CONTEXT.md`; and the stack, from `CLAUDE.md` or the
pairing working agreement's `Stack` and `Layout`. Report:

- contradictions of an ADR,
- new identifiers or terms that conflict with `GLOSSARY.md` or use one of its
  `_Avoid_` words,
- a new actor or external system the change talks to that `CONTEXT.md` does
  not show inside or across its boundary,
- new dependencies outside the stack, and layering violations,
- choices made in this diff that clear the ADR bar (hard to reverse,
  surprising without context, a real trade-off) but have no ADR.

## 3. Smell baseline

Judgement calls, not violations. Name the smell, the hunk, and the cheaper
shape. Report one only when it makes this change harder to read or change.

1. **Long function.** It does several things you could name separately.
2. **Large class or module.** Many reasons to change live in one place.
3. **Long parameter list.** Several arguments always travel together; they
   want to be one type.
4. **Duplicated logic.** The same rule written twice, so the copies will
   drift.
5. **Feature envy.** A function reads another type's data more than its own;
   it probably belongs there.
6. **Primitive obsession.** A domain idea (money, an id, a status) passed as
   a bare string or number, with its rules scattered.
7. **Shotgun surgery.** One small idea needed edits in many unrelated files.
8. **Speculative generality.** Hooks, flags, or abstractions that nothing in
   this change uses.
9. **Misleading name.** A name that says something other than what the code
   does, or a word the glossary would not use.

## 4. Run it

Spawn three sub-agents **in one message** so they run in parallel. Each
prompt carries: the base sha and the diff and log commands, the source files
for its axis (paste any rule text it cannot read itself; the Standards prompt
includes the smell baseline above), and this brief:

> Report findings for your axis only. For each: file and hunk, the rule or
> spec line or ADR it concerns (quoted), and whether it is a hard violation
> or a judgement call. Number them S1.., P1.., D1.. for Standards, Spec,
> Decisions. Under 400 words. Say "no findings" if there are none.

The Spec sub-agent may run the story's `Verification` and the acceptance
checks; the other two only read.

**No sub-agent tool?** Run the three axes one after another yourself. Before
each, re-read the diff and that axis's sources from disk as if for the first
time, and do not carry findings from one axis into the next. Say in the
report that the axes ran sequentially in one context, so they are less
independent than usual.

## 5. Presenting

Show the three reports under `## Standards`, `## Spec`, and `## Decisions`,
lightly cleaned, never merged or reranked. Head them with one line naming
the spec source and the base sha. End with one line: findings per axis and
the worst finding within each axis.

## Rules

- **A fixed base.** Every axis reviews the same `<base>...HEAD`.
- **One axis per reviewer.** Independence is the point; never merge the
  reports into one ranked list.
- **Evidence over opinion.** Every finding quotes the rule, spec line, or ADR
  it rests on, or says it is a smell from the baseline.
- **Report, don't fix.** Dispositions belong to the caller and the user.
