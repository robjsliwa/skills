# Story file template

Every story file uses this exact 7-section structure. Section headings are H2 (`##`) so the file's H1 is the story title.

The story file path is `phase-NN-<phase-slug>/story-NN-MM-<story-slug>.md` and the H1 is `# Story NN-MM — <Title>`.

```markdown
# Story NN-MM — <Title>

## Narrative

A short (1–4 paragraph) explanation of *why* this story exists and how
it fits the proposal. Reference proposal sections by name or number
where it sharpens the connection ("§4.2 of the proposal defines
GearSpec; this story implements a slimmed version"). Set scope
expectations early: what's *in* this story, what's deferred, what's
being deliberately kept simple.

This is the place to be opinionated — say what tradeoff you're making
and why.

## Pre-requisites

- Story NN-MM (or "Phase X complete") for each thing this depends on.
- External prerequisites if any (e.g. "Postgres 15+ running locally").

## Description

The substance of what to build. This section is allowed to be long.
Use subsections (### headings) liberally. Include:

- Interface / port / type definitions in fenced ```go``` blocks (or
  the appropriate language).
- SQL schema in fenced ```sql``` blocks.
- YAML / JSON samples in fenced blocks.
- Concrete file paths: `internal/core/ports/foo.go`,
  `cmd/<tool>/cmd/foo.go`.
- HTTP route shapes including request/response JSON.
- CLI command shapes including flags and output examples.

Be specific about file paths. The agent will create files at those
exact paths.

If there are decisions the agent needs to make, name them and pick a
default. Don't punt with "you might want to consider".

## TDD plan

A numbered list of tests, written RED-first. Each test gets a
descriptive `Test_Subject_Condition_Outcome`-style name and a one-line
explanation of what it asserts.

1. **TestName_Condition_ExpectedOutcome** — what it asserts.
2. **TestName_OtherCondition_OtherOutcome** — what it asserts.
3. ...

Tests are ordered the way the agent should write them: the simplest
first (often a parser or pure function), the most integrated last
(often an end-to-end HTTP test).

Mention specific testing libraries / patterns when they matter:
- "Use testcontainers-go for the DB tests."
- "Use a fake HTTP client; no live network in unit tests."
- "Race detector clean: `go test -race ./...`."

If there are tricky concurrency tests or things that need care, call
them out under the relevant numbered item.

## Implementation hints

Short, specific notes that save the agent time. Examples:

- "Don't use `fmt.Print` from inside a tea model — return strings from
  `View()`."
- "Memoise custom React Flow node components or canvas perf will tank."
- "The `app.tenant_id` setting must be set inside the transaction, not
  on the connection."

Three to ten bullets is typical. If you don't have specific hints,
omit the section rather than padding it.

## Acceptance criteria

Checkboxes the human reviewer (and the agent) can tick off:

- [ ] Concrete deliverable 1 (e.g. "All N tests above pass").
- [ ] Concrete deliverable 2 (e.g. "Migration applies cleanly on a
      fresh database").
- [ ] `go test -race ./...` is green.
- [ ] No regressions in the suite from the previous story.

Each criterion must be objectively verifiable. "Code is well-designed"
is not a criterion. "All exported functions have doc comments" is.

## README updates

What to add to the phase README and/or top-level README when this
story lands. Examples:

> Add to top-level README under "CLI": a subsection for the new
> command with the synopsis, flags, and a one-paragraph example.

> Add a "Broker" section to the top-level README explaining that MVP
> uses in-process channels and post-MVP swaps in NATS.

This forces the documentation to stay current with the code.

## Verification

Concrete shell commands the agent (and the human) can run to confirm
the story is done. Include the expected output in comments or code
fences.

```bash
make test
go test ./internal/core/services/foo/... -race -count=1

# End-to-end smoke
./bin/<tool> command-under-test
# Expect: ...
```

If verification is "follow the steps in story NN-MM-end-to-end-smoke",
say so explicitly and link.
```

## Section ordering rationale

The order is intentional and shouldn't be reshuffled:

1. **Narrative** orients the reader and connects to the proposal.
2. **Pre-requisites** prevent the reader from starting too early.
3. **Description** is the bulk of the story. By this point the reader knows why and what comes before.
4. **TDD plan** comes before implementation hints because tests are written first.
5. **Implementation hints** come after the test plan because they often refer to test setup ("the test from #3 needs...").
6. **Acceptance criteria** are derived from the description + TDD plan, so they come after both.
7. **README updates** force a doc step that's easy to forget.
8. **Verification** closes with the "how do I know I'm done" check.

## Common pitfalls

- **Skipping "Pre-requisites".** Even if it's obvious, write at least one line. The agent uses this to know whether the prior state is in place.
- **Fluffy acceptance criteria.** "Code is clean and well-tested" is not actionable. Replace with specific bullets.
- **Verification that's just "tests pass".** Include at least one *manual* verification step that produces visible output (a curl, a CLI invocation). It catches integration bugs that unit tests miss.
- **Implementation hints that are really requirements.** If something must be done a certain way, put it in Description, not Hints. Hints are the things the agent could figure out but shouldn't have to.
- **Tests numbered in random order.** Order them the way the agent should write them. The agent will work top-down through the list.
