# FLOW prototypes

A click-through simulator of a sequence across participants. Each step is
one message; the human walks it with Next and Back, sees the payload, and
watches every participant's state change. Then they flip on a failure (a
timeout, a bad token, a duplicate) and watch the same story go wrong.

## When this is the right shape

- Auth flows: redirect, code exchange, refresh, an expired or invalid token.
- Webhook and event pipelines: signatures, retries with backoff, duplicates,
  events arriving out of order.
- Payments, provisioning, anything with a saga or a compensation step.
- Multi-agent or multi-service handoffs: who holds the work, who notices
  when a handoff is lost.

The test: two or more parties exchange messages, and the question is about
order, timing, or failure. One component's rules are [LOGIC.md](LOGIC.md);
a screen is [UI.md](UI.md). A Mermaid `sequenceDiagram` alone is enough when
nobody needs to see state change or a failure branch; draw that instead.

## Process

1. **Write the question** in `PROTO` (EDIT HERE 1). Name the outcome that
   matters: "does order 1042 end up paid exactly once, and who notices when
   it does not?"
2. **Define the flow as data** in `FLOW` (EDIT HERE 2):
   - `participants`: `id` (letters, digits, underscores, so it is a valid
     Mermaid id), `name`, and `short` for phone-width lane headers. Four or
     five at most.
   - `initialState`: per participant, the labelled fields that matter to the
     question. Not everything they own; only what the human should watch.
   - `steps`: the happy path. Each has `from`, `to` (the same id for an
     internal step such as "verify signature"), `label`, `kind` (`call`,
     `reply`, or `lost` for a message sent and never received), optional
     `bad: true`, a one-sentence `why`, a realistic `payload`, and
     `stateChanges` as `{ participant: { field: value } }`.
   - `failures`: each has `id`, `title`, `toggle` (the switch label), `from`
     (the index into `steps` where the failure takes over), and its own
     `steps`. The branch replaces the happy path from `from` onwards; a
     `from` equal to the number of steps appends (a duplicate delivery after
     everything went fine).
3. **Choose failures that test the question.** Two to four. Each should end
   in a state that answers it, good or bad: "paid once," or "stuck, and
   nobody is paged."
4. **Fill `TRADEOFFS`** (EDIT HERE 3) per scenario: what the design does
   about this case, what that gains, what it gives up.
5. **Walk every scenario yourself** to the end, toggle each failure from the
   middle of the happy path, and check the state panels tell the story
   without reading the payloads.
6. **Hand it over** pointing at the failure you are least sure about.

## What the template gives you

- **Scenario picker**: the happy path plus each failure, each starting from
  step 1.
- **Failure toggles**: switch to a failure branch while keeping your place
  if you have not passed the step where it starts. Toggle off to return to
  the happy path.
- **Lanes**: one per participant with lifelines, messages drawn as arrows up
  to the current step (dashed for replies, a cross for lost messages, red
  for failures). Click a past message to jump back to it.
- **Step detail**: the message, who sends it to whom, why it happens, and
  the payload as JSON. Next, Back, Restart, and the arrow keys.
- **State panels**: one per participant, changed fields highlighted.
- **Copy as Mermaid**: the scenario on screen as a `sequenceDiagram`, with a
  note where the failure was injected. This is the bridge back to the
  canonical record.
- The shared chrome: badge, tradeoff drawer, feedback bar.

## Closing the loop

For each scenario that settled something, paste its Mermaid into the node
file or design doc, validate it with the `visualize` checker, and trim it to
the messages the decision depends on (about 12). Write the decision next to
it: "dedupe on event id at insert, reply 200 on conflict, alert on three
consecutive 401s."

## Anti-patterns

- **Real calls.** No network, no queue, no sandbox account. The simulator is
  data; that is why it can be turned into Mermaid.
- **Every field of every participant.** State panels with twenty fields hide
  the one that changes.
- **Failures nobody would ask about.** Pick the ones that threaten the
  outcome in the question.
- **A single giant scenario.** Over about 15 steps, split the flow or start
  later.
- **Labels in code.** "POST /webhooks/payments evt_481" is fine; `handleEvt()`
  is not. The human is reading a story.
