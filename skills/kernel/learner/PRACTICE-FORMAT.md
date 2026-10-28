# PRACTICE.md Format

`PRACTICE.md` is the spaced retrieval queue: open questions about ideas from
earlier lessons, each due at a later lesson. A teaching session opens with the
prompts that are due, asked in chat and answered in the learner's own words,
before anything new. It replaces an end-of-lesson multiple-choice quiz: the
learner generates the answer, gets feedback at once, and meets the idea again
after a gap, which is where retrieval does the most for retention.

## Template

```md
# Practice

| # | Prompt | From | Due | Last answer |
|---|---|---|---|---|
| 1 | Why can't the Call button go stale when `isValid` is never stored? | L2 | L3 | — |
| 2 | Typing a digit: which view bodies re-run, and how does SwiftUI know? | L2 | L3 | — |
| 3 | A call is a value. What does that buy over a class with a status field? | L1 | L4 | solid (L2) |

## Retired
- {prompts answered solidly twice, with the lessons}
```

## Writing a prompt

- **Open, not multiple choice.** "Why...", "What happens if...", "Explain
  ... to someone who knows Go", "Trace ... for input ...". The learner writes
  the answer.
- **About the idea, not the wording.** Ask for a prediction, a reason, or an
  application to a new case, never a definition to recite.
- **One idea per prompt**, answerable in two to five sentences or one small
  trace.
- **Mix old with new.** When two prompts are due, prefer ones from different
  lessons, so the learner has to pick which idea applies.

## Spacing rule

After the learner answers a due prompt, give feedback, then:

| Answer | Next `Due` | `Last answer` |
|---|---|---|
| solid, unprompted | two lessons later than the last gap (L+1 → L+3 → L+6) | `solid (Ln)` |
| partly right, or right only after a hint | the next lesson | `shaky (Ln)` |
| wrong | the next lesson, and write a "corrected" learning record | `wrong (Ln)` |

Retire a prompt after two solid answers in a row. Keep the queue to the
prompts that matter: at most three due per session.
