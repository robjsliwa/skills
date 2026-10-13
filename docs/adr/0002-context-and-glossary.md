# 2. CONTEXT.md is system context; GLOSSARY.md is language

**Status:** accepted
**Date:** 2026-10-13

## Context

v1's planning loop wrote the domain glossary to `CONTEXT.md`; the pairing loop wrote `GLOSSARY.md`. Two names for one thing, and no home for the system's context picture.

## Decision

`GLOSSARY.md` holds terms, definitions, and words to avoid. `CONTEXT.md` holds the C4 level 1 picture, the actors, what sits outside the boundary, and why the system exists. Both live at the repo root and every mode reads both.

## Consequences

`repo-setup` offers to move terms out of a v1 `CONTEXT.md` into `GLOSSARY.md` and redraw `CONTEXT.md` as system context.
