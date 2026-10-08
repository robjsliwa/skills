# Review

Three axes, each in its own sub-agent so one cannot mask another: code that
follows every rule can build the wrong thing, code that builds the right thing
can break the conventions, and either can quietly contradict a decision the
repo already made.

## Pin the diff

`git diff <base>...HEAD` (three dots, against the merge base) and
`git log <base>..HEAD --oneline`, where `base` is the slice's `base`, or the
merge base with the default branch if the slice was rebased. Confirm the diff
is non-empty before spawning anything.

## The axes

**Standards.** Does the code follow this repo's rules? Sources: the
agreement's `Coding style`, `Testing`, and `Hard rules`, every config the
tools read, and `CLAUDE.md`. If Matt Pocock's `code-review` skill is
installed, its smell baseline applies as judgement calls, overridden by any
documented repo rule. Skip what a linter already enforces.

**Spec.** Does the code do what the slice promised? Sources: the slice's
`Goal`, `Scope`, and `Acceptance`, plus the source section it cites. Report
what is missing or partial, what was built that was not asked for (scope
creep), and what looks implemented but wrong. A recorded `Drift` entry is not
a finding.

**Decisions.** Does the code respect what the repo has decided? Sources:
every ADR in the slice's `adrs` plus any other ADR the diff touches, the
glossary, and the agreement's `Stack` and `Layout`. Report contradictions of
an ADR, new identifiers or terms that conflict with the glossary or use an
`_Avoid_` word, new dependencies outside the stack list, layering violations,
and choices made in this diff that clear the ADR bar but have no ADR.

## Running it

If `code-review` is installed, call it with the slice base as the fixed point
and the slice file as the spec; it runs Standards and Spec. Spawn the
Decisions sub-agent alongside it. Otherwise spawn all three sub-agents in one
message so they run in parallel.

Each sub-agent prompt carries: the diff and log commands, the source files for
its axis (paste any rule text it cannot read itself), and this brief:

> Report findings for your axis only. For each: file and hunk, the rule or
> spec line or ADR it concerns (quoted), and whether it is a hard violation
> or a judgement call. Number them S1.., P1.., D1.. for Standards, Spec,
> Decisions. Under 400 words. Say "no findings" if there are none.

## Presenting

Show the three reports under `## Standards`, `## Spec`, and `## Decisions`,
lightly cleaned, never merged or reranked. End with one line: findings per
axis and the worst finding within each axis.
