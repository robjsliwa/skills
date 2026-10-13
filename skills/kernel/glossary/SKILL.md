---
name: glossary
description: >-
  Own the repo's language and its record of context and decisions: GLOSSARY.md
  (settled terms, definitions, words to avoid), CONTEXT.md (system context as a
  C4 level 1 picture, actors, what is outside the boundary, why the system
  exists), and ADRs under docs/adr. Use when a term is settled or contested in
  conversation, when actors or the system boundary change, when a decision is
  hard to reverse, or when any skill needs to write one of these files. Also
  user-invocable: "add this to the glossary," "write an ADR," "redraw
  CONTEXT.md."
argument-hint: "Optional: 'term <word>', 'context', or 'adr <title>'."
---

# Glossary

Three files hold what every skill needs to stay consistent: the words, the
boundary, and the decisions. This skill owns their formats and the rules for
changing them. Other skills write through it: `interview` settles terms and
offers ADRs, `repo-setup` migrates v1 files, `solution-design` records
decisions.

| File | Holds | Format |
|---|---|---|
| `GLOSSARY.md` (repo root) | the ubiquitous language | [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md) |
| `CONTEXT.md` (repo root) | system context: C4 level 1, actors, boundary, why | [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md) |
| `docs/adr/NNNN-slug.md` | decisions worth explaining later | [ADR-FORMAT.md](ADR-FORMAT.md) |

The ADR folder comes from `docs/agents/profile.md` (`Docs / ADRs`), default
`docs/adr`.

## GLOSSARY.md: when to update

- **Add** a term when the user has settled it: they agreed to the word, the
  definition, and the words to avoid. Never from your own guess.
- **Revise** in place when understanding changes. No stale entries, no
  "formerly" notes; git has the history.
- **Remove** a term the system no longer has.
- Add terms a user would say, plus the few technical terms the team uses
  constantly. Not every class name.

## How to challenge a term

Language goes fuzzy one word at a time. Stop it at the word.

1. **Spot it.** Two words for one thing ("client" and "customer"), one word for
   two things ("order" for both a cart and a purchase), a word that conflicts
   with `GLOSSARY.md`, or an implementation word where a user's word belongs.
2. **Check the glossary.** If the term is defined, quote the definition back.
3. **Name the conflict in one line** and recommend a resolution: pick the
   canonical word, push the other to `_Avoid_`, or split one word into two terms.
4. **Ask once, settle, write.** In an interview this is a normal question turn.
   Outside one, ask in a single line and carry on.

Once settled, the canonical term is the one used everywhere: prose, story
titles, code names where practical, and diagrams.

## Diagram labels are glossary terms

Every node label in a Mermaid diagram anywhere on the docs spine (CONTEXT.md,
requirements, design, stories, ADRs, PR bodies) uses glossary terms. If a
diagram needs a word the glossary does not have, that is a term to settle, not a
label to invent. External system names (Stripe, GitHub) are proper nouns and
are exempt.

## CONTEXT.md: when to update

- Create it when the first align session settles actors and boundary, or when
  `repo-setup` migrates a v1 glossary-style `CONTEXT.md`. Ask before creating.
- Update it when an actor, an external system, or the boundary changes, or when
  a key constraint is added or lifted.
- Never put term definitions here. Link to `GLOSSARY.md` instead.

Draw the picture through `visualize`, in its C4 style (see the worked example in
[CONTEXT-FORMAT.md](CONTEXT-FORMAT.md)), and validate it when the profile has
diagram validation on.

## ADRs: when to write one

Only when the decision clears all three of the bar:

1. **Hard to reverse.** Undoing it costs real rework or a migration.
2. **Surprising without context.** A newcomer would ask "why on earth did they
   do it this way?"
3. **A real tradeoff.** There was a credible alternative that lost for reasons.

Offer it, do not just write it; most sessions produce zero or one. Never edit an
accepted ADR's decision: write a new one that supersedes it and mark the old one
`Superseded by NNNN`. Fixing a typo or a broken link is fine.

## Migrating a v1 CONTEXT.md

v1 used `CONTEXT.md` as the glossary. When `repo-setup` hands over the split:

1. Parse each term and definition into `GLOSSARY.md`'s format. Merge with an
   existing `GLOSSARY.md`; list conflicting definitions and settle each with the
   user before writing.
2. Propose actors and external systems from the old file and the code.
3. Draw the C4 level 1 sketch and run a "show, then ask" turn (`interview`) to
   correct it.
4. Rewrite `CONTEXT.md` in [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md).

## Conventions

- Prose, short, no em dashes.
- Relative links between the three files.
- Do not commit. Show the diff.
