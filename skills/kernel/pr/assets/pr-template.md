# PR body template

Built from the journal (a pairing slice's or a story's), the ADRs, and the
diff, by the `pr` skill. Brief prose, no preamble, the glossary's domain
language throughout. Remove a section that has nothing to say rather than
writing "n/a". The `Summary` visual is one Mermaid diagram of what the change
did, its type picked from the table in the `pr` skill (a sequence when the
interaction changed, before/after when the structure did, a state diagram
for a lifecycle, and so on), drawn per the `visualize` skill's notation and
validated before it goes in the body.

Title: `<type>(<scope>): <what this change makes true>` per the repo's
commit convention (the working agreement or `CLAUDE.md`), e.g. `feat(invoice): totals in cents with half-even rounding`.

```markdown
## Why

<One to three sentences: the piece of the spec this serves, the problem it
solves, in the user's words where possible.>

Slice: `docs/pairing/slices/0003-invoice-totals.md` · Source: S1 §3.2
<or> Story: `docs/planning/invoicing/stories/01-02-owner-sees-totals.md`

## Summary

<one Mermaid diagram of the type that fits the change, e.g. a
sequenceDiagram with the new hop in a `rect`, or before/after subgraphs,
then one caption sentence saying what changed. Or one line saying why there
is no diagram.>

## What changed

Grouped by concern, not by file. One row per concern.

| Concern | What | Why | How |
|---|---|---|---|
| Totals | `Invoice.Total()` returns integer cents | the spec's example only matches exact arithmetic | sums sub-cent amounts, rounds once (`invoice/total.go`) |
| Validation | negative quantities rejected | S1 §3.2 rule 4 | `NewLine` returns `ErrNegativeQuantity` (`invoice/line.go`) |

## Rationale journal

The path we took, condensed from the slice journal, oldest first. Keep the
dead ends: they answer "why didn't you just...". In pairing, the mode shows
who wrote it; in tdd, the entry names the task.

1. **Line total as integer cents** (driver). Chose cents over float64 to make
   rounding explicit. 3f2a91c
2. **Rounding per line, abandoned** (navigator). Drifted a cent on the spec's
   example; moved rounding to the invoice total. See ADR 0004. 7b10e2d
3. **Debug: flaky table test.** Map iteration order; hypothesis held on the
   first try; sorted the fixture keys. 91ac4f0
4. **Review round 1.** D1 fixed (renamed `Amount` to `Subtotal` per the
   glossary); S2 deferred to the roadmap.

Full journal: the slice or story file above.

## Decisions

- ADR 0004 (new): round half-even, once, at the invoice level.
- Glossary: added **Subtotal**; **Amount** is now an _Avoid_ word.
- Drift: S1 §3.2 says half-up; we chose half-even (ADR 0004). <Spec updated
  in this PR | not yet, tracked in ROADMAP>.

## Evidence

- [x] A1. Three-line invoice totals correctly: `go test ./invoice -run TestTotal` passes
- [x] A2. Halves round to even: table test, 6 cases
- Before: `TestTotal/halves` got 1001, want 1000. After: pass.
- Full check: `make check` green on <sha>.

## Review

| Finding | Axis | Disposition |
|---|---|---|
| D1 `Amount` conflicts with glossary | Decisions | fixed, 5d2e8aa |
| S2 `total.go` exceeds 60 lines | Standards | deferred, ROADMAP |
| P1 none | Spec | |

## Merge danger

**Door:** <one-way | two-way>. <What would be hard to undo, if anything:
migrations, public API, data written.>
**Blast radius:** <one word>. <Who or what notices if this is wrong.>

## Follow-ups

- <Parked and deferred items, each now a ROADMAP row.>
```

The working agreement's or profile's PR footer, if one is named, goes after the last section.
