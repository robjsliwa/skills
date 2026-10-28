# Learning Record Format

Records live in `learning-records/NNNN-slug.md` (in a code repo,
`docs/code-along/learning-records/`), numbered from the highest existing
number. Create the directory when the first record is written. This is the
same format `teach-me` and `code-along` use.

Records are the teaching equivalent of ADRs: decision-grade facts about the
learner that steer what comes next.

## Template

```md
# {What was learned, disclosed, corrected, or changed}

**Trigger:** demonstrated | disclosed | corrected | goal shifted
**Lesson:** {NNNN, or "intake"}
**Evidence:** {how they showed it: a prediction made before the reveal, a
teach-back in their own words, a challenge solved, code they changed and why}

{1-3 sentences: what is now true and why it changes what to teach next.}
```

Optional, only when it adds something: `**Status:** superseded by NNNN`,
and an `## Implications` paragraph when what this unlocks or rules out is not
obvious.

## The four triggers

1. **Demonstrated.** The learner used a non-trivial idea correctly without
   being led: predicted an outcome, explained why, chose well and said why.
   This raises the floor.
2. **Disclosed.** The learner stated prior knowledge ("I've used SwiftUI at
   work"). Record the depth claimed, and treat it as a claim until a lab
   shows it.
3. **Corrected.** A misconception surfaced and was fixed. Always record these:
   they predict where related lessons will stumble. Quote what they believed.
4. **Goal shifted.** The mission moved. Link the new `MISSION.md`.

## Not a record

- Material covered. Wait for evidence.
- A term definition (that is `GLOSSARY.md`).
- A session log (that is `NOTES.md`).

## Supersession

When understanding deepens or a disclosed claim turns out wrong, mark the old
record `**Status:** superseded by NNNN`. Keep it: how understanding moved is
itself useful.
