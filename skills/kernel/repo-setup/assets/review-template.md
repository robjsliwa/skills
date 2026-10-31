# Review rules

What a reviewer should care about here. `review-change` gives this file to
every reviewer and verifier. Keep it short, and when a review comment keeps
repeating, move it here. A check a linter can do belongs in the linter. Add a
`REVIEW.md` in a directory for rules that apply only there.

## What failure looks like here

<One line per part of the repo that fails its own way.>

- docs: it lies
- config: it misroutes
- `<path>`: <what going wrong means here>

## Always check

- <A rule the tools cannot enforce, e.g. every handler under `api/` checks the
  caller's tenant.>

## Do not flag

- <A pattern that looks wrong and is intended, and why.>

## Always deep

Paths that get the deepest review however small the change. `review-change`
already spots the obvious ones by name; list what a name would not give away.

- <e.g. `internal/ledger/`, `lib/permissions.rb`>

## Skip these paths

- <generated code, vendored code, lockfiles, fixtures>

## Reporting

- Nits: at most 3 per review.
- Cite a file and line as evidence, never a guess from a name.
- Start the summary with the count, and say plainly when there is nothing to
  fix.
