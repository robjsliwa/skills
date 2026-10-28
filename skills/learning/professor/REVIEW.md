# Review: the Cold Read

The author of a lesson cannot see its gaps: they know what every term means
and what comes next. So before delivery, a fresh agent that has seen nothing
but what the learner will see reads the lesson as the learner, and reports
where it got lost. Then the author checks the structure.

## 1. The cold read

Spawn one agent (the Agent tool; if none, do it inline and say so) with this
brief and nothing else from the session:

> You are a learner. Here is everything you know: {MISSION.md's Starting point
> and Anchors, verbatim}, plus lessons {list of done lessons, by title and
> one-line idea}. Read this lecture transcript and this lab in order, as if
> working through them. {Paste the transcript text of lecture.html slide by
> slide, with each slide's id and a one-line description of its picture, then
> the text of lab.html.}
>
> Report, as a table (location, problem, severity: blocking or minor):
> 1. Any term, name, or symbol used before it was explained.
> 2. Any code, table, or figure discussed before it was shown.
> 3. Any sentence you had to read twice.
> 4. Any step where you would not know what to do or what to expect.
> 5. Any jump: two new ideas at once, or a missing step between two.
> 6. Any edge case or aside that interrupted the main line.
> 7. Any predict question you could not attempt from what came before it.
> 8. Any claim that sounded uncertain or unsupported.
> Then: in two sentences, what is the lesson's main idea, as you understood it?

If its two-sentence summary does not match the plan's idea, that is a blocking
finding on its own.

## 2. The structural check (the author)

- [ ] `render_deck.py` prints `Clean.` and every screenshot was viewed.
- [ ] `assemble.py --strict-numbers` wrote the lab with no warnings left
      unexplained.
- [ ] Every predict slide's answer is the last step, and the transcript asks
      the learner to commit first.
- [ ] The lab reads correctly with every Under the hood box closed.
- [ ] Every lab step has Do, Run, Expect; every Expect came from `build/run/`.
- [ ] No challenge solution appears on the page.
- [ ] The parking lot's every item landed where the plan said.
- [ ] VOICE.md: no headline fragments, no "simply" or "just", no ornament the
      learner's `NOTES.md` did not ask for.

## 3. Fix and re-read

Fix every blocking finding, rebuild both pages, re-run the checks, and give
the cold reader the changed parts once more. Minor findings: fix the cheap
ones, list the rest in the session log. Done when the second read finds
nothing blocking.
