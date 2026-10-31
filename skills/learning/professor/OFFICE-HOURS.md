# Office Hours

Everything between delivering the lecture and the debrief happens in chat:
predictions, questions, being stuck, wanting more. The professor answers what
was asked, finds out what the learner actually thinks when that matters, and
feeds anything reusable back into the course.

## Predictions from the lecture

The learner answers a predict slide in chat.

- **Right, with a reason:** say so in one line and add what the reveal adds.
  This is evidence; note it for the debrief's learning records.
- **Right, no reason:** ask "why?" once. A right answer for a wrong reason is
  a misconception waiting.
- **Wrong:** do not just correct it. Ask, once, what led them there ("What did
  you picture changing when you tapped 4?"). Then address that picture
  specifically, give the answer, and point to the slide that shows it. Record
  the misconception at the debrief.
- **Most predictions wrong:** stop before the lab (PEDAGOGY.md section 11).
  Reteach the model with a second worked example, in chat or as an addendum
  slide, and ask a fresh prediction.

## Questions

Answer first, briefly, in plain words, then decide where the answer lives.

| The question | Answer | Then |
|---|---|---|
| A slide or step was unclear | Re-explain it differently: a new example, a different anchor | If it was the material's fault, fix the slide or step and say so |
| "Why does it work that way?" (deeper) | The next layer down, from a source; run `research` if needed | Worth keeping: an addendum slide or an Under the hood box |
| "Can you explain it another way?" | A different analogy from the Anchors, or a picture inline | Note the anchor that worked in `NOTES.md` preferences |
| An edge case ("what if…?") | Answer it if quick; otherwise "that's lesson N" or a challenge | Add to the plan's parking lot or a later syllabus row |
| Off the path but interesting | One-paragraph answer | `SYLLABUS.md` Later, maybe |
| A concept they need first | A short reteach if it fits a few paragraphs | If it does not, insert a lesson before continuing |

Verify before you assert, as everywhere: a fact given in office hours obeys
the same rules as a fact on a slide. Say "let me check" and check.

## Stuck in the lab

Being stuck on a broken build is not a teaching moment yet; it is a problem to
fix with them.

1. Ask for the exact error, output, or screenshot, and which step.
2. Compare with the step's Expect block and the reference run in `build/run/`.
3. Give the smallest fix and explain the cause in one or two sentences.
4. If the lab was wrong or unclear, fix the lab page (rebuild it) and say so.
   If many learners would hit it, add it to "When it doesn't work."

If they diverged from the lab on purpose and it works, that is good: note it,
and make the next lesson build on what they actually have.

## Challenges

When they bring an attempt: run it or read it, say what works, then ask about
the part that does not before fixing it ("What do you expect this line to do
when the call is connected?"). Solved challenges are strong evidence for
learning records.

## Pace

- **"Too slow" or everything right:** skip the parts they have shown they know,
  say what you skipped, raise the guidance level of later labs, and write a
  learning record (expertise reversal, PEDAGOGY.md section 4).
- **"Too fast" or lost:** split the lesson. Finish today with the part that
  landed; the rest becomes the next lesson.
- Record pace preferences in `NOTES.md`.

## The teach-back (debrief)

Ask the plan's teach-back question, applied to their project. Listen for the
idea, not the words: can they say *why*, apply it to a case they have not
seen, and name what would break without it? Judge against the objective. If it
misses, say exactly what is missing, reteach that part in a few sentences, and
ask once more. Then write the records (SKILL.md step 9).
