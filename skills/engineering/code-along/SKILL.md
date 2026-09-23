---
name: code-along
description: >-
  Build a planned story together with the user as a lesson they code
  themselves, one story at a time, then debrief what they built before writing
  the next lesson. The human-in-the-loop alternative to tdd in the planning
  loop. Use when the user says "code along," "let's build this story
  together," "teach me while we build," "I want to understand this code," "I
  want to write it myself," or runs /code-along on a story file or with no
  argument to continue. Writes lessons and debriefs; never writes the
  project's source on its own initiative.
argument-hint: "A story file to start, or nothing to continue (debrief the open lesson, then write the next)."
---

# Code Along

The planning loop gets a feature to stories. `tdd` then builds each story for
the user, which is fast, and leaves them owning code they never wrote. This
skill builds each story *with* the user. Each story becomes a **lesson**: the
motive, a picture of where the slice sits, the ideas it needs, then RED to GREEN
steps the user types or pastes into their own editor. When they finish, a
**debrief** records what they actually built, what they changed and why, and
what they now know. Only then is the next lesson written, against the code that
now exists.

This is `teach-me`'s rhythm (plan once, one lesson per session, learning
records) applied to `elaborate-current-phase`'s rule (the built code is ground
truth for what comes next), one level down: per story instead of per phase.

Reference lives beside this file. Read each when its step says to.

- [LESSON-FORMAT.md](LESSON-FORMAT.md): the lesson template, step anatomy, the
  type/paste tags, the three modes, when to split into parts.
- [DEBRIEF.md](DEBRIEF.md): the divergence review, recall check, outcome table,
  pivot routing, learning records.
- [VERIFY.md](VERIFY.md): building and running the reference solution in a
  throwaway worktree so every block in a lesson is proven before the user sees
  it.

## Where things live

```
docs/planning/<slug>/
  stories/NN-MM-*.md            Status: ready-for-agent → in-lesson → done
                                + "As built" section when the user diverged
  lessons/NN-MM-<slug>.md       one lesson per story; debrief appended at the end
  lessons/NN-MM-<slug>.ref.patch  the verified reference solution, as a patch
docs/code-along/
  NOTES.md                      the learner: default mode, pace, known languages,
                                hard rules, session log
  learning-records/NNNN-*.md    what the user has demonstrably learned
```

A lesson split into parts is `NN-MM-a-<slug>.md`, `NN-MM-b-<slug>.md`, each with
its own `.ref.patch`. When stories live in a tracker (per
`docs/agents/issue-tracker.md`), name lessons by the issue reference instead of
`NN-MM`, and track state with the tracker's label or status (`in-lesson`, then
closed) rather than a `Status` line.

Learner state sits at the repo level, not per feature, so the first lesson of
the next feature already knows what this one taught.

**`docs/code-along/NOTES.md` outranks this skill.** Its hard rules and
preferences apply as written. Create it on first run with:

```markdown
# Code-along notes

## Preferences
- Default mode: type            # type | paste | attempt-first
- Pace: normal                  # brisk = fewer checks; thorough = more
- Languages and tools I know well:
- Explain in depth:             # topics the user wants slowed down

## Hard rules
- The agent never commits. I commit.

## Session log
```

Ask the user for the default mode and the languages they know well; leave the
rest at the defaults above.

## Which step to run

Read the state from disk, then take the first row that matches.

| State | Do |
|---|---|
| A lesson with `status: open` in frontmatter | **Debrief** it (below), then offer the next lesson |
| The user named a story, no open lesson | **Write the lesson** for that story |
| No argument, a phase with an unblocked story that has no lesson | **Write the lesson** for the first unblocked story, in `NN-MM` order |
| Every story of the current phase done | Stop. Hand off to `elaborate-current-phase` |
| No `phases.md` or no stories | Stop. Name the planning-loop step that is missing |

If two lessons are open, ask which one the user is working on. Never write a
new lesson while one is open; the debrief is what shapes the next lesson.

## Write a lesson

1. **Orient.** Read `NOTES.md`, every learning record, `CLAUDE.md`,
   `CONTEXT.md`, the story, the design sections it cites, the previous
   lesson's debrief, and every `As built` note in this phase's stories. Then
   read the code the story touches. The story's sample code is a sketch
   written before earlier stories were built; where the code disagrees, the
   code wins, and the lesson says so. Done when you can name the files the
   lesson touches and the seams it plugs into as they exist today.

2. **Check the tree.** Run `git status`. If there are uncommitted changes, stop
   and ask the user to commit or stash them; the lesson's base must be a
   commit. Record `git rev-parse HEAD` as the base. Done when the tree is clean
   and the base SHA is known.

3. **Plan the steps.** Turn the story's TDD plan into lesson steps, one RED to
   GREEN cycle each, in the order the story lists, simplest first. Re-derive
   any step the built code has made wrong. Pick the mode from `NOTES.md`
   unless the user named one. If the plan exceeds eight steps, split into
   parts per LESSON-FORMAT.md and plan part a only. List the ideas the lesson
   needs and drop every one a learning record or `NOTES.md` says the user
   already has. Show the user the step titles and the new ideas in five to ten
   lines and ask if the order and depth suit them. Done when they agree.

4. **Build and verify the reference** per VERIFY.md: in a throwaway worktree at
   the base, apply each step's RED code, run the tests, capture the real
   failure; apply its GREEN code, run, capture the pass. Run the story's
   verification commands at the end. Save the full diff as the `.ref.patch`.
   Remove the worktree. Done when every step's captured output is real and the
   final state passes every verification command.

5. **Write the lesson** per LESSON-FORMAT.md, cutting every code block from the
   verified reference, never retyping it from memory. Tag every block
   `type this` or `paste freely`. Write the "Before you debrief" questions last.
   Done when every step has its block, its placement, its real expected output,
   and the checklist in LESSON-FORMAT.md passes.

6. **Hand it over.** Set the story's `Status` to `in-lesson`. Append a line to
   the session log in `NOTES.md`. Tell the user the lesson's path, the mode,
   roughly how long it should take, and:
   > Work through it in your editor at your pace. Change anything you think
   > should be different; that is the point. When you're done, or stuck, or
   > want to change course, run `/code-along` and we'll debrief.

   Leave everything uncommitted for the user unless `NOTES.md` says otherwise.

## Debrief

Read DEBRIEF.md and follow it. In outline:

1. **Look.** Diff the user's work from the lesson's base SHA (committed and
   uncommitted, untracked files included), run the story's verification
   commands, and compare against the `.ref.patch`.
2. **Ask.** First an open question: how did it go, anything to flag? Then one
   question at a time about each divergence that matters. Record the answers;
   do not grade them.
3. **Recall.** Two or three fresh questions about the ideas the lesson taught,
   asked about the user's own code.
4. **Decide the outcome** with the user: done as-is, done with changes,
   partial, or pivot. Write what DEBRIEF.md's outcome table says for it.
5. **Record** learning records for what the user demonstrated, the debrief
   section in the lesson, `status: debriefed`, and the session log.
6. **Next.** On done or done with changes, ask the user to commit, then offer
   the next lesson. If the context is already heavy, recommend `/clear` and
   `/code-along`; the state on disk picks up where this left off. On partial,
   the next lesson is the remainder. On pivot, stop and name the planning step
   to run.

## Rules

- **The user's hands write the project.** Never create or edit source or test
  files in the working tree on your own initiative. You write lessons,
  reference patches, story status, and notes. If the user explicitly asks you
  to apply a block ("paste the fixtures for me"), you may, for that block, and
  the debrief records it as applied by the agent. If they want the whole story
  done for them, suggest `tdd` for it; mixing is fine.
- **Nothing unverified reaches the user.** Every code block and every expected
  output comes from a real run in the worktree. If you could not run
  something, the lesson says so in plain words at that step.
- **One lesson at a time.** Never write lesson N+1 before lesson N is
  debriefed, and never write lessons for a later phase.
- **The code is ground truth.** Each lesson is derived from the code the user
  actually has, including their divergences, not from the story's original
  sketch.
- **Divergence is data, not failure.** A change the user made for a reason is
  recorded and, if it affects later stories, carried forward.
- **Stuck is a valid debrief.** If the user comes back mid-lesson, debrief what
  exists; the outcome is usually partial, with a smaller next step.
- **Deep detours go to `teach-me`.** If a concept needs more than a few
  paragraphs, give the minimum the step needs and suggest
  `/teach-me <concept>` in a separate workspace.

## Self-check

Before handing over a lesson:

- [ ] Only one lesson is open, and it is for an unblocked story in the current
      phase.
- [ ] The base SHA in frontmatter is a clean commit.
- [ ] Every code block was cut from the verified reference; every expected
      output was captured from a real run.
- [ ] Every block is tagged `type this` or `paste freely`, with exact
      placement.
- [ ] No idea is taught that a learning record says the user already knows.
- [ ] Where the story's design and the real code disagree, the lesson says so.
- [ ] No source or test file in the working tree was touched.

Before closing a debrief:

- [ ] Every divergence that changes behaviour or a contract was discussed and
      recorded.
- [ ] Every acceptance criterion is checked off or carried into a remainder.
- [ ] Dependent stories affected by a change were amended, with the user's
      approval, or the drift was recorded in `phases.md`.
- [ ] Learning records were written only for demonstrated understanding.

## Hand off

Within a phase, `/code-along` is the whole loop: debrief, then the next lesson.
When the last story of the phase is debriefed as done, hand off to
`elaborate-current-phase`, which reads the debriefs and `As built` notes as
evidence when it reconciles the next phase.
