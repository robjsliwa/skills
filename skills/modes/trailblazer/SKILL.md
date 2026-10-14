---
name: trailblazer
description: >-
  Pair-research a big or foggy idea with the user, one question at a time,
  around a living Mermaid trail map in docs/research/<topic>/. The agent reads
  the code and docs before asking, sends background agents to research and
  spike while the conversation continues, shows every fork as small diagrams,
  plays back the redrawn map after each decision, and lets the user pick where
  to go next. Ends with a report and a hand-off to the right loop. Use when the
  user says "help me figure out," "explore this," "research this with me,"
  "I don't know where to start," "wayfind," runs /trailblazer, or when start
  or light find more fog than a plan can hold.
disable-model-invocation: true
argument-hint: "An idea to explore, or a topic to resume. Nothing, to resume the latest trail."
---

# Trailblazer

Some work arrives as fog: too big for one session, and nobody can yet say what
the questions are, let alone the answers. Trailblazer finds the way through it
**with** the user. It is pair research: the agent does the reading, running,
and drawing; the user does the deciding; the map in the middle is how both see
where they are.

The rhythm is a conversation, not an intake form. One question per turn, a
picture before a wall of text, facts fetched before anyone is asked, and after
every decision the map is redrawn and played back so the user always knows
where the trail stands.

Reference beside this file:

- [MAP-FORMAT.md](MAP-FORMAT.md): the trail map, node files, evidence words,
  and the report.
- [NODES.md](NODES.md): how to work each kind of node, the turn shapes, and the
  playback.

Skills it calls: `research` (facts, recon), `spike` (can it work), `prototype`
(how should it look or behave), `interview` (its turn anatomy only; see that
skill's note on trails), `visualize` (every diagram, the viewer), `glossary`
(terms and ADRs).

## Start or resume

Look for `docs/research/*/map.md` (or the `Research:` location in the profile).

- **The user named a topic with a map:** resume it.
- **No argument, and a trail is `exploring`:** resume the most recent one and
  say which. `parked` trails resume only when named.
- **A new idea:** start a trail. Pick a short kebab-case topic slug.

**Resuming** starts with a playback, never a question. Read `map.md`, the
active and recently decided node files, and every findings note or spike brief
newer than the last Session log line. For each blue or purple node, check its
output file: if it exists, fold it in; if it does not, the agent did not
survive the last session, so set the node back to open and say so in one line.
Then play back (step 6) and offer the next nodes.

## 1. Recon, quickly

Run `research` in its **recon** variant: what in the repo bears on the idea,
and what `GLOSSARY.md`, `CONTEXT.md`, `docs/adr/`, and earlier trails already
settle. It must finish before the first message, so keep it to a few minutes
(inline is fine). Nothing it answers is ever asked. A missing profile or
glossary is not mentioned now; it can wait for the report.

## 2. Open: one message, one question

The first message has four parts and nothing more:

1. **What you understand**, two or three sentences in the repo's words,
   including what recon found that matters.
2. **A first sketch**: one small Mermaid diagram of the idea as you see it now,
   solid for what exists, dashed for what is unknown.
3. **A drafted destination and anti-goal**, one line each, for the user to
   correct in passing: "I am assuming we are heading for a recommendation, and
   that late fees are out."
4. **One question.** If the user already named a fork ("email or SMS?"), ask
   about the part of it they can answer now, or the why behind it. Otherwise ask
   what would have to be true at the end for this to have been worth it, with
   your guess.

No list of questions. The sketch and the drafts are there to be corrected.

## 3. Draw the first map

From the reply, write `map.md` per MAP-FORMAT.md: the destination and
anti-goals (as corrected), and three to seven nodes for the unknowns you can
see, each with a kind (talk, research, spike, prototype, ask, task) and its
dependencies. Anything dimmer goes in **Fog**.

Start the docs viewer (`visualize`) now unless the user has said no, or the
session cannot run it: from here on the map lives there, and chat carries a
one-line pointer instead of Mermaid source. Without the viewer, put the
diagrams in chat.

Show the map with one question: "What is wrong or missing here?" Once the user
has answered, start the research nodes' agents: at most three at a time, the
rest wait as open nodes marked "queued" in their files.

Two turns from the user's first message to a real node is the target. Never
more than three.

## 4. Work one node at a time

Repeat:

1. **Offer the next node.** Recommend two or three from the **Frontier** (nodes
   whose dependencies are all decided), one line each on why now. Rank per
   NODES.md. The user picks, or names another. Never choose silently.
2. **Mark it active** (yellow) in the map.
3. **Work it by its kind**, per NODES.md.
4. **Decide.** The user rules on choices; facts resolve themselves. Write the
   node file's Evidence and Decision, every fact marked per MAP-FORMAT.md's
   evidence words.
5. **Update the map:** the node turns green, one line in Decisions so far, new
   nodes from what it opened, fog that can now be phrased as a question becomes
   a node, anything past the destination goes to Out of scope. Move nodes whose
   dependencies are now decided from Waiting to Frontier. Offer an ADR if the
   decision clears the bar. Collapse decided subtrees once the map passes about
   fifteen nodes.

## 5. Background work

Research and spike nodes usually run as background agents while the
conversation is on another node.

- A result that lands **while you are mid-question** does not interrupt. Write
  it into its node file and the map, and mention it in the next playback.
- A result that **changes the question on the table** gets one line after the
  current turn: "N3 just came back and changes this: <why>. Still want to decide
  now, or look at it first?"
- **No sub-agent tool:** do research between turns, inline and short, and say
  you did. Do not run a spike inline without asking; it blocks the conversation
  for its whole timebox. Offer "now, or at the end of the session?"

## 6. Play it back

A playback follows every **user decision** and starts every resumed session.
Background results never trigger one on their own. Shape per NODES.md:

- **Where we are**, at most 150 words: what was just decided and why, what came
  back from background agents since the last playback, and what that changes.
- **The map**, redrawn ("updated in the viewer" when it is running).
- **Next**: two or three recommended frontier nodes, and the question of which
  one.

## 7. Arrive, or park

**Arrive** when the frontier toward the destination is empty and no fog is left
in scope. Write `report.md` per MAP-FORMAT.md, set the map's status to
`arrived`, and hand off by destination type:

| Destination | Next |
|---|---|
| A decision | The ADR (with `glossary`); the report links it. Done. |
| A spec: a feature to build, architecture-heavy | `write-requirements`, pointed at `report.md` |
| A change: small, or one piece to build | `light` to plan and build it, or `pair-slice` with `report.md` as the source to build it together |
| A recommendation | The report is the deliverable. Offer an ADR if it commits to something. |
| An understanding | The report is the deliverable. Offer `teach-me` if the user wants to go deeper. |

**Park** when the user says to stop the trail, not just for today: write a
partial `report.md` (what is decided, what is open, what is running, how to
resume), set the status to `parked`, and log it.

## Conversation controls

The user can steer at any point, in their own words. Act without fuss: "zoom
out" (the whole map and Fog), "go deeper" (split the active node), "park it"
(the node back to Fog), "that's out" (Out of scope, with the reason), "look it
up" (research node), "spike it" (spike node), "show me" (prototype node), "ask
<person>" (ask node), "you decide" (decide, recorded as delegated), "stop for
today" (checkpoint), "park the trail" (step 7).

## Checkpoint

The disk is the memory. Every decision writes the node file and `map.md`
before the playback, so `/clear` costs nothing. At "stop for today," or when the
context is heavy, add a Session log line (what moved, what is still running,
the recommended next node) and offer to commit the trail folder. Resume handles
agents that did not finish.

## Rules

- **One question per turn.** Never a numbered list of questions. A downstream
  concern rides along as "a later node owns this."
- **Facts are the agent's job.** Recon, research, or spike before asking. Ask the
  user only for judgement, preference, or knowledge only they have.
- **Pictures for structure.** Every fork with two or more structural options is
  shown as two or three small diagrams side by side, a line of gains and a line
  of what each gives up.
- **Widen before narrowing.** Before recommending, make sure the options really
  differ. The smallest thing that could work, and not building it at all, are
  named in one line under the options when they are plausible, not drawn.
- **Short turns.** About 150 words of prose per turn, plus diagrams.
- **The user picks the next node.** Recommend, never choose silently.
- **The human answers human nodes.** Never answer your own talk or prototype
  question.
- **Terms wait until they matter.** New or fuzzy words go on the map's Terms in
  play; settle one with `glossary` only when a decision depends on it.
- **The map is an index.** A decision lives in its node file; the map gists it
  in a line and links.
- **No tickets.** The trail lives in files (ADR 0004). If the profile names a
  tracker and the user wants visibility, one issue may mirror the map with a
  link, updated on arrival.
