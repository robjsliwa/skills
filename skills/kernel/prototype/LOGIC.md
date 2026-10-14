# LOGIC prototypes

One HTML file that lets anyone drive a state model by pressing buttons and
watching the state change. The page is throwaway; the pure module inside it
is the part worth arguing about, and later the part worth lifting.

## When this is the right shape

- "Can a refund happen while the parcel is in transit?"
- "What happens if the second approval arrives after the first was revoked?"
- "Does this data model let me represent a part-paid, part-refunded order?"
- Rules that read fine in a table and fall apart in a sequence: business
  rules, lifecycles, permissions, pricing, quotas.

If the question is what a screen should look like, use [UI.md](UI.md). If
the interesting part is messages between parties (and what happens when one
is late or lost), use [FLOW.md](FLOW.md).

## Process

1. **Write the question** into `PROTO` (EDIT HERE 1): a title and one or two
   sentences in the domain's words. It renders at the top of the page.
2. **Write the pure module** (EDIT HERE 2). Pick the shape the question
   needs, not the one easiest to wire:
   - a **state machine** when "which actions are legal right now" is part of
     the question (the template's default),
   - a **reducer** `(state, action) => state` when every action is always
     legal and only the result matters,
   - a few **pure functions** over plain data when there is no current state,
     only calculations.

   Keep the template's surface so the page shell works unchanged: `STATES`,
   `ACTIONS`, `TRANSITIONS` (with an optional `guard` label), `INITIAL`,
   `FINAL`, `initial()`, `allowed(state)`, `step(state, action, arg)`
   returning `{ ok, state, reason }`, and `describe(state)` returning labelled
   fields. No DOM, no `document`, no page variables inside it. If you reach
   for one, the logic is leaking into the page.
3. **Write the page data** (EDIT HERE 3):
   - `FREE_PLAY`: one button per action, with realistic arguments.
   - `SCENARIOS`: three to five. The happy path, one case that is awkward on
     paper (two partial refunds that should hit a cap), and at least one
     illegal move marked `expect: "refused"`. Each scenario starts from
     `initial()`, so it runs the same way every time.
   - `TRADEOFFS`: per scenario, the rule it probes, what that rule gains and
     what it gives up.
4. **Run every scenario yourself**, then free-play the illegal buttons. A
   refused step must leave the state unchanged and say why in domain words.
5. **Hand it over** with the one scenario you most want an opinion on.

## What the template gives you

- **Current state**: every state as a chip with the current one filled,
  final states marked, the `describe()` fields with changed values
  highlighted, and the actions legal right now.
- **Guided scenarios**: tabs; each step is a real button, refusals show the
  module's reason inline, and free play during a scenario is flagged as
  drift.
- **Free play**: every action, any order; legal ones are outlined.
- **What happened**: a numbered log, refusals in red.
- **Close the loop**: "Copy as Mermaid" turns `TRANSITIONS` into a
  `stateDiagram-v2`, ready to validate with the `visualize` checker.
- The shared chrome: badge, tradeoff drawer, feedback bar ("Looks right",
  "Add a note").

## Anti-patterns

- **Tests.** A prototype that needs tests has stopped being one. The tests
  come when the module is lifted, through `tdd`.
- **A module that knows about the page.** Button handlers, `document`, or
  formatting for a specific element inside `Model`.
- **Code words on buttons.** `REFUND_REQ` means nothing to the person who
  has to react. Use the glossary terms.
- **Only happy paths.** The point is the case that should be impossible.
- **Generalising.** No plugin points for rules nobody asked about.
- **A raw JSON dump** instead of labelled fields. Non-developers stop reading.
