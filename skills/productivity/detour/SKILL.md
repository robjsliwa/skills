---
name: detour
description: >-
  Step out of the work in progress to learn or explore something in a clean
  context, then come back with the answer. Leaving pauses the active flow
  (pairing, code-along, trailblazer, interview) through its own checkpoint,
  writes a committed brief in docs/detours/ that states the gap, where it hit,
  and what "unstuck" means, and prints the first line for professor (or
  teach-me), trailblazer, or spike. Returning writes the answer into the
  brief so the paused flow folds it in on resume. Use when the user says "I don't
  understand this yet," "I need to learn X first," "detour," "let me go figure
  this out," "hand this off," or runs /detour.
disable-model-invocation: true
argument-hint: "What you are stuck on, to leave. Or 'back' (and optionally the brief's path), to return."
---

# Detour

Mid-flow, the user hits something they do not understand or do not know how to
do yet. Explaining it here would bury the work under a lesson, and the context
is already full of the work. A detour leaves the work paused and safe, takes
the gap to a clean context where `professor` or `trailblazer` can do it justice,
and brings the answer back to exactly where the work stopped.

It is a round trip, not a hand-off. The work's own state is saved by the flow
that owns it; the detour only carries the question out and the answer back.

Format of the brief: [BRIEF-FORMAT.md](BRIEF-FORMAT.md).

## Which direction

- **No argument, or a description of the gap:** leave (below).
- **`back`**, with or without a brief path: return (below).
- **A brief path alone:** if its Status is `out`, return; if `answered`, say
  the paused flow will fold it in and name the command that resumes it.

## Is it a detour at all?

Before leaving, check the gap is worth a clean context. Say which row applies
in one line and act on it.

| The gap | Do |
|---|---|
| Fits in a few paragraphs and the user just needs enough to keep going | No detour. Answer it here, briefly, and carry on. |
| A fact someone has written down ("what does the API do when...") | No detour. Run `research` in the background here and keep working. |
| A concept the user wants to own, not just get past | Detour to `professor` (or `teach-me`, in a workspace that already uses it). |
| Fog: the user cannot yet say how to approach it, or what the options are | Detour to `trailblazer`. From inside a trail, this is a new node, not a detour. |
| "Can it even work?" with a long timebox | Detour to `spike`, or run it in the background here if the user would rather keep going. |

Recommend one, with the reason. The user can overrule.

## Leave

1. **Name the gap.** One sentence, as a question, in the user's words where
   possible. If the argument already says it, restate it and move on. Otherwise
   ask one question with your guess: "Sounds like the gap is how Go's context
   cancellation reaches a blocked read. Right?" Done when the user agrees the
   sentence is the gap.

2. **Find the active flow** and its resume point. Check in this order; the
   first match is the flow being paused.

   | Found | Flow | Resume point |
   |---|---|---|
   | An interview in this conversation, no trail active | interview | the question on the table |
   | `docs/pairing/STATE.md` with an active slice | pairing | the slice and its next step |
   | A lesson with `status: open` under `docs/planning/*/lessons/` | code-along | the lesson and the step the user is on (ask if unknown) |
   | A trail in `docs/research/*/map.md` with `Status: exploring` | trailblazer | the active node |
   | None of these | none | the branch, `git status`, and what the user was doing |

   An interview inside a trail belongs to the trail: the flow is trailblazer.

3. **Number the brief.** Next free `NNNN` in `docs/detours/` (the `Detours`
   location in `docs/agents/profile.md` if it names one), with a kebab-case
   slug from the gap.

4. **Pause the flow** with the tool that owns its state. Never duplicate that
   state in the brief; point at it.

   - **pairing:** call the Skill tool with `pair-checkpoint`, passing the note
     "Detour NNNN: <the gap>". Then add to `STATE.md`'s Open threads:
     `- Detour NNNN out (<destination>): <the gap>. docs/detours/NNNN-<slug>.md`.
   - **code-along:** append a `## Detours` line to the open lesson
     (`- Step N: detour NNNN, <the gap>`) and a session-log line to
     `docs/code-along/NOTES.md`. Leave the user's code exactly as it is.
   - **trailblazer:** move the active node to Waiting with "Waiting on: detour
     NNNN (<destination>)", and add a Session log line per the trail's
     Checkpoint.
   - **interview:** write the pause file per the `interview` skill's "Pause
     and resume" section.
   - **none:** the brief's Context section carries what the next session
     needs (BRIEF-FORMAT.md says what goes there).

5. **Ask where the detour runs**, only for `professor` or `teach-me`: its workspace is the
   directory it runs in, usually not this repo. One question, with a
   recommendation: an existing workspace for the subject if the user has one,
   else `~/learning/<subject>`. Trailblazer and spike run in this repo.

6. **Write the brief** per BRIEF-FORMAT.md: the gap, where it hit (the real
   code, error, or fork, as `path:line` plus the few lines that matter), what
   the user already knows or tried, what unstuck means, what is out of scope,
   and the start line. Use absolute paths: the detour may run in another
   directory. Redact secrets, tokens, and personal data as `<REDACTED>`.
   Done when a fresh agent given only the start line could begin without
   asking what the problem is.

7. **Commit** the brief, and the pause file if one was written, by path, in the
   repo's commit convention: `docs: detour NNNN, <the gap>`. Pairing has
   already committed through `pair-checkpoint`; commit the brief on the same
   slice branch. If the flow's rules say the user commits (code-along's
   `NOTES.md` hard rule, or the working agreement), show the message and leave
   it for them.

8. **Hand over** in four lines at most:

   > Paused: slice 0003, step 5 (saved on feat/0003-invoice-totals).
   > Brief: docs/detours/0002-context-cancellation.md
   > Next: `/clear`, then in ~/learning/go-concurrency:
   > `/professor how context cancellation reaches a blocked read. Detour brief: /abs/path/docs/detours/0002-context-cancellation.md`

   Then: "When you're unstuck, run `/detour back` there."

## Return

1. **Find the brief.** The path given, or the only `Status: out` brief in
   `docs/detours/` of the current directory, or the path the detour's own
   session was started with. If none can be found, ask for the path.

2. **Gather what the detour produced:** the lessons and learning records it
   wrote (professor or teach-me), the trail's `report.md` (trailblazer), the spike brief
   and verdict (spike). Read them.

3. **Ask the user to say it back**, one question: "In your own words, what's
   the answer, and what would you do differently at <where it hit> now?"
   Saying it is retrieval practice, and it tells you whether the gap is really
   closed. If the answer misses the brief's "Unstuck means", say what is
   missing and offer to stay on the detour.

4. **Write the Return section** per BRIEF-FORMAT.md: the answer in three to
   five lines (the user's version, corrected only where wrong), links to what
   the detour produced, and what changes for the paused work. Set Status to
   `answered`. If the user gives up on it, set `dropped` with one line on why,
   and write what the paused work should do without the answer.

5. **Leave the commit to the paused flow.** The brief rides in its next
   commit, because the user may be on another branch, or in another
   directory. Say so.

6. **Point back** in two lines: the brief's Status, and the command that
   resumes the paused flow (`/pair`, `/code-along`, `/trailblazer <topic>`,
   `/interview resume <slug>`, or for none, "start a session in <repo> and
   read the brief").

## Folding in (for the paused flows)

When a flow resumes, it reads every brief in `docs/detours/` whose `Paused`
line names it:

- **`answered`:** mention it in the first brief or playback in one line, apply
  "What changes" (re-ask the paused question, revise the next step, amend the
  lesson), then set Status to `closed`, and commit with the flow's next commit.
- **`out`:** the detour is still running. Say so in one line; carry on with
  what does not depend on it, or wait if the next step does.
- **`dropped`:** do what its Return section says.

The `pair`, `code-along`, `trailblazer`, and `interview` skills each say where
this happens in their resume.

## Rules

- **A round trip.** Every brief ends `answered`, `closed`, or `dropped`, never
  forgotten. A brief still `out` is an open thread wherever it shows up.
- **The flow owns its state.** The detour pauses it through the flow's own
  checkpoint and points at it. It never copies a slice, a lesson, or a trail
  into the brief.
- **The question, not the conversation.** The brief carries the gap and its
  concrete motive. A summary of the session is noise to a teacher.
- **One question per turn**, with a recommendation, as everywhere.
- **Never discard work.** No reset, stash, or checkout on the user's behalf.
  Uncommitted work stays where it is and the brief says it exists.
- **Small detours.** "Out of scope" in the brief keeps the detour to the gap.
  What it opens beyond that goes in the Return section as a later thread, not
  into the detour.
