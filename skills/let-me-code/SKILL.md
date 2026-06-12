---
name: let-me-code
description: Generate a TDD-structured tutorial markdown file that guides the user to type each line of code themselves for learning and muscle memory. Use when the user wants to learn by doing, says "teach me", "I want to code it myself", "walk me through step by step", "don't write the code for me", or asks for a hands-on coding tutorial. The tutorial follows red-green-refactor cycles where each step is a complete, typeable unit.
---

# Let Me Code

## Philosophy

**Core principle**: You do not write the implementation. You write *instructions for a human to write the implementation.* The tutorial is the artifact; the code the user types is theirs.

Learning happens when the learner's hands are on the keyboard. This skill turns a feature request into a guided exercise: the agent understands the problem, designs the TDD plan, and produces a step-by-step tutorial where every code block is meant to be typed — not pasted — by the user.

The tutorial follows TDD discipline exactly. Each step is one RED→GREEN cycle. The learner types a failing test, runs it, watches it fail, types the minimal implementation, runs it again, watches it pass. Understanding accumulates from the act of doing.

See [tutorial-format.md](tutorial-format.md) for examples of well-formed vs poorly-formed steps, and [step-anatomy.md](step-anatomy.md) for the anatomy of each step section.

## Critical Difference from TDD

| Phase | TDD | let-me-code |
|---|---|---|
| Planning | Explore, list behaviors, get approval | Same + determine teaching order |
| Tracer bullet | Agent writes test + impl | Agent designs Step 1 of tutorial |
| Incremental loop | Agent writes code | Agent writes RED+GREEN tutorial steps |
| Refactor | Agent modifies source files | Agent writes refactor section in tutorial |
| Final output | Working code in project | `TUTORIAL.md` only; zero source files |

In the `tdd` skill, the agent writes code.

In `let-me-code`, the agent **never writes code into the project**. Instead, it writes a `TUTORIAL.md` file (or `docs/tutorials/<feature-name>.md`) that contains all the code the user will type themselves.

The agent's outputs are:
1. A planning conversation (same as TDD planning phase)
2. A single markdown tutorial file

Nothing else. No source files. No test files. Only the tutorial.

## Anti-Pattern: Pasting Instead of Typing

The tutorial must be designed for typing, not copy-pasting. This means:

- Each code block is **complete and self-contained** — the user types the whole thing, not a diff
- Code blocks are **short enough to type in one sitting** — 5–30 lines per block is ideal
- Each block has **precise placement**: which file, which class, which position
- The explanation tells the user **what to expect as they type** so the act of typing is also the act of understanding

A tutorial where code blocks are 200-line dumps encourages copy-paste behavior. Break long blocks into sub-steps.

## Workflow

### 1. Planning

Before writing the tutorial, understand the problem deeply. Use the project's domain glossary, check for ADRs, explore existing interfaces.

- [ ] Ask: "What feature or concept do you want to learn to implement?"
- [ ] Confirm the language, test framework, and project structure
- [ ] Confirm which behaviors to cover (prioritize — you can't teach everything)
- [ ] Identify opportunities for [deep modules](deep-modules.md)
- [ ] Design interfaces for [testability](interface-design.md)
- [ ] List the behaviors in teaching order (simplest first, then incremental)
- [ ] Get user approval: "Here are the steps I'll teach. Does this order make sense for how you want to learn?"

Ask: "What should the public interface look like? Which behaviors are most important for you to understand deeply?"

The teaching order matters: start with the tracer bullet that proves the system works end-to-end, then add complexity.

### 2. Tutorial Tracer Bullet (Step 1 of the file)

Design the first tutorial step as a tracer bullet: one test that proves the simplest observable behavior works. This becomes Step 1 in the tutorial.

The tracer bullet step has:
- The failing test to type (RED)
- What error the user should see when they run it
- The minimal implementation to type (GREEN)
- What passing output looks like

This is the most important step to get right. It sets the pace and confidence for everything that follows.

### 3. Incremental Tutorial Steps

For each remaining behavior, design one tutorial step. Each step is one RED→GREEN cycle.

Step design rules:
- Each step builds on all previous steps (no step is standalone after step 1)
- Each test is typed in full — never partial
- Each implementation is minimal for *this* step's test — nothing extra
- Code blocks are sized for typing (target 10–20 lines, max 30)
- Explanation precedes each code block

See [tutorial-format.md](tutorial-format.md) for the exact section structure of each step.

### 4. Tutorial Refactor Step

After all RED→GREEN steps, add a final "Refactor" section. This section does not introduce new tests. Instead, it:
- Explains what to look for using [refactoring.md](refactoring.md) candidates
- Shows the before and after of one or two targeted refactors visible in code the learner typed
- Includes "Understanding check" questions about why the refactor is an improvement

### 5. Write the Tutorial File

Produce a single markdown file. Default path is `TUTORIAL.md` in the project root. If the project has a `docs/` directory, use `docs/tutorials/<kebab-case-feature-name>.md`.

The file must include:
- Title, date, and a one-paragraph "what you'll build" summary
- A prerequisites section
- Numbered steps following the format in [tutorial-format.md](tutorial-format.md)
- A "what's next" section suggesting follow-on exercises

After writing the file, tell the user:
> "Your tutorial is at `<path>`. Open it, follow the steps in order, and type every line yourself. Don't copy-paste — the point is the muscle memory. Come back when you're done if you want to explore the refactor phase or extend it further."

## Checklist Per Step

```
[ ] Step title names the behavior being learned
[ ] Explanation says WHY this test, not just what it does
[ ] RED block is the complete test — no partials
[ ] Expected failure output is shown
[ ] GREEN block is minimal implementation only
[ ] Expected pass output is shown
[ ] Code block is ≤30 lines (break into sub-steps if longer)
[ ] "Understanding check" after any complex logic
```
