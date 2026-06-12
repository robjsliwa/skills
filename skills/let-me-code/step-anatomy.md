# Step Anatomy Decisions

## When to split a step into sub-steps

Split when the code block exceeds 30 lines, or when the RED→GREEN cycle involves two distinct concepts that each deserve explanation.

Signs you need to split:
- "Type this, then also type this other thing"
- The expected failure changes partway through
- Two files need to change to make one test pass

When you split, make the first sub-step produce a *new* compile/parse error, and the second sub-step produce the passing test. Each sub-step has its own expected output.

## When to add an "Understanding check"

Add after:
- Any design decision that isn't obvious (why a value object, why dependency injection)
- Any language feature the learner might not know (closures, generics, decorators)
- Any moment where the minimal implementation looks wrong but is correct ("why don't we validate here?")

Understanding checks are questions, not answers. The learner should be able to answer them after typing and running the step. They may look up the answer or reason from what they just did.

Good understanding check:
> Why did the test use `checkout(cart, payment)` instead of `cart.checkout(payment)`?
> What would the test look like if we had chosen the other design?

Bad understanding check:
> Did you understand this step? (y/n)

## How to write the RED block

The RED block contains *only* the test. Never include implementation code in the RED block even as a comment. The learner should run the tests and see them fail before typing anything else.

The expected failure output should be as exact as the framework allows. This matters because:
- Seeing the *right* failure message proves the test is testing the right thing
- An unexpected failure message tells the learner something went wrong

Common failure types to show explicitly:
- `NameError` / `cannot find symbol` — the class/function doesn't exist yet
- `AssertionError: expected X got Y` — exists but behaves wrong
- Type errors — useful for statically typed languages

## How to write the GREEN block

The GREEN block contains *only* the minimum code to pass the current step's test. Not the next test's requirements. Not helper utilities that seem useful. Not error handling that no test verifies.

The discipline of minimal GREEN code is the core teaching of TDD. When a step's implementation is deliberately thin, say so explicitly: "Notice we're not handling the empty cart case yet — we'll get there in Step 4."

## Where code goes in the file

Always tell the learner exactly where to type:
- "Open `cart.py`. If the file doesn't exist, create it."
- "Add this method inside the `Cart` class, after `__init__`."
- "Replace the existing `checkout` function with this version."

Never say "add this somewhere" or "update the Cart class." Be specific about file, class, and position.

## Tutorial file placement

When writing the tutorial into the project:
- `TUTORIAL.md` — if the project has no `docs/` directory
- `docs/tutorials/<feature-name>.md` — if `docs/` exists

Create `docs/tutorials/` if `docs/` exists but `tutorials/` does not. Never create `docs/` if it doesn't exist.
