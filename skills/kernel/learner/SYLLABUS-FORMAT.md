# SYLLABUS.md Format

`SYLLABUS.md` is the course: the project the learner builds across it, the
lens that says what "verified" and "a lab" mean for this subject, and the arc
of lessons, each pairing one idea with one project milestone. It is a plan,
so it changes: the learning records are the evidence that moves it.

## Template

```md
# Syllabus: {Topic}

**Mission:** [MISSION.md](MISSION.md)
**Lens:** {Engineering | Quantitative | Natural science | Humanities and law | Creative craft}
**Updated:** {date}

## The project
{2-4 sentences. What the learner will have built, written, composed, or
analysed by the end, and why it is a fair test of the mission. Where it
lives: `~/code/webrtc-phone`, `~/learning/macro/notebooks/`.}

## How we verify
{One line per kind of claim, from the lens: "code runs and its tests pass",
"every number recomputed in Python", "every quote matched to the edition in
RESOURCES.md", "harmony checked against the rules in Aldwell & Schachter".}

## Lessons

| # | Idea (the lecture) | Milestone (the lab) | Status |
|---|---|---|---|
| 1 | A call is a value: model state as data | `PhoneCore` package, eight tests green | done |
| 2 | One source of truth for many views | Dial pad on the iPhone, Call lights at 10 digits | lab |
| 3 | Who may mint a credential | Go token server returns a signed JWT | planned |

## Later, maybe
- {Ideas that came up but are out of the current arc, with where they came from}
```

## Status values

`planned` → `researched` → `lectured` → `lab` → `done`. A lesson the learner
skipped because they already know it is `skipped` with a record number.

## Rules

- **One idea per lesson, one milestone per lesson.** If the idea column needs
  "and," it is two lessons. The milestone is something the learner can run,
  show, or hand in, and it uses the idea.
- **Every milestone builds on the last.** The project grows one vertical slice
  per lesson; no lesson exists only to set up a later one.
- **Plan the next three, sketch the rest.** Rows past the next three are one
  line each and expected to change.
- **The arc follows evidence.** After each lesson, check the next rows against
  the new records: drop what is now known, insert a missing prerequisite.
- **Ideas use glossary words** once they are in `GLOSSARY.md`.
