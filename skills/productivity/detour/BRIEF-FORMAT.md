# Detour brief format

One file per detour, `docs/detours/NNNN-<slug>.md`, committed in the repo whose
work was paused. Numbers are never reused. The brief is written once on the
way out; only Status, Returned, and Return change after that.

````markdown
# Detour 0002: How does context cancellation reach a blocked read?

**Status:** out            # out | answered | closed | dropped
**Opened:** 2026-10-18   **Returned:**
**Paused:** pairing, slice 0003 step 5 (docs/pairing/STATE.md)
**Repo:** /Users/me/code/invoices (feat/0003-invoice-totals)
**Go to:** teach-me, in ~/learning/go-concurrency

## The gap

How does cancelling a `context.Context` stop a goroutine that is blocked
reading from a network connection?

## Where it hit

Step 5 needs the reminder sender to stop cleanly when the request is
cancelled. The test hangs instead of failing:

/Users/me/code/invoices/internal/remind/sender.go:42

```go
n, err := conn.Read(buf) // never returns after cancel()
```

`go test ./internal/remind -run TestSenderStopsOnCancel` times out after 30s.

## What I already know

- I can use `select` with `ctx.Done()` on channels.
- I tried wrapping the read in a goroutine and selecting on its result; the
  goroutine leaks.
- Not sure whether `SetReadDeadline` is the idiom or a workaround.

## Unstuck means

I can explain why the read ignores the context, and write the cancel path for
`sender.go` myself, with a test that proves no goroutine leaks.

## Out of scope

- The retry policy (a later step of the slice).
- Context values; only cancellation.

## Start the detour

```text
cd ~/learning/go-concurrency
/teach-me how context cancellation reaches a blocked read. Detour brief: /Users/me/code/invoices/docs/detours/0002-context-cancellation.md
```

When unstuck: `/detour back /Users/me/code/invoices/docs/detours/0002-context-cancellation.md`

## Return

(written by `/detour back`)
````

## Header lines

- **Status:** `out` while away; `answered` when the Return is written;
  `closed` once the paused flow has folded it in; `dropped` if the user gave
  up on it.
- **Paused:** the flow (`pairing`, `code-along`, `trailblazer`, `interview`,
  `none`) and a pointer to its resume point: the slice and step, the lesson
  and step, the trail and node, or the interview pause file. The paused flow
  finds its briefs by this line.
- **Repo:** absolute path and branch, so a detour in another directory can find
  its way back.
- **Go to:** the destination skill, and for `teach-me` the workspace.

## Sections

- **The gap:** one sentence, a question. A detour with two gaps is two
  detours.
- **Where it hit:** the concrete motive. A `path:line` (absolute) and at most
  about fifteen lines of the code, error, or command output that matter. For a
  design fork, the options as the user saw them. Link to files, specs, ADRs,
  and trail nodes instead of copying them.
- **What I already know:** what the user knows and has tried, so the teacher
  starts in the right place. For `teach-me`, this is evidence for the zone of
  proximal development, not a learning record.
- **Unstuck means:** what the user will be able to do or decide at the end, in
  terms of the paused work. `teach-me` takes it as the lesson's target,
  `trailblazer` as its destination, `spike` as its pass criteria.
- **Out of scope:** what the detour must not grow into.
- **Context:** only when Paused is `none`. What the next session needs because
  no other file holds it: what the user was doing, uncommitted work (`git
  status --short`), decisions made in the chat that are not written anywhere
  else. Still short; still the question, not the conversation.
- **Start the detour:** the exact lines to type, with the brief's absolute
  path in the argument, then the return line.

## Return

Written by `/detour back`, which also fills the header's Returned date. Three
to five lines plus links.

```markdown
## Return

A blocked `Read` never looks at the context; it only returns when the
connection is closed or its deadline passes. So cancellation has to be turned
into one of those: watch `ctx.Done()` in a goroutine and call
`conn.SetReadDeadline(time.Now())`, which makes the read fail at once.

- Learned in: ~/learning/go-concurrency/lessons/0004-cancelling-blocked-io.html
- Learning record: ~/learning/go-concurrency/learning-records/0006-deadlines-not-context.md

**What changes:** step 5's plan holds. Add a goroutine-leak check
(`goleak`) to the test; the user drives step 5.

**Later:** whether the HTTP client's transport does this for us (not needed now).
```

"What changes" is written for the paused flow: the step to revise, the question
to re-ask with what is now known, or "nothing, carry on."
