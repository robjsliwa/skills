# Splitting stories

A story is too big when it has more than five tasks, when its acceptance
criteria fall into groups with no shared prerequisite, or when its Demo needs
"and then" to describe. Split it so that every piece is still something a
person can see. A split that produces "backend story" and "frontend story" is
a split by layer, and both halves fail the Demo rule.

Try the patterns in this order. The first one that gives pieces of roughly
similar value usually wins.

## 1. Workflow steps

A journey with several steps becomes one story per step, or a thin story that
walks all steps simply followed by stories that thicken one step.

- Before: "Customer checks out."
- After: "Customer reviews the cart," "Customer pays by card," "Customer gets a
  confirmation email." Or: "Customer checks out with a fixed test card"
  (thin, end to end), then "Customer pays with a real card."

## 2. Business-rule variations

One behaviour with several rules becomes one story per rule, simplest first.

- Before: "Owner sets prices with discounts."
- After: "Owner sets a flat price," "Owner gives a percentage discount," "Owner
  gives a discount that expires."

## 3. Happy path, then unhappy paths

The path where everything works ships first. Each meaningful failure becomes a
story when the person would notice it.

- Before: "Visitor follows a short link."
- After: "Visitor follows a short link," "Visitor following an unknown link sees
  a clear message," "Visitor following an expired link sees when it expired."

## 4. One data variation first

Handle one kind of input end to end, then add the others.

- Before: "Owner imports their product list."
- After: "Owner imports products from a CSV," "Owner imports products from a
  spreadsheet."

## 5. One interface first

One device, one channel, or one client first.

- Before: "Customer gets order updates."
- After: "Customer gets order updates by email," "Customer gets order updates by
  text message."

## 6. Hardcode, then generalize

Ship the behaviour with a hardcoded value, then make it configurable in the next
story. The first story is still a real change a person can see.

- Before: "Owner chooses the store's currency."
- After: "Prices show in dollars," then "Owner chooses the store's currency."

## 7. Defer performance and polish

Make it work for a person, then make it fast or pretty in a later story, when
the slowness is something a person would notice.

- Before: "Owner searches thousands of orders instantly."
- After: "Owner searches orders," then "Search stays under a second with ten
  thousand orders."

## 8. Spike the unknown

When the hard part is not knowing, split off a spike whose Demo is the answer,
then write the real story once the answer exists. See SKILL.md.

## Splits to refuse

- **By layer.** Schema story, API story, UI story. Each is a task.
- **By CRUD for its own sake.** Create, read, update, delete as four stories is
  fine only when each is something a person does on its own. Often "Owner
  manages their links" splits better by workflow: "Owner creates a link," then
  "Owner fixes a typo in a link."
- **Setup stories.** "Set up the project," "Configure CI." These are tasks in the
  walking skeleton story.
- **Over-splitting.** "Add the button," "Wire the button," "Show the result."
  When the pieces are each a few minutes of work, they are one story with one
  task.
