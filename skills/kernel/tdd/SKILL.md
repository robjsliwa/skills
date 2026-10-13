---
name: tdd
description: >-
  Build one story test-first: work its tasks T1..Tn in order, each by
  red-green-refactor at the seams its TDD plan names, one behaviour at a time,
  tick each task when its tests and Verify pass, then run the story's
  Verification, perform the Demo for real, and mark the story done. Use when the
  user says "build this story," "build story 01-02," "tdd this," "make it pass,"
  or when a mode hands over a ready story to build. Also works for a plain
  feature with no story: plan the behaviours first, then the same loop.
argument-hint: "A story file path or issue id. Nothing, to pick the next ready story."
---

# TDD

Build one story so that every line of production code exists because a failing
test asked for it, and the story ends with a person seeing the Demo work. The
story says what to build and in what order; this skill is the discipline for
building it.

## Inputs

Read before writing any code:

- **The story.** Format in the `story` skill's `FORMAT.md`: Scenario, Demo,
  Picture, Acceptance, Tasks (each with Design, TDD plan, Verify), Verification.
  If no story was named, take the first `ready` story whose blockers are done.
- **`CLAUDE.md`** (or `AGENTS.md`): the agent contract, stack, and conventions.
- **`GLOSSARY.md`**: names in tests and code use its terms.
- **`docs/agents/profile.md`**: `Fast tests`, `Full check`, `Run the app`, and
  the tracker. If missing, find the commands from the manifest, use them, and
  say once that `/repo-setup` would record them.
- **The code at the seams** the tasks name. Read the real interfaces before
  writing a test against them.

Set the story's **Status** to `in-progress` (and move the tracker label per the
profile). Status values: `ready` → `in-progress` → `done`.

## The loop

Work tasks in order, T1 first. Within a task, follow its TDD plan test by test:

1. **Red.** Write the next test from the plan, one behaviour, at the seam the
   plan names. Run the fast tests. Watch it fail, and read the failure: it must
   fail for the reason the test is about (an assertion, a missing behaviour),
   not a typo, an import error, or a test that cannot compile because nothing
   exists yet. If it fails for the wrong reason, fix the test until the red is
   real. If it passes, the behaviour already exists or the test is wrong; find
   out which before going on.
2. **Green.** Write the least code that makes it pass. Hard-coding is allowed
   when the next test will force the generalisation. Run the fast tests. All
   green, not only the new one.
3. **Refactor**, while green. Remove duplication, improve names toward the
   glossary, deepen the module. Run the tests after each change. Never refactor
   on red.
4. **Next test.** Back to red with the next behaviour in the plan.

**Vertical within a task.** One behaviour at a time, all the way to green,
before the next test. Never write all the tests first and then all the code:
the second test you write should be shaped by what the first one taught you.

**The plan is a plan.** If a test in the plan turns out redundant, skip it and
say why. If a behaviour the plan missed shows up, add a test for it in the same
loop and note it in the task.

### Finishing a task

When the task's tests are green, run its **Verify** commands and compare the
output with what Verify expects. Both pass: tick the task's checkbox in the
`## Tasks` list. Then the next task.

If Verify fails while the tests pass, the tests missed something. Write the test
that catches it, then fix.

## Finishing the story

After the last task:

1. **Verification.** Run every command in the story's `## Verification`,
   including the full check from the profile. All green.
2. **Perform the Demo.** Actually do what the Demo line says: start the app with
   the profile's `Run the app` command, open the page or call the CLI, do the
   thing, and see the result. Report what you saw, with the output or a
   screenshot where the tooling allows. If the Demo cannot be performed from
   here (needs a phone, a human sign-in), say exactly which step the user must
   do and what they should see.
3. **Acceptance.** Tick each acceptance line you observed in the Demo or
   Verification. Leave unticked any you could not observe, and say why.
4. **Status.** Set `**Status:** done` in the story file. With a tracker, close
   the issue or move it to the done label using the profile's Notes recipe.
5. **Suggest `review-change`** on the story's branch, with the story file as the
   spec source. Do not commit or open a PR unless the user asks.

## When the code disagrees with the story

The code is ground truth. If the real interface, schema, or behaviour differs
from the task's Design (a type already exists with another name, an adapter
works differently), build against the code, then add a section at the end of
the story:

```markdown
## As built
- T2: `ShelfRepository.find` already returns `Option<Shelf>`; used it instead of
  the `findShelf` port in the design.
```

If the disagreement changes what the user will see (the Demo, an acceptance
line), stop and ask before going on.

## v1 stories

A v1 story has no `## Tasks` and one design section plus a TDD plan. Treat the
whole story as one task, T1: its TDD plan is the plan, its verification is
Verify. Do not rewrite the story into v2 format; tick its acceptance lines and
set its status as above.

## No story at all

When the user asks to build a feature directly, plan before code: list the
behaviours in order, name the seam for each, write the plan as a short
`Subject_Condition_Outcome` list, and get the user's nod. Then the same loop.
If it grows past a handful of behaviours or the user cannot see the result,
suggest writing a story first via `story`.

## Good tests

Detail and examples: [TESTS.md](TESTS.md). In short:

- **Behaviour through public interfaces, at seams.** Test what the code does
  for its caller, through the port, handler, or module boundary the plan names.
  Never reach into private state or assert on internals.
- **One assertion idea per test.** Several asserts are fine if they check one
  idea. Two ideas are two tests.
- **Names:** `Subject_Condition_Outcome`, e.g.
  `Cart_AddingSameItemTwice_IncrementsQuantity`. Adapt the casing to the
  language's test conventions, keep the three parts.
- **Fakes at ports, no mocking what you own.** Replace the outside world (a
  clock, a payment API, the database behind a port) with an in-memory fake that
  honours the port. Do not mock your own classes to test other classes of
  yours; use the real ones.
- **Fast and deterministic.** No sleeps, no network, no shared state between
  tests. Inject time and randomness.

## Hard bugs

If a test goes red for a reason you cannot explain within a couple of tries, or
something unrelated breaks and the cause is not obvious, stop guessing. Hand
over to `diagnose` with the failing test as the reproduction, then come back to
the loop once it is understood.

## Conventions

- Run the fast tests after every red and every green. Paste the relevant lines
  of real output; never claim a result you did not run.
- Small steps. If green takes more than a few minutes of code, the test was too
  big; back out and write a smaller one.
- Keep the story file current as you go: ticked tasks, `As built` notes. It is
  how the next session (or the user) knows where things stand.
- No em dashes in anything you write into the story.
