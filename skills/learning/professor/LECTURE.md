# Lecture

Fifteen to twenty minutes, ten to fifteen slides, built with the `slides`
skill. The lecture gives the learner the mental model the lab needs, and
nothing the lab does not need. The `slides` skill's `deck-template.html` is
a complete example of this arc (the dial-pad lesson).

## The arc

In order. Each line is one slide unless it says otherwise.

1. **Title.** The lesson's promise in one sentence: what they will be able to
   do, in the project's terms. Transcript: where the course is, what they will
   have by the end of the lab.
2. **Last time.** A picture of what already exists (the project so far, or the
   previous idea). Transcript opens with one recall question to answer in
   chat; the step reveals the answer and today's piece of the picture.
3. **The hook.** A concrete failure, puzzle, or case with real values, built
   in two or three steps so the problem lands before it is explained. No
   names for the concept yet.
4. **Predict.** A question the hook raises ("name one more way this goes
   wrong", "what happens if…"). Answer at the last step.
5. **The model** (one to three slides). The idea as a picture, built one layer
   per step: concrete first, then the structure, then the name and the rule on
   the final step. If an anchor helps, a two-column slide: the familiar idea
   and the new one, and where they differ.
6. **Worked example** (one or two slides). One case traced end to end, a row
   or a part per step, with verified values. This is the demonstration the lab
   will ask them to repeat.
7. **The mechanism** (optional, one or two slides). How it works underneath,
   when the lab needs it to make sense (how SwiftUI knows what to redraw).
8. **Predict.** Apply the model to a new case. Answer at the last step.
9. **Code or notation glimpse** (optional). The core of what the lab builds,
   condensed, with the parts highlighted step by step. Not for typing; for
   recognising in the lab.
10. **The bridge.** Today's lab in four or five steps and the one observable
    result that says it works. Transcript ends: "Any questions before we
    build?"

## Rules

- **The lecture is not the lab.** No setup instructions, no full listings, no
  troubleshooting. If the learner needs to type it, it is in the lab.
- **Two or three predict slides.** At least one before the model is named and
  one after it, so the second checks the model.
- **Activation first.** Slide 2 always recalls the previous lesson (or, for
  lesson 1, what the learner told you they already know).
- **No edge cases.** They are in the plan's parking lot.
- **Every number and line of code comes from `build/`.** When the deck quotes
  computed values or code, write it as `build/lecture.tpl.html` and assemble
  it to `lecture.html` with `fact-check`'s `assemble.py` before running the
  `slides` checker. (`deck-template.html` shows an assembled deck, so its
  values appear as text.)
- **Transcript paragraphs match steps.** One paragraph per step, about what
  that step shows (the `slides` skill's DECK-FORMAT.md).
- **Sources are linked in the transcript**, on the words they support.

## Addendum slides

When office hours produce an explanation worth keeping, add it as a
`slide addendum` after the slide it extends, with an id like
`addendum-why-class`. Re-run the checker. Tell the learner it is there.
