# Debrief

The debrief closes one lesson and decides what the next one is. It has two
jobs: find out what the user actually built and why, so the next lesson is
written against reality; and find out what they now understand, so the next
lesson starts in the right place. It is a conversation, one question at a
time, not a grading pass.

## Contents

- 1. Look
- 2. Ask
- 3. Recall
- 4. Decide the outcome
- 5. Record
- 6. Next
- Learning records
- The debrief section

## 1. Look

Before saying anything, gather the evidence:

```bash
base=<base SHA from the lesson frontmatter>
git log --oneline "$base"..HEAD            # what the user committed
git diff --stat "$base"                    # committed + uncommitted, tracked files
git status --porcelain                     # untracked files too
git diff "$base"                           # the full change
```

Then run the story's verification commands and note which pass.

Compare the user's change with the lesson's `.ref.patch` and sort every
difference into one of these:

| Kind | Example | What to do |
|---|---|---|
| Cosmetic | a name, formatting, file order | ignore, unless it is a pattern worth a word |
| Equivalent | a loop where the reference used a helper; a table test instead of three tests | ask briefly why; record |
| Better | a clearer name, an edge case the reference missed, a simpler shape | say so plainly; the user's version is now ground truth |
| Contract change | a changed signature, type, schema, error, or public behaviour | must discuss; check which later stories depend on it |
| Missing | an acceptance criterion not met, a step not done | feeds the outcome (partial) |
| Bug | a verification command fails; a behaviour is wrong | show the evidence; the user fixes it |

Also check for anything the user added that the lesson did not ask for. It is
either an equivalent, a better, or scope creep; ask which.

## 2. Ask

Open with one question and wait: "How did it go? Anything you want to flag
before I show you what I see?" The user's own account comes first. They may
already name the divergences, the pain, or a wish to pivot.

Then take the divergences that matter (not cosmetic ones), most consequential
first, **one question per message**. Each question:

- quotes the few lines in question from their code, and the reference's
  version when that helps,
- asks why, neutrally: "You returned an error here instead of `(Tenant,
  false)`. What made you go that way?",
- when useful, gives your view in one sentence after they answer, including
  when theirs is better.

For a **bug**, show the failing command and its output, ask what they think is
happening, and let them fix it. If they want help, write a one-step mini
lesson in the chat (the RED that exposes it, then the fix), in the same step
anatomy. Do not edit their file.

For **missing** work, ask whether they ran out of time, got stuck, or decided
it was not needed. Each leads somewhere different.

Stop asking when every contract change, bug, and missing piece has an answer,
or when the user says they want to move on; record what is still open.

## 3. Recall

Ask two or three questions, one at a time, that the user answers from memory
about **their own code**, not the lesson text. Different from the "Before you
debrief" questions, which they have seen the answers to.

- Explain: "In your `Verify`, why does the tenant check come before the
  expiry check?"
- Predict: "If someone calls `Lookup` with an empty id, what does your code
  return?"
- Transfer: "Where would you add rate limiting in what you built, and why
  there?"

Tell them briefly whether the answer holds up, and why. A wrong answer is the
most useful result of the debrief: correct it in a few sentences, and it is a
learning record (misconception corrected). Respect a "skip".

## 4. Decide the outcome

Propose one outcome with a one-line reason; the user confirms or picks
another.

| Outcome | When | Write |
|---|---|---|
| **Done as-is** | every criterion met, divergences cosmetic or equivalent | story `Status: done` |
| **Done with changes** | every criterion met, with a better or contract-changing divergence | story `Status: done` and an `As built` section; amend dependent stories (below) |
| **Partial** | some criteria unmet, and the rest of the story still makes sense | story stays `in-lesson`; the remainder becomes the next lesson part, or a new story `NN-MM+1` when it is a separable slice (with the user's approval, inserted in dependency order and added to `phases.md`) |
| **Pivot** | the user, or what the code revealed, says the plan is wrong | a `Drift` note in `phases.md`; stop and route (below) |

### The `As built` section

Append to the story, above `## Verification`:

```markdown
## As built

Lesson NN-MM, debriefed <date>.

- <What differs from the design above, one line each, with the user's reason.>
- <Public contract as it now stands, when it changed: the real signature.>
```

### Amending dependent stories

When a contract changed, find every open story in the phase that references
the old contract (its Interfaces, Sample code, TDD plan). Show the user the
edits you propose, as before/after lines, and apply them only on their
approval. Mark each edited line `(amended after NN-MM)`. If the change reaches
stories in a later phase, do not edit them; write a `Drift` note under that
phase in `phases.md` instead, since later phases are re-derived by
`elaborate-current-phase` anyway.

### Pivot routing

Name the smallest step that fixes the plan:

| What is wrong | Route |
|---|---|
| The remaining stories of this phase are sliced wrong | `to-story` on this phase only, with the debrief as input |
| This phase's scope or order is wrong | `elaborate-current-phase` (it will record Drift and re-plan) |
| Later phases are wrong too | `vertical-slice-phasing` on the remaining phases |
| The mechanism is wrong (a port, the data model, a boundary) | `solution-design`, then re-phase |
| What we are building is wrong | `write-requirements` (after a `grill-with-docs` if it is a big change) |

Write the `Drift` note, stop, and hand off. Do not write another lesson against
a plan you both believe is stale.

## 5. Record

- **The lesson:** append the debrief section (below) and set frontmatter
  `status: debriefed`.
- **The story:** status and `As built` per the outcome.
- **`phases.md`:** `Drift` notes only when the outcome calls for them.
- **Learning records:** per the next section.
- **`NOTES.md`:** any preference the user voiced ("less explanation of Go
  syntax", "attempt-first from now on") goes under Preferences; append a
  session-log line: date, lesson, outcome, one phrase on what was learned.

## 6. Next

- **Done / done with changes:** ask the user to commit their work (the next
  lesson's base must be a clean commit). Then offer the next lesson: the first
  unblocked story in the phase. If none is left, hand off to
  `elaborate-current-phase`.
- **Partial:** offer the remainder as the next lesson (part b), smaller if they
  were stuck.
- **Pivot:** hand off, as routed.

If the debrief ran long, recommend `/clear` then `/code-along`; the disk has
everything the next lesson needs.

## Learning records

`docs/code-along/learning-records/NNNN-<dash-case-name>.md`, numbered from the
highest existing. Create the directory with the first record. Format:

```markdown
# <Short title of what was learned or established>

<1-3 sentences: what the user now knows, and why it changes what to teach
next.>

**Evidence:** <how they showed it: a recall answer, a design choice they
explained, code they wrote.>
```

Write one only when one of these is true:

1. The user **demonstrated** understanding of something non-trivial: they
   explained it, predicted correctly, or made a sound design choice with a
   reason. Coverage alone is not learning.
2. The user **stated prior knowledge** ("I've used sqlc for years"). Record the
   depth they claimed.
3. A **misconception was corrected**. These predict future stumbling blocks;
   always record them.
4. The user's **goals shifted**: they now care about something different.
   Update `NOTES.md` too.

When a later record contradicts an earlier one, add `**Status:** superseded by
NNNN` to the old one rather than deleting it.

A learning record here uses the same format as `teach-me`'s, so the two can
share a directory if the user wants that; `NOTES.md` would say so.

## The debrief section

Appended to the end of the lesson file:

```markdown
---

## Debrief (<date>)

**Outcome:** done with changes
**Mode used:** type (switched to paste for fixtures)
**Applied by agent:** none

**What the user reported:** <one or two sentences in their words.>

**Divergences:**
- <kind> · <what> · <why, per the user>

**Recall:** <questions asked, one line each: held / corrected>

**Carried forward:** <story amendments, Drift notes, open items, or "none">

**Learning records:** 0007, 0008
```
