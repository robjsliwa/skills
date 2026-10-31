---
name: learner
description: >-
  Own the learner's record in a teaching workspace: MISSION.md (why they are
  learning and where they start), SYLLABUS.md (the course arc, the project, and
  each lesson's status), RESOURCES.md (trusted sources and communities),
  learning-records/ (what they have demonstrably learned), PRACTICE.md (the
  spaced retrieval queue), GLOSSARY.md, and NOTES.md. Reads them to place the
  zone of proximal development and writes them when evidence arrives. Lessons
  are numbered `NNNN` in file names and `L<n>` in tables (`L2` is
  `lessons/0002-*`). Use when a teaching skill (professor, teach-me, code-along) starts or closes a
  session, when the user states prior knowledge, shows they understand or
  misunderstand something, changes their goal, or asks "what have I learned,"
  "what's next," or "where am I in the course."
argument-hint: "Optional: 'orient', 'record <what happened>', or 'status'."
---

# Learner

Every teaching skill needs the same answers before it says a word: why is this
person learning, what do they already know, what did they get wrong last time,
and what comes next. This skill owns the files that hold those answers, so
`professor`, `teach-me`, and `code-along` read and write one record instead of
three. (`teach-me` keeps identical copies of these formats until it is retired.)

The record is evidence, not a diary. A file changes when the learner shows
something (says it back, predicts correctly, builds it, gets it wrong in an
instructive way), never because material was merely covered.

## The files

All at the workspace root unless noted. A workspace is one subject, usually its
own directory (`~/learning/<subject>`).

| File | Holds | Format |
|---|---|---|
| `MISSION.md` | why, where they start, what success looks like | [MISSION-FORMAT.md](MISSION-FORMAT.md) |
| `SYLLABUS.md` | the project, the lens, the lesson arc and each lesson's status | [SYLLABUS-FORMAT.md](SYLLABUS-FORMAT.md) |
| `RESOURCES.md` | high-trust sources and communities, annotated | [RESOURCES-FORMAT.md](RESOURCES-FORMAT.md) |
| `learning-records/NNNN-slug.md` | what was demonstrated, disclosed, corrected, or changed | [RECORD-FORMAT.md](RECORD-FORMAT.md) |
| `PRACTICE.md` | open retrieval prompts, each with the lesson it is next due | [PRACTICE-FORMAT.md](PRACTICE-FORMAT.md) |
| `GLOSSARY.md` | the workspace's canonical terms, added only once used correctly | [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md) |
| `NOTES.md` | preferences, hard rules, session log | below |

`NOTES.md` outranks every teaching skill. Its hard rules (where the learner's
own code lives, who commits, which language to answer in, "no epigraphs") apply
as written. Keep three sections: `## Hard rules`, `## Preferences`,
`## Session log` (one line per session: date, lesson, what changed), plus
`## Lens notes` when the subject has conventions every lesson must follow
(notation, tools).

## Orient (start of a session)

Read, in this order: `NOTES.md`, `MISSION.md`, `SYLLABUS.md`, every learning
record (superseded ones only for history), `PRACTICE.md`, `GLOSSARY.md`,
`RESOURCES.md`. Then report to the caller, in at most eight lines:

1. The mission in one sentence.
2. The current lesson and its status, or the next planned one.
3. The floor: what the learner has demonstrably learned that this lesson builds
   on (cite record numbers).
4. Live misconceptions: corrected ones that predict stumbles here.
5. Practice due: the prompts whose `Due` is this lesson or earlier (at most
   three, oldest first).
6. Gaps: anything missing (no mission, no syllabus, no source for the topic).

Done when the caller can name the lesson's target in one sentence tied to the
mission, and knows which prompts open the session.

### Adopting a teach-me workspace

A workspace with `lessons/*.html`, `learning-records/`, and `MISSION.md` but no
`SYLLABUS.md` came from `teach-me`. The records and mission formats are the
same, so nothing is migrated. Draft `SYLLABUS.md` from the existing lessons
(each becomes a `done` row) plus the next steps the mission implies, add the
`## Starting point` section to `MISSION.md` from the records, and confirm both
with the user in one question. Leave the old lessons where they are.

## Record (end of a session, or when evidence arrives)

Write a learning record when one of the four triggers in RECORD-FORMAT.md
fires, and only then. In the same pass:

- **Glossary.** Add a term the learner has now used correctly in their own
  words. Never a term they have only read.
- **Practice.** For each idea the lesson made central, add one open retrieval
  prompt (PRACTICE-FORMAT.md) due at the next lesson. When the learner answers
  a due prompt, update it per the spacing rule there.
- **Syllabus.** Move the lesson's status and adjust what follows if the
  evidence says the plan was wrong (too easy, too hard, a prerequisite missing).
- **Mission.** If the goal moved, confirm the change with the user in one
  question, then rewrite `MISSION.md` and write a record with trigger 4.
- **Notes.** One session-log line.

Done when every file the evidence touches is updated and nothing was written
on coverage alone.

## Status (when the user asks where they are)

Answer from the files, in prose: the mission, how far through the syllabus,
what is solid (records), what is shaky (misconceptions, prompts answered
wrong), and the next lesson. Offer to open `SYLLABUS.md`.

## Rules

- **Evidence or nothing.** Coverage is not learning. A record cites how the
  learner showed it.
- **One workspace, one mission.** Two unrelated subjects are two workspaces.
- **Ask, don't infer, about the learner.** Prior knowledge, time, and goals come
  from the learner, one question at a time with a recommendation (the
  `interview` skill's contract), never from guesses.
- **Revise in place, supersede records.** Stale mission or syllabus text is
  rewritten; a wrong record is marked superseded, never deleted.
- **Formats are shared.** `code-along` writes records in the same format, so a
  repo's `docs/code-along/learning-records/` and a workspace's
  `learning-records/` can be read the same way.
