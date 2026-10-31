# 5. Teaching skills share a learning kernel, and lessons have no quiz

**Status:** accepted
**Date:** 2026-10-28

## Context

`teach-me` held everything in one folder: the workspace formats, the voice,
figure drawing, page assembly, and the quiz widget. `code-along` copied its
learning-record format by reference. A second teacher, `professor`, needed the
same record, the same verification, and a new medium (lecture decks), and a
third would have needed them again.

`teach-me`'s lessons ended in a multiple-choice quiz. In a chat, open answers
with immediate feedback cost nothing, and the evidence favours them: with
corrective feedback, short-answer retrieval beat multiple choice on a later
test in a laboratory study (Kang, McDermott & Roediger 2007), and constructive
activities that produce new output outrank active ones like selecting
(Chi & Wylie 2014). An end-of-page quiz also comes minutes after the lesson,
when spaced retrieval would do more (Cepeda et al. 2006).

## Decision

Three kernel skills hold what any teaching skill needs: `learner` (the
workspace record), `fact-check` (claims ledger and verified assembly), and
`slides` (lecture decks). `professor` composes them with `research` and the
`interview` contract and holds only the teaching method. Lessons have no
multiple-choice quiz; retrieval is open-response: predict slides during the
lecture, a teach-back at the debrief, and spaced prompts from `PRACTICE.md` at
the start of later sessions.

## Consequences

- A teaching workspace can be read by any of the three teaching skills;
  `professor` adopts a `teach-me` workspace without migration.
- `fact-check` and `slides` are usable outside teaching (a PR walkthrough, a
  design talk, any page that quotes numbers).
- Learners lose the instant score a quiz gave. The practice queue and the
  learning records replace it as the measure of progress.
- `teach-me` keeps its own copies of the formats until it is retired.
