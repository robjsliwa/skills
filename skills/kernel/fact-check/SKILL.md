---
name: fact-check
description: >-
  Make a teaching page or document tell the truth: inventory every claim it
  will make (code, numbers, quotes, citations, behaviour, dates), verify each
  one the way its kind demands (run the code, recompute the number, match the
  quote against the source, resolve the link), record the result in a claims
  ledger, and assemble the page from a template whose code and numbers are
  filled in from what was verified, so the prose cannot disagree with it. Works
  for any subject. Use when a teaching skill (professor, teach-me, code-along)
  writes a lecture or lab, when any skill writes a page that quotes numbers or
  code, or when the user says "check every claim," "verify this," "is all of
  this actually true."
argument-hint: "The draft or plan to check, and where the build folder should go."
---

# Fact-check

Nothing a learner reads should rest on the writer's memory. A model's recall
of an API, a statute, a date, or a constant is a guess until it is checked,
and a guess presented in a lecture becomes the learner's belief. This skill
turns "I'm fairly sure" into a ledger of claims, each with the evidence that
settled it, and builds the page so that the evidence, not the draft, supplies
the code and the numbers.

`<skill-dir>` is the folder this `SKILL.md` was loaded from.

- [LEDGER-FORMAT.md](LEDGER-FORMAT.md): the claims ledger and the values
  script.
- `scripts/assemble.py`: fills a template from verified values and code, and
  refuses to write the page if anything is unresolved or unverified.

## The build folder

Beside the page it serves, e.g. `lessons/0002-one-phone/build/`:

```
build/
  claims.json      the ledger: every claim, its kind, source, status, evidence
  values.py        computes every number the page quotes; writes values.json
  values.json
  ref/             verified code: the reference solution, run and tested here,
                   never in the learner's own project
  run/             saved outputs: test runs, command transcripts, compiler errors
  lab.tpl.html     the page as a template with {{slots}}
  shots/           screenshots for review
```

## Steps

1. **Inventory.** Read the plan or draft and list every claim it will make in
   `claims.json`, one per row, before checking any of them. A claim is
   anything a learner could get wrong by believing it: a code line, an output,
   an error message, a number, a quotation, a date, a "the spec says," a "this
   always happens." Done when no sentence of the plan states a fact that has
   no row.

2. **Verify each claim by its kind** (LEDGER-FORMAT.md has the table). Code
   runs in `build/ref/`, with its real toolchain, and its output is saved to
   `build/run/`. Numbers are computed by `values.py`, never typed. Quotes are
   matched against the source fetched now, in the edition `RESOURCES.md`
   names. Citations are opened, not remembered. Behaviour ("the compiler
   rejects this") is shown by doing it and saving the output. Work in the
   background with the `research` skill for anything that needs reading. Done
   when every row is `verified`, `failed`, or `unverifiable`.

3. **Act on failures.** A `failed` claim is good news found early: change the
   plan, not the evidence. Sometimes the failure is the lesson (the dial pad's
   key-ten surprise came from running the parser one key at a time); hand that
   back to the caller as a candidate challenge. An `unverifiable` claim either
   leaves the page or is said to the reader as uncertain ("I could not find a
   primary source for this"), with a `note`.

4. **Template.** Write the page with slots instead of facts:
   `{{value:tenth_hint}}` for a number or string from `values.json`,
   `{{snip:phone_stored}}` for code between `snip:phone_stored` and
   `end:phone_stored` marker comments in `build/ref/`, `{{file:Phone.swift}}`
   for a complete file, `{{include:fig-1.svg.html}}` for a generated figure.
   Done when the template quotes no number of three or more digits and no code
   line by hand.

5. **Assemble.**

   ```bash
   python3 <skill-dir>/scripts/assemble.py build/lab.tpl.html lab.html \
     --values build/values.json --claims build/claims.json --src build/ref --strict-numbers
   ```

   It refuses to write while a slot is unresolved, a claim is `pending` or
   `failed`, a relative link is broken, or a tag is unbalanced, and with
   `--strict-numbers` while the prose quotes a number the values script did
   not produce. Done when it prints `wrote`.

6. **Hand back** the page, the count of claims by status, and any failure
   that changed the plan.

## Rules

- **Inventory before verifying.** Checking as you go misses the claims you
  were sure of; those are the dangerous ones.
- **Primary sources.** A claim is verified against the thing itself or its
  owner (RESOURCES.md's tiers). A blog post can point to the source; it cannot
  be the source.
- **The evidence fills the page.** Code and numbers flow from `build/` into
  the page through slots. Retyping a value "because it's the same" is how
  pages drift.
- **The learner's project is not the lab bench.** Reference code runs in
  `build/ref/`. The learner's own directory is theirs (the workspace's
  `NOTES.md` hard rules decide who touches it).
- **Date the ledger.** APIs, prices, and rules change; each row says when it
  was checked.
- **Say what you could not check.** An honest "unverified" beats a confident
  error.
