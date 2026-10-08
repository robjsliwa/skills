# PR body template

Built from the slice's journal, its ADRs, and the diff. Brief prose, no
preamble, the glossary's domain language throughout. Remove a section that
has nothing to say rather than writing "n/a". The `Summary` visual follows
Matt Pocock's `pr` skill: pick the smallest picture that makes the point
(pseudocode, call tree, file tree, Mermaid, or a diff-sketch).

Title: `<type>(<scope>): <what this slice makes true>` per the agreement's
commit convention, e.g. `feat(invoice): totals in cents with half-even rounding`.

```markdown
## Why

<One to three sentences: the piece of the spec this serves, the problem it
solves, in the user's words where possible.>

Slice: `docs/pairing/slices/0003-invoice-totals.md` · Source: S1 §3.2

## Summary

<the smallest visual that shows the shape of the change>

## What changed

Grouped by concern, not by file. One row per concern.

| Concern | What | Why | How |
|---|---|---|---|
| Totals | `Invoice.Total()` returns integer cents | the spec's example only matches exact arithmetic | sums sub-cent amounts, rounds once (`invoice/total.go`) |
| Validation | negative quantities rejected | S1 §3.2 rule 4 | `NewLine` returns `ErrNegativeQuantity` (`invoice/line.go`) |

## Rationale journal

The path we took, condensed from the slice journal, oldest first. Keep the
dead ends: they answer "why didn't you just...". Mode shows who wrote it.

1. **Line total as integer cents** (driver). Chose cents over float64 to make
   rounding explicit. 3f2a91c
2. **Rounding per line, abandoned** (navigator). Drifted a cent on the spec's
   example; moved rounding to the invoice total. See ADR 0004. 7b10e2d
3. **Debug: flaky table test.** Map iteration order; hypothesis held on the
   first try; sorted the fixture keys. 91ac4f0
4. **Review round 1.** D1 fixed (renamed `Amount` to `Subtotal` per the
   glossary); S2 deferred to the roadmap.

Full journal: the slice file above.

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

The agreement's PR footer, if it names one, goes after the last section.
