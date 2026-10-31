# Lesson Plan

`lessons/NNNN-<slug>/plan.md` is written before any slide or lab step, and
everything built afterwards follows it. It is where the teaching decisions are
made, checked against PEDAGOGY.md's checklist, and kept for the record. Keep
it to two screens.

## Template

```md
# Lesson NNNN: {Title}

**Objective:** {One observable thing the learner can do after this lesson.}
**Milestone:** {What exists in the project at the end, and how they show it works.}
**Hook:** {The concrete failure, puzzle, or case that opens the lecture, with real values.}

## Where they start
- Builds on: {records LR-0003, LR-0005; lesson 1's CallMachine}
- Live misconceptions: {from records, or "none"}
- Guidance level: {full steps | goals and tests, hints collapsed | goal only}, because {records}

## The idea
{One sentence. The thing to carry forward.}

**Anchor:** {The familiar idea from MISSION.md's Anchors} → {where it breaks}.

## Lecture arc
| # | Slide id | Kind | Shows | Says (the point of the transcript) |
|---|---|---|---|---|
| 1 | title | title | promise | where we are going |
| 2 | last-time | picture | PhoneCore box, then the screen above it | warm-up recall, then today's piece |
| … | | | | |

**Predict points:** {slide id: question → answer, for each of two or three}

## Worked example
{The case traced end to end, with the values the values script must produce.}

## Lab
1. {Setup step: the workspace runs} → expect: {output}
2. {Step} → expect: {output}
…
**Challenges:** {2-4, each: what to do, how they know it worked, the kind: extend | break and fix | transfer}

## Parking lot
| Aside or edge case | Goes to |
|---|---|
| Default actor isolation details | Under the hood, lab step 6 (the tests) |
| Parser rejects a leading 1 | Challenge 1 |
| Observation tracks the whole `call` struct | Challenge 4 |

## Checks
**Teach-back:** {The question asked at the debrief, applied to their project.}
**Practice prompts:** {one or two open prompts for PRACTICE.md}
**Claims to verify:** {pointer to build/claims.json once inventoried}
**Sources:** {research notes and RESOURCES.md entries this lesson uses}
```

## Rules

- The objective is a verb the learner performs ("explain why…", "build…",
  "predict…", "write a paragraph that…"), never "understand."
- The lecture arc has ten to fifteen rows; LECTURE.md gives the order.
- Every lab step has an expected result. A step whose result cannot be seen is
  merged into the next.
- Everything true that does not fit goes in the parking lot with a
  destination. Nothing is dropped silently, and nothing is crammed in.
