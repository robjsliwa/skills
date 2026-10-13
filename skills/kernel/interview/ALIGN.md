# Align playbook

Align is the interview that comes first. It ends when you and the user could
each describe the change, who it is for, what is out, and the words for it, and
the descriptions would match. It is relentless: one question at a time, every
fuzzy word stopped and settled the moment it appears.

## The tree

Walk these in order. Skip what step 0 already settled, and say you skipped it.

1. **Intent.** What problem, for whom, and why now. Recommend a one-sentence
   statement of the change and ask the user to correct it.
2. **Users and actors.** Who uses it, who is affected, which outside systems it
   talks to. This is where the first "show, then ask" usually goes: a C4 level 1
   sketch (person, system, external) drawn through `visualize`.
3. **Scope.** What is in, what is explicitly out, what is deferred. Recommend the
   smallest scope that still serves the intent.
4. **Language.** The nouns and verbs this change lives in. Runs through every
   other branch, not only here (see below).
5. **Success.** What a person will see when it works. This seeds the Demo line
   of the first story.
6. **Constraints.** Deadlines, platforms, compliance, existing systems that must
   not change.

Structural branches (2, sometimes 3 and 5) get a "show, then ask" turn. Every
align session has at least one.

## Challenge every term

The glossary is the language of the system. Align is where it gets made.

- **The moment a fuzzy or new term appears**, in the user's words or yours,
  stop and settle it before the branch continues. Fuzzy means: two words for
  one thing, one word for two things, a word that conflicts with
  `GLOSSARY.md`, or a word from the implementation where a user's word belongs
  ("record," "entity," "job," "item").
- **Check `GLOSSARY.md` first.** If the term is there, use its definition and
  say so. If the user is using it differently, name the conflict: "GLOSSARY.md
  says an *order* is a confirmed purchase; you just used it for a cart. Which
  do you mean?" Recommend one.
- **If it is new**, propose the term, a one-sentence definition, and the words
  to avoid. That is one question turn like any other.
- **Write it as it settles** via `glossary` (format in
  the `glossary` skill's `GLOSSARY-FORMAT.md`). Settled means the user agreed.
  Never write a term the user has not confirmed.
- **Use the settled word from then on**, including in your diagrams' node
  labels. If you slip, correct yourself.

## Offer ADRs

When a decision clears the bar in the `glossary` skill's `ADR-FORMAT.md` (hard
to reverse, surprising without context, a real tradeoff), offer to record it:
"This clears the ADR bar; want me to write 0004-tenants-are-workspaces?" Write
it via `glossary` on a yes. Most align sessions produce zero or one ADR.

## CONTEXT.md

If the actors or boundary changed, or `CONTEXT.md` does not exist yet, update it
via `glossary` (format in the `glossary` skill's `CONTEXT-FORMAT.md`) using the
C4 level 1 picture the user just corrected. Ask before creating it the first
time.

## Output

No findings document unless the user asks. The output is:

- the shared understanding, recapped in the conversation in five to ten lines
  (intent, users, scope in and out, success, constraints);
- the `GLOSSARY.md` entries written during the session;
- any ADRs and `CONTEXT.md` changes.

When a mode called align, hand the recap back to it. The full loop passes it to
`write-requirements`; the light loop passes it to `story`.
