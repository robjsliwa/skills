# Lesson Format

A lesson is one markdown file the user keeps open beside their editor. It turns
one story into a sequence of small RED to GREEN cycles the user performs
themselves. It is read top to bottom once, while coding, so it leads with why,
shows the map, teaches only what is new, and then gets out of the way.

## Contents

- Template
- Modes
- Type this / paste freely
- Step anatomy
- Splitting into parts
- The "Before you debrief" section
- Checklist

## Template

````markdown
---
story: docs/planning/<slug>/stories/NN-MM-<story-slug>.md
lesson: NN-MM            # NN-MM-a for a part
base: <full commit SHA>
mode: type               # type | paste | attempt-first
status: open             # open → debriefed
reference: NN-MM-<slug>.ref.patch
estimate: 45 min
---

# Lesson NN-MM: <Story title>

## Why this slice

Two to four sentences: what becomes possible when this is done, in the user's
terms, and why it comes now (what earlier lessons set up, what later ones need
from this one). Name the requirement ids it serves. End with the one-line
demo: "When you're done, `<command>` prints `<output>`."

## Where it sits

A Mermaid diagram of the components this slice touches, drawn from the real
code. Mark what already exists and what this lesson adds (a `classDef new`
style, or `(new)` in the label). Then one short paragraph walking the diagram
in the order a request or call flows through it.

If the real code differs from the story's design, say so here in one or two
sentences: "The story sketches `TenantStore.Get`; lesson 01-01 landed it as
`TenantStore.Lookup` returning `(Tenant, bool)`, so this lesson uses that."

## New ideas

Only the ideas this lesson needs that the user has not already shown they
know. For each: a name, two to five sentences, a tiny example if it helps, a
link to a primary source (language docs, library docs, the ADR). If an idea
needs more than that, give the minimum and suggest `/teach-me <idea>`.

Omit the section when there is nothing new.

## Before you start

- The branch or commit you should be on (`base`), and the command that proves
  the suite is green right now.
- Files you will touch, in the order you will touch them.

## Step 1: <behaviour, in plain words>

(See Step anatomy.)

## Step N: ...

## Refactor (optional)

Only when the steps left something worth improving that is visible in code the
user just wrote. Before and after, why it is better, and one understanding
check. No new tests.

## Verify

The story's acceptance criteria as a checklist, each with its requirement id,
then the verification commands with their expected output:

- [ ] <criterion> (R3)

```bash
<test command>          # expect: ok ... (N tests)
<manual smoke>          # expect: ...
```

## Before you debrief

(See the section below.)
````

Keep every section the lesson needs and omit the ones it does not. An empty
heading is noise.

## Modes

The mode sets how much of the implementation the lesson shows up front. The
tests are always shown in full: the test is the specification, and the user
should never have to guess it.

| Mode | The test | The implementation | Understanding checks |
|---|---|---|---|
| `type` | shown | shown, meant to be typed | after every non-obvious step |
| `paste` | shown | shown, fine to paste | only at real design decisions |
| `attempt-first` | shown | a hint first, then the code folded in `<details>` | after every step, asked before the reveal |

In `attempt-first`, each GREEN block becomes:

````markdown
**Your turn.** Make the test pass. Hint: <one sentence pointing at the idea,
not the code>.

<details>
<summary>Reference implementation</summary>

```go
...
```

</details>
````

The user may switch modes mid-lesson; the lesson does not need rewriting for
that. The debrief records which mode was used.

## Type this / paste freely

Every code block carries one tag on the line above it:

- **`✍️ type this`**: the decision-rich core, where the understanding is: the
  domain logic, the port signature, the branch that handles the edge case,
  the test's assertion.
- **`📋 paste freely`**: code with little to learn by typing it: imports,
  fixtures and test data, generated code, struct literals with many fields,
  wiring that mirrors something the user has written before.

When in doubt, tag it `type this`. If more than half the lines in a lesson are
`paste freely`, the story is mostly wiring; say so in "Why this slice" so the
user can move through it quickly.

## Step anatomy

Each step is one RED to GREEN cycle for one behaviour.

````markdown
## Step 3: Rejects a token from another tenant

<Why this behaviour, and why now. One short paragraph. If the minimal
implementation will look incomplete, say so: "We won't handle expiry yet;
Step 5 does.">

**Predict.** <A question about what the test run will show before they write
the implementation. "What error do you expect, and from which line?">

✍️ type this · `internal/auth/token_test.go`, after `TestVerify_ValidToken`

```go
<the complete test, never a fragment>
```

Run it:

```bash
go test ./internal/auth -run TestVerify_ForeignTenant
```

Expected (RED):

```
<the real failure output captured in the worktree, trimmed to the lines that
matter>
```

✍️ type this · `internal/auth/token.go`, inside `Verify`, replacing the
`return claims, nil` line

```go
<the minimal implementation for this test only>
```

Expected (GREEN):

```
<the real passing output>
```

> **Check.** <One question the user can answer from what they just did.>
````

Rules for steps:

- **Placement is exact.** Name the file, the enclosing type or function, and
  the position ("after `__init__`", "replacing the `return` on line ~40").
  Say "create the file" when it does not exist. Never "add this somewhere".
- **Blocks are whole and short.** Five to thirty lines. A test is always
  complete. When a change is a small edit to existing code, show the whole
  function after the edit, not a diff; the user should be able to match it
  against their screen.
- **Expected output is real.** Captured in the worktree per VERIFY.md, trimmed
  but never paraphrased. The right failure proves the test tests the right
  thing.
- **GREEN is minimal.** Only what this step's test needs. Name what is
  deliberately left out and which step adds it.
- **Split a step** when its block would pass thirty lines, when it introduces
  two ideas, or when one test needs changes in two files. The first sub-step
  should produce a new, different failure; the second, the pass.
- **Understanding checks are questions, not answers.** Good: "Why does
  `Verify` take the tenant id as a parameter instead of reading it from the
  context?" Bad: "Did that make sense?"
- **Refer to the user's own earlier code by name.** "Call the `Lookup` you
  wrote in lesson 01-01" is what ties the lessons into one codebase the user
  knows.

## Splitting into parts

A lesson should take thirty to ninety minutes. When the story's TDD plan
needs more than eight steps, split the lesson into parts at a point where the
suite is green and something is demoable, usually where the story's
acceptance criteria fall into two groups.

- Write part a only. Its "Why this slice" names what part b will add.
- Each part has its own lesson file, reference patch, base SHA, and debrief.
- Part b is written after part a is debriefed, against the code part a left.
- The story stays `in-lesson` until the last part is debriefed as done.

## The "Before you debrief" section

The last section of every lesson. It prepares the user for the debrief and
gives them a moment of retrieval practice while the work is fresh.

````markdown
## Before you debrief

Answer these without scrolling up, then check.

1. <A question about the main idea of the lesson.>
2. <A question about a decision in the design: why this way and not another.>
3. <A question that transfers the idea: "If the token also carried a role,
   where would the check go?">

<details>
<summary>Answers</summary>

1. ...
2. ...
3. ...

</details>

Jot down, anywhere, anything you did differently from the lesson and why:
names you changed, a different approach, a test you added or skipped, a bug
you found. Then run `/code-along`.
````

## Checklist

```
[ ] Frontmatter has story, lesson, base, mode, status: open, reference
[ ] "Why this slice" names requirement ids and a one-line demo
[ ] The diagram is drawn from the real code and marks what is new
[ ] Every disagreement between the story and the real code is stated
[ ] "New ideas" skips everything the learning records say is known
[ ] Every block is tagged, placed exactly, and 30 lines or fewer
[ ] Every test is complete; every GREEN is minimal for its test
[ ] Every expected output was captured from a real run
[ ] Eight steps or fewer, otherwise split into parts
[ ] "Verify" lists every acceptance criterion with its requirement id
[ ] "Before you debrief" has three questions with folded answers
```
