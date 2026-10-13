# Story critic

The critic reads stories the way a stakeholder or a reviewer would: without
having watched them being written. It runs in a fresh context so it cannot
fill gaps with what the writer meant.

Rules 1 to 5 apply to every story and to the human header of a pairing slice.
Rules 6 and 7 apply to stories with tasks. Rule 8 applies to a whole breakdown.

## The rules

1. **Title.** It says what a person can now do or now has, using glossary
   terms. It names no implementation artifact: table, schema, migration, port,
   adapter, endpoint, route, handler, service, repository, model, controller,
   component, job, queue, config.
2. **Demo.** It describes something a person does and sees: a page, a command
   with visible output, a file, a message. A test run, a type check, or "the
   code compiles" alone is not a demo. A spike's demo is the answer it
   produces.
3. **Scenario.** It names a person (a role or a name) and a reason this matters
   to them, in plain words, in at most three sentences.
4. **Picture.** There is exactly one diagram. It shows the change a person
   would notice, not the internal structure. Node labels use glossary terms.
   About a dozen nodes at most.
5. **Acceptance.** Every line is observable from outside the code, in the
   user's words, and carries a requirement id when requirements exist. Status
   codes, function names, and table names belong in task Verify sections, not
   here.
6. **Tasks.** One to five. Each has a technical title, its own TDD plan, and
   its own Verify. A task that only makes sense together with another task is
   merged with it.
7. **Fit.** The tasks together deliver the Demo and every Acceptance line. No
   task builds something the story does not need.
8. **Breakdown.** Across all stories in the set:
   - The first story is a walking skeleton: the thinnest path a person can see
     working end to end.
   - No story exists only to set up another. Setup is a task.
   - No story is a single layer of the system.
   - Read in order, the titles tell the story of the product getting better.
   - Every requirement the set is meant to serve appears in some story's
     Serves line.

## The brief

Pass this to the critic sub-agent with the draft stories, `GLOSSARY.md`,
`CONTEXT.md` if it exists, and this file:

> You are reviewing draft stories for a software project. You did not write
> them. Read CRITIC.md and apply its rules to each story, then rule 8 to the
> set. For each story, answer PASS or REJECT. For each rejection, name the rule
> number, quote the offending text, and propose a rewrite in one line (a new
> title, a new demo, a merge, or a move to a task). Then give the breakdown
> verdict for rule 8 with the same format. Do not comment on anything the rules
> do not cover. Under 500 words.

## Reading the result

Revise every rejected story and rerun the critic. A story rejected three times
on the same rule goes to the user with the critic's objection beside it; the
user rules. Record an overruled objection in the hand-off so the reviewer of
the PR knows it was a choice.
