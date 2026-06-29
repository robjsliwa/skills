# Phase README template

Every phase folder has a `README.md` that introduces the phase. It's read by both the human reviewer and any agent picking up the phase fresh.

```markdown
# Phase NN — <Phase title>

## What this phase delivers

A 1–3 paragraph description of the user-visible (or developer-visible)
capability that exists at the end of this phase. This should be
concrete and demonstrable.

For Phase 0 (bootstrap), this can be "the project compiles, the
schema applies cleanly, CI is green" — there's no end-user behavior
yet, but there's a verifiable state.

For later phases, name the capability: "By the end of Phase 3, a
workload runs. The user can execute `hello.yaml` and watch its
single step succeed."

Conclude this section with a 3–6 bullet list of what the phase
introduces (the major artifacts, not every file):

- The X interface and a small starter Y.
- An in-memory Z adapter — same shape as the future production
  adapter but lives in-process.
- The W service that orchestrates A and B.
- An `execute` CLI verb and the corresponding HTTP route.
- A streaming endpoint for events.

## Why this ordering

A short paragraph or bullet list explaining why the stories are in
this specific order. The point is to defend choices that aren't
obvious — if story NN-03 has to come after NN-02 because it consumes
NN-02's output, say so. If two stories could swap order but you've
chosen one ordering for a reason, say why.

This section helps a reviewer either accept the ordering or push
back constructively.

## Stories

| ID    | Title                                                  |
|-------|--------------------------------------------------------|
| NN-01 | First story title                                       |
| NN-02 | Second story title                                      |
| NN-03 | Third story title                                       |

## Exit criteria

A list of objective checks for "the phase is done":

- [ ] Story-level acceptance criteria all met.
- [ ] One or two phase-level integration checks (an end-to-end script
      that uses multiple stories together).
- [ ] Any cross-story invariants hold (e.g. "every public CLI command
      respects the `--output text|json|id` convention").

## Out of scope (deferred)

A short list of related items deliberately *not* in this phase. Each
should name where it does land (later phase, post-MVP, or
"not in MVP"). This is the place to head off "why isn't X in this
phase?" questions.

- X — post-MVP per proposal §N.
- Y — phase NN+1.
- Z — not in MVP; the proposal flags it as a Phase 4 item.
```

## Why this exact structure

- **What this phase delivers** sets expectations. A reviewer reads this first to know if the phase is the right size.
- **Why this ordering** answers the most common reviewer question.
- **Stories** is the table of contents.
- **Exit criteria** lets a phase be "checked off" cleanly.
- **Out of scope** prevents the agent from over-building. Without this section, agents tend to do "while I'm in there..." work that bloats the PR.

## Length target

40–90 lines. Phase READMEs that grow past 100 lines are usually trying to do work that belongs in a story file or in CLAUDE.md.
