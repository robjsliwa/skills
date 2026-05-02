# Rationale Journal Workflow Template

Workflow text inserted into the generated `CLAUDE.md`. Replace placeholders
before writing:

- `{TEST_COMMAND}` = `make test`
- `{ARCHITECTURAL_LAYERS}` = bullet list of this project's layers
  (Domain Ports, Application Core, Authentication, Adapters, Application Entry,
  Configuration)
- `{TEST_APPROACH_GUIDANCE}` = "Table-driven tests with the standard
  `testing` package. Use `t.Run` subtests for cases. Auth middleware tests
  use `httptest` plus signed test tokens (HS256 with a known secret).
  Validation tests exercise the `decodeAndValidate` helper directly with
  string bodies. Integration tests for the store adapter use
  testcontainers-go behind the `integration` build tag."
- `{CROSS_CUTTING_SECTIONS}` = include API Contract Changes (always),
  Database / Migration Changes (if SQL DB), Policy / Authorization Changes
  (always — auth scopes evolve)

Everything between the ✂️ markers is the literal text to insert into
the generated `CLAUDE.md`.

---

## ✂️ INSERT INTO GENERATED CLAUDE.md BELOW THIS LINE ✂️

## Story Implementation Workflow

When asked to implement a story, follow this exact sequence:

### Step 1: Acknowledge the Story

Confirm which phase and story you're about to implement. Restate the
acceptance criteria.

### Step 2: Write Tests First (Red)

Before writing any production code, write the tests that encode this
story's acceptance criteria.

- Translate each acceptance criterion into one or more test cases
- Include at least one test for the primary success path and one for a
  meaningful failure or edge case
- Test at the layer boundary where the behavior is most visible — port
  contract for domain ports, handler for HTTP endpoints, service method
  for business logic, middleware for auth/validation rules
- Stubs and interfaces are fine

Run `{TEST_COMMAND}` and confirm the new tests **fail** for the right
reasons. If a test passes immediately, tighten the assertion.

### Step 3: Implement to Pass (Green)

Write the minimum production code needed to make all tests pass. Follow
the architecture and conventions in this CLAUDE.md and `docs/ARCHITECTURE.md`.
Implement ONLY the requested story.

Run `{TEST_COMMAND}` and confirm **all tests pass**.

If a story is too large to implement cleanly, propose a split. Don't
silently implement a partial version.

### Step 4: Refactor (Green stays green)

Improve structure without changing behavior. Run `{TEST_COMMAND}` after
refactoring. Skip if Green is already clean.

### Step 5: Update OpenAPI Spec (if HTTP changes)

If the story added or changed any HTTP handler, run `make swagger` to
regenerate the OpenAPI spec. Verify the resulting `docs/swagger.json` and
`docs/swagger.yaml` look correct (new endpoints, new fields, updated
descriptions). Commit the regenerated files alongside the code change.

### Step 6: Commit

Stage all changes and commit with a descriptive message referencing the
story.

### Important Rules

- NEVER implement more than one story at a time
- NEVER write production code before failing tests exist
- NEVER commit without regenerating the OpenAPI spec if handlers changed
  (CI will fail anyway, but catch it locally)
- Acceptance criteria ambiguous? Stop and ask

---

## Rationale Journal Template

Adapt depth to story complexity. Omit optional sections that don't apply.
Never omit Testing Strategy.

```markdown
# Phase {N}, Story {N}: {Story Title}

**Date:** {date}
**Status:** Implemented

## What This Story Accomplishes

One paragraph. What capability did we add and why?

## Architectural Rationale

Map each piece to the project's layers:

{ARCHITECTURAL_LAYERS}

Explain why each piece belongs in its layer.

## File-by-File Breakdown

For each file created or modified:

### `path/to/file.go`

- **Layer:** Which layer
- **What was added/changed:** Walkthrough of key types and functions
- **Why it's shaped this way:** Design decisions, rejected alternatives
- **How it connects:** Callers, callees, data flow

## Testing Strategy

{TEST_APPROACH_GUIDANCE}

### Tests Written

- **`path/to/file_test.go`** — Scenarios covered. Why these cases.
  What each test proves.

### Red Phase Insights

What did writing tests first reveal? Did the test-first approach surface
interface problems or AC gaps? If tests suggested a different shape than
planned, explain the pivot.

### Coverage Decisions

What was deliberately NOT tested in this story and why.

## Key Design Decisions

- **Decision:** What was decided
  - **Why:** The reasoning
  - **Alternative considered:** What else
  - **Tradeoff:** What we gave up

## API Contract Changes (if applicable)

- New or changed endpoints, request/response shapes
- Breaking vs. non-breaking
- Validation rules added (`validate:` tags)
- swag annotations added or modified
- Confirmation that `make swagger` was run and spec is committed

## Database & Migration Changes (if applicable)

- New tables, columns, indexes and why
- Migration files added (`migrations/NNN_*.sql`)
- Backwards compatibility implications

## Policy / Authorization Changes (if applicable)

- New scopes introduced (e.g., `widgets:write`)
- Endpoints newly protected or unprotected
- Skip-list changes to `AUTH_SKIP_PATHS`
- Required claims changes

## How to Read This Code

Numbered list of files in reading order. Start with tests — they are
the spec.

1. `path/to/file_test.go` — defines the contract
2. `path/to/file.go` — the implementation
3. `path/to/adapter.go` — the wiring

## Connection to Previous Stories

How does this build on earlier work? What does it set up for next?
```

## ✂️ STOP INSERTING HERE ✂️

---

## Skill author note

When the database choice is `none`, omit the "Database & Migration Changes"
section. When the choice is `mongodb`, replace it with:

```markdown
## Database / Index Changes (if applicable)

- New collections or indexes and why
- Schema changes to documents
- Backwards compatibility for existing documents
```

When `auth_enabled=false`, the "Policy / Authorization Changes" section
is omitted from the template (no auth means no auth changes to track).
