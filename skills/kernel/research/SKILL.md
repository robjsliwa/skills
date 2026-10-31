---
name: research
description: >-
  Answer a factual question from primary sources (official docs, specs, source
  code, first-party APIs) in a background agent, and write a cited findings
  note that ends with what the answer means for us. Also a recon variant that
  reads the local code and docs and reports what already exists. Use when a
  decision waits on a fact someone has already written down, when the user
  says "look into," "find out how X works," "what does the API do when," or
  when trailblazer, interview, spike, or solution-design need facts before
  asking the user anything.
argument-hint: "The question, and optionally where the note should go."
---

# Research

Finding facts is the agent's job; making decisions is the human's. This skill
does the first so the human only ever gets asked the second. It runs as a
background agent, so the conversation keeps going while it reads.

Research answers what is **written down somewhere**. If the answer only appears
when you run something ("does it keep up at our volume," "what does the payload
really look like"), that is a `spike`. If it is a judgement made by looking or
clicking, that is a `prototype`. If it is a choice, that is an `interview` turn.

## Two variants

- **Research**: an outside question. Primary sources, cited, written to a note.
- **Recon**: an inside question. What does this repo already have that bears on
  the topic: modules, seams, data shapes, conventions, ADRs, glossary terms,
  prior research in `docs/research/`, tests that pin behaviour. Recon writes no
  file unless asked; it returns a short report to the caller, who uses it so it
  never asks the human something the code answers.

## Write the brief

A subagent only knows what the brief says. Every brief carries:

1. **The question**, one sentence, sharp enough that "answered" is obvious.
2. **Why it matters**: the decision waiting on it, in one or two lines, so the
   agent knows which details count.
3. **What we already know**, with sources, so it does not re-derive them.
4. **Where to look first**: the official docs, the spec, the repo of the
   library, the local paths.
5. **Assumptions to confirm**: anything the answer depends on that only the
   user knows (the country, the plan tier, the volume). State the assumption so
   the agent answers for it, and flag it to the caller, who adds it to the map
   or asks the user.
6. **What not to do**: no blog posts or forum answers as sources (they may point
   to a primary source, which is then cited), no installing or running things
   (that is a spike), no recommendations beyond the question.
7. **The output**: the note's path and the template below (with its For
   teaching section when a teaching skill is the caller), or for recon, "reply
   with a report under 300 words."

Spawn it in the background with the Agent tool when there is one, and carry on.
Keep at most three research agents running at once. With no sub-agent tool, do
the research inline, say so, and keep it short.

## Where the note goes

In a teaching workspace (a `MISSION.md` at the root), `research/NNNN-<slug>.md`.
Inside a trail, `docs/research/<topic>/findings/<slug>.md`. Otherwise
`docs/research/<slug>.md`, or the `Research:` location in
`docs/agents/profile.md`. Match a convention the repo already has.

## The note

```markdown
# <The question>

**Checked:** <date>   **For:** <the decision or node it feeds, linked>
**Answer in one line:** <the direct answer, or "unknown" and why>

## Findings

- <Claim.> (**cited**: [Source title, section](url))
- <Claim.> (**inferred** from the two above)
- <Claim the sources disagree on.> (**conflict**: [A](url) says X, [B](url) says Y; which one owns the behaviour and why)

## Diagram

<Only when the mechanism is easier to see than read: a sequence or state diagram
per the `visualize` skill, labelled with what the sources call things, mapped to
glossary terms where they differ.>

## What this means for us

<Two to five sentences tying the answer back to the decision: what it rules
out, what it makes easy, what it leaves open. Any options it surfaces, each in
one line, for the human to choose between later.>

## For teaching

<Only when a teaching skill (professor, teach-me) asked for it. Four short
items, each from the sources above: the core idea in one sentence; the common
misconceptions and where they come from; one concrete example with real values
that shows the idea; and what a first lesson can safely leave for later.>

## Still unknown

<What the sources do not say, and whether a spike would settle it.>

## Sources

- [Title](url): what it is (official docs, spec section, source file at commit).
```

## Rules

- **Primary sources only.** Follow every claim to the source that owns it: the
  vendor's docs, the RFC, the library's code at a named version.
- **Every claim carries its strength.** `cited`, `inferred`, or `conflict`.
  Nothing unmarked.
- **Date it.** APIs and prices change; the note says when it was true.
- **Answer the question asked.** Interesting side findings go in one line under
  Still unknown or are left out.
- **Say "unknown" plainly.** A note that admits the docs are silent, and names
  the spike that would settle it, is a good note.

## Hand back

Tell the caller the one-line answer and the note's path. Inside a trail,
`trailblazer` updates the node with the answer and its strength, and mentions
it in the next playback. Outside a trail, offer the next step: the interview
question the answer unblocks, or a spike for what is still unknown.
