---
name: review-change
description: >-
  Review a change against a fixed base on up to four separate axes, each in
  its own sub-agent: Standards (the repo's rules, REVIEW.md, and a short smell
  baseline), Spec (does it do what the story, slice, or PR promised),
  Decisions (ADRs, glossary, system boundary, stack), and Security. The depth
  (quick, standard, deep) follows the risk of what the change touches. Fresh
  verifiers then vote on every finding, and survivors are tagged Important,
  Nit, or Pre-existing. Presents the reports side by side, unmerged. Use when
  a story or slice is ready to ship, when pair-ship or the full loop reaches
  review, or when the user says "review this," "review the branch," "deep
  review this," or "check this PR."
argument-hint: "Optional: the spec source (story file, slice file, or PR number), the base, and a depth. All are inferred when omitted. A re-review also takes the last reviewed sha and the findings already reported, with their dispositions."
---

# Review Change

Four axes, each in its own sub-agent so one cannot mask another: code that
follows every rule can build the wrong thing, code that builds the right
thing can break the conventions, either can quietly contradict a decision the
repo already made, and all of them can be exploitable.

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

**Review rules.** `REVIEW.md` at the repo root, plus any in a directory the
diff touches, if they exist. Every reviewer and verifier gets them: they say
what failure looks like here, which paths to skip, and how many nits to allow.

**A re-review**, when the caller passes the last reviewed sha and the findings
already reported:

- Review `git diff <last-reviewed>..HEAD` only. If that sha is no longer an
  ancestor of HEAD (the branch was rebased), review `<base>...HEAD` instead
  and say so.
- Every prompt carries the earlier findings with this instruction: never
  report one again, whatever its disposition. Report a finding on older code
  only when this diff makes it worse.
- Spec still checks the whole change, because a fix can break an acceptance
  line it never touched.
- Run Spec, plus each axis with a finding that was fixed since the last
  review. An axis with nothing fixed sits out, and the report says so. At Deep,
  every axis runs.

**The depth.** Review effort follows risk. The first that applies wins:

1. A depth the user or caller named.
2. The profile's `Review / Depth`, unless it is `auto`, which is the default.
3. **Deep**, if a changed path matches `## Always deep` in `REVIEW.md`, or looks
   like auth, sessions, tokens, secrets, crypto, payments, billing, migrations
   or schemas, a public API definition, CI workflows, or infrastructure. A prose
   file does not count by name alone, so `docs/auth.md` is not Deep unless
   `REVIEW.md` lists it.
4. **Quick**, if every changed file is prose (docs, comments, changelog), or
   the change is under 30 changed lines by `git diff --numstat`, adds no file,
   and touches no dependency manifest.
5. **Standard**, for everything else, and whenever you are unsure.

| Depth | Reviewers | Verifiers |
|---|---|---|
| Quick | Spec, plus Security if any code changed | 1 |
| Standard | All four | 2, plus a third on a split vote |
| Deep | All four | 3 |

With no spec source, Quick runs Standards in Spec's place. Work out the depth
from the whole change on every round: it can rise and never falls, so a fix
that reaches a sensitive path turns the review Deep. Done when the depth and
the reason for it are named.

## 2. The axes

**Standards.** Does the code follow this repo's rules? Sources: `CLAUDE.md`
or `AGENTS.md`, the pairing working agreement's `Coding style`, `Testing`, and
`Hard rules` when one exists, the rules in `REVIEW.md`, and every config the
tools read. Skip what a linter or formatter already enforces. Then apply the
smell baseline below as judgement calls; a documented repo rule overrides any
of them.

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

**Security.** Can this change be abused? The profile's `Review / Security`
value picks the source; [SECURITY.md](SECURITY.md) says how to run each one
and holds the built-in brief. Every source ends in the same findings, so the
rest of this skill does not care which one ran. Name the source in the report.

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

Spawn the depth's sub-agents **in one message** so they run in parallel. Each
prompt carries: the base sha and the diff and log commands, the source files for its
axis (paste any rule text it cannot read itself; the Standards prompt includes
the smell baseline above), the review rules, and this brief:

> Report findings for your axis only. For each: file and line, the rule or
> spec line or ADR it concerns (quoted), and whether it is a hard violation
> or a judgement call. If it is one instance of a class of bug, name the class
> and list every instance in the change, so the author fixes them all at once.
> Number them S1.., P1.., D1.., X1.. for Standards, Spec, Decisions, Security.
> Under 400 words. Say "no findings" if there are none.

The Spec sub-agent may run the story's `Verification` and the acceptance
checks; the others only read, apart from a scanner the profile names.

**No sub-agent tool?** Run the axes one after another yourself. Before
each, re-read the diff and that axis's sources from disk as if for the first
time, and do not carry findings from one axis into the next. Say in the
report that the axes ran sequentially in one context, so they are less
independent than usual.

## 5. Verify

A reviewer that has to find something will. Before anyone sees a finding,
other agents try to disprove it. Skip this step if no axis found anything.

The number of verifiers comes from the depth, not from the number of findings.
None has seen another's work or a reviewer's reasoning beyond the findings.
Each gets the diff commands, the review rules, and its findings, with this
brief:

> For each finding, read the code it cites and try to disprove it. Reply with
> the finding's number and one verdict: `real` (you confirmed it in the code;
> cite the file and line) or `false` (one line on why it does not hold). A
> finding that rests on a guess from a name, or that you cannot confirm, is
> `false`. Judge the claim, not its importance.

How the votes count:

- **Quick:** one verifier. `real` keeps the finding; `false` drops it.
- **Standard:** two verifiers in one message. Two matching verdicts settle a
  finding, because a third vote could not change the result. Only if they split
  does a third verifier run, on the split findings alone, and the majority
  stands.
- **Deep:** three verifiers in one message. A finding is dropped only if all
  three say `false`, since here a missed bug costs more than a false alarm.

Spec findings from a command that really failed, and scanner hits, are verified
the same way: a test failure stands if it reproduces, a scanner hit stands if
the code is reachable as the scanner claims.

**No sub-agent tool?** Re-read each finding's code from disk and argue against
it once, keep what survives, and say the findings were not independently
verified.

## 6. Tag

Tag each survivor with exactly one:

- **Pre-existing**: the bug is in lines this change did not write. Check with
  `git blame -s <base>..HEAD -L <line>,<line> -- <file>`: a commit id starting
  with `^` means the line predates the change. It is not the author's fault
  and does not hold up this change.
- **Important**: it would make the change wrong, unsafe, or break a rule or
  decision the repo holds. Hard violations land here, and every Security
  finding that is not Pre-existing.
- **Nit**: a judgement call or a smell worth knowing about and safe to skip.
  Honour any nit cap in `REVIEW.md`, keeping the ones that matter most.

A Spec finding about something missing has no line to blame; tag it Important
or Nit.

## 7. Presenting

Show the reports under `## Standards`, `## Spec`, `## Decisions`, and
`## Security`, lightly cleaned, never merged or ranked across axes. Within an
axis, list Important first, then Nit, then Pre-existing. An axis that did not
run gets one line saying why, so nobody reads its silence as a pass. Head the
reports with one line naming the spec source, the base sha, the head sha
reviewed (what a later re-review starts from), and the depth with its reason.
Under each axis, one line on what the verifiers dropped: how many, and the
reason for each, so a wrong drop can be caught.

End with a count, then the worst finding within each axis; with nothing to
fix, say that plainly. If any Security finding is Important, add: **not ready
to merge**. If the same class of finding has now come up in earlier rounds, or
a rule keeps being applied by hand, name it as a candidate for `REVIEW.md`,
`CLAUDE.md`, or a lint rule.

## Rules

- **A fixed base.** Every axis reviews the same diff.
- **Effort follows risk.** When the depth is in doubt, go up, not down.
- **One axis per reviewer.** Independence is the point; never merge the
  reports into one ranked list.
- **Evidence over opinion.** Every finding cites a file and line and quotes
  the rule, spec line, or ADR it rests on, or says it is a smell from the
  baseline.
- **Nothing reaches the user unverified**, and nothing is dropped silently.
- **Never report a finding twice.** A re-review reports only what is new.
- **Report, don't fix.** Dispositions belong to the caller and the user.
