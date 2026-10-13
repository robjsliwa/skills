---
name: story
description: >-
  Write, split, or check stories that a person can see: each story is one
  change with a Scenario, a Demo, a Picture, and Acceptance in the user's
  words, and owns the context-window sized Tasks an agent builds. Runs a
  critic in a fresh context before anyone sees the breakdown. Use when
  writing or reviewing stories, when a story reads like a work order ("add
  table," "create port"), when the user asks to split a story, or when
  to-story, light, or pair-slice need the format or the critic.
---

# Story

A story is the unit a person reads. It answers one question: after this ships,
what can somebody do that they could not do before, and how would I show them?
A task is the unit an agent builds: one context window, one run of
red-green-refactor, with the design detail it needs. A story owns its tasks, in
the same file (ADR 0001).

The failure this skill exists to prevent is the work-order story: "Create the
SQLite database," "Tenant port," "Wire the adapter." Each is real work, and none
is something a person can see. They are tasks. The story is the change they add
up to.

Reference beside this file:

- [FORMAT.md](FORMAT.md): the story file, field by field, with a worked example.
- [SPLITTING.md](SPLITTING.md): how to split a big story so each piece is still
  something a person can see.
- [CRITIC.md](CRITIC.md): the numbered rules, and the brief for the critic
  sub-agent.

## Write a story

1. **Start from a person.** Name who is doing this and why it matters now. If
   nobody can be named, the work is a task inside another story, or a spike
   (below). Read `GLOSSARY.md` and `CONTEXT.md` first; the actors and terms are
   there.
2. **Write the Demo before anything else.** "After this ships, I open ___, do
   ___, and see ___." If the only demo you can write is a test run, stop: this
   is a task. The Demo uses the profile's `Run the app` command where there is
   one.
3. **Title it by what the person can now do**, in glossary words: "Visitor
   follows a short link," not "Redirect endpoint."
4. **Draw the Picture** with `visualize`: the slice of the journey, the screen
   flow, or the sequence this story lights up. Glossary terms as node labels.
   One diagram, about a dozen nodes at most.
5. **Write Acceptance** as observable outcomes, each tied to a requirement id
   when requirements exist. Outside-in: what a person or a calling system sees,
   not which function was called.
6. **Write the Tasks.** One to five. Each carries only what it needs from the
   design: interfaces and types, data, algorithm, sample code, files, a RED-first
   TDD plan, and Verify commands. Contract-first lives here: the walking
   skeleton's T1 often defines the interface or schema that later tasks and
   stories build behind.
7. **Write Out of scope and Verification.** Verification is the Demo as
   commands, plus the full test command.

## Split a story

More than five tasks, two groups of acceptance criteria with no shared
prerequisite, or a Demo with "and then" in the middle all mean split. Use
SPLITTING.md: workflow steps, business-rule variations, happy then unhappy
paths, one data variation first, one interface first, hardcode then generalize,
defer performance, or spike the unknown. Never split by layer. Every piece
passes the same rules as the original.

## Spikes

When the unknown is the work ("which payment provider," "can the parser keep
up"), write a spike story. Its Demo is the answer: "I read the note in
`docs/adr/` and know which provider we use and why," or "I run the benchmark and
see the throughput number." It is time-boxed, its single task produces evidence,
and its output is a decision, not production code.

## Check a breakdown

Before a set of stories reaches the user, run the critic:

1. Spawn one sub-agent with a fresh context. Give it only the draft stories,
   `GLOSSARY.md`, `CONTEXT.md` if it exists, and CRITIC.md, plus the brief at
   the bottom of CRITIC.md. Nothing from this conversation; the point is a
   reader who did not watch the stories being written.
2. Revise every story it rejects, then run it again.
3. After three rounds on the same story, stop revising. Show the user the
   critic's objection beside the story and let them rule.

With no sub-agent tool, re-read CRITIC.md from disk and check each story line by
line yourself, and say in the hand-off that the critic ran in this context.

## Rules

- **A story is something a person can see.** Infrastructure, schema, ports, and
  wiring are tasks inside the first story that needs them.
- **A task is sized for an agent.** One context window, one TDD plan, its own
  Verify. If a task needs another task's details to make sense, they belong
  together or the design is missing a seam.
- **The human part comes first in the file.** Scenario, Demo, Picture, and
  Acceptance before any task detail, so a reviewer stops reading when they have
  what they need.
- **Glossary words everywhere a person reads.** A term the glossary lacks is
  either a new term to settle with `glossary` or a sign the story drifted into
  implementation.
- **v1 stories still work.** A story with a `## What to build` and a TDD plan
  but no tasks is read as one story with one task. New stories use FORMAT.md.

## Hand off

The story goes to whichever build mode the user picks: `tdd` (the agent builds
it, task by task) or `code-along` (the user builds it from a lesson). A pairing
slice uses only the human header (Scenario, Demo, Picture, Acceptance); its plan
steps play the role of tasks.
