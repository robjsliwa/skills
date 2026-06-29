# Refactoring in Tutorials

## Purpose

The refactor section is the capstone of the tutorial. At this point all tests pass. The learner has typed every line and has a working implementation. The refactor section teaches them to see the code with fresh eyes and improve it without breaking behavior.

The key teaching: tests protect the refactor. The learner should run tests after every change in this section and trust them as a safety net.

## What to cover

After the TDD cycle, look for these candidates and pick 1–2 that are most visible in the code the learner just typed:

- **Duplication** — identical logic in two places. Show before/after an extracted function.
- **Long methods** — a method doing too much. Show how to split into private helpers while keeping tests on the public interface.
- **Shallow modules** — a class that just passes through to another. Show how to combine or deepen.
- **Feature envy** — logic living in the wrong class. Show a move.
- **Primitive obsession** — a string or int where a value object would clarify intent.

Choose candidates that are *visible in what the learner typed* in this tutorial. Don't invent abstract refactors. Point at specific lines.

## Format for refactor steps

Each refactor in the tutorial follows this pattern:

```
### Refactor: <name>

**What to look for**: <one sentence describing the smell>

**Before** (in `<filename>`, around line <N>):

```<language>
<the current code>
```

**Type this instead**:

```<language>
<the refactored version>
```

Run tests to confirm nothing broke:

```bash
<test command>
```

**Understanding check**

> <question probing why this is better>
```

## What not to include

- Do not introduce new behaviors in the refactor section
- Do not add tests in the refactor section (all tests were written RED→GREEN)
- Do not refactor things the tutorial didn't cover — stay in scope

## Tone

Refactoring is presented as *noticing* and *responding*, not as a checklist to execute. The framing should be: "Now that the code works, let's step back and look at it. What do you notice? Here's something I see..."
