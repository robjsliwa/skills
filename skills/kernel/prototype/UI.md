# UI prototypes

Several radically different versions of one screen, switchable in the
browser, so the human can flip between them and say which one, or which
parts of which. Usually the answer is "B's timeline with C's preview," and
that combination is the design.

## When this is the right shape

- "What should the reminders settings screen look like?"
- "Show me a few layouts for the dashboard before we commit."
- Any time someone would otherwise hold three vague layouts in their head
  and argue about them in words.

If the question is about rules or state, use [LOGIC.md](LOGIC.md). If only
the placement on one screen matters and there is nothing to compare, a
static mockup from the `visualize` skill is enough.

## In the app or standalone

**Prefer the app.** Variants judged inside the real page (real header, real
navigation, real data density) expose problems a blank page hides. Put the
variants on the real route behind `?variant=`, keep the route's data loading
as it is, swap only the rendered part, and mount the floating switcher from
[assets/switcher-snippet.md](assets/switcher-snippet.md). Commit on a
`prototype/<slug>` branch that is never merged. Something that has no page
yet but would live inside one (a new card on settings, a new step in
checkout) still goes inside that page.

**Standalone only when there is no app yet**, or the screen has no plausible
host: copy `assets/ui-variants-template.html` into the `prototypes/` folder.
It fakes a minimal app shell so the variants are not floating in a void.

## Process

1. **Write the question and the plan** in one line: "Three layouts for
   invoice reminders, on `/settings/reminders` behind `?variant=`." Default
   to three variants; five is the most that stay meaningfully different.
2. **Draft the variants so they disagree about structure**: what comes
   first, what the primary action is, how the information is grouped.
   Settings-first, time-first, and message-first are three variants. Three
   card grids in different colours are one. If two drafts look alike, redo
   one with an explicit ban ("no form").
3. **Use the same sample data in every variant**, realistic and taken from
   the glossary: "INV-2041, Northwind Studio, £1,840.00." Differences in
   data make variants incomparable.
4. **Fill the tradeoff drawer**: per variant, what it gains and what it gives
   up. If you cannot say what a variant gives up, you do not understand it
   yet.
5. **Click through every variant** at desktop and phone width, with the
   arrow keys and the pill, and check the console.
6. **Hand it over** with the URL and the keys: `?variant=a|b|c`.

## What the standalone template gives you

- `VARIANTS` (EDIT HERE 2): each with `id`, `name`, `render()` returning the
  screen's HTML, and an optional `mount(el)` for in-memory interactions
  (select a reminder, flip a switch). Nothing persists.
- `DATA` and `PROTO` (EDIT HERE 1), `TRADEOFFS` (EDIT HERE 3), and a block of
  variant CSS (EDIT HERE in the style block), each rule prefixed with its
  variant class.
- A low-fi kit in greys (`.box`, `.row`, `.input`, `.sw`, `.sbtn`, `.tagx`)
  so the layout is judged, not the paint.
- The floating pill: previous, the variant key and name, next, then "Pick
  this" and "Add a note." Left and Right arrow keys switch too, except while
  typing in a field. The URL keeps `?variant=` so a reload or a shared link
  lands on the same variant, and other parameters (the viewer's `?path=`)
  survive.
- Give interesting parts a `data-node` label; a note then says which part it
  is about.

## Closing the loop

Draw the decision as a screen-flow `flowchart` in the node file or design
doc: the screens the winner implies, with `click` on the screen node pointing
at the prototype file. Name what was taken from the losing variants. In the
app, the winner is rewritten properly on the feature branch, with the
component library and tests; the `prototype/<slug>` branch stays as the
record.

## Anti-patterns

- **Variants that differ in colour, copy, or spacing.**
- **A shared layout component across variants.** A shared header is fine;
  a shared layout defeats the point.
- **Real mutations.** Save buttons do nothing or change in-memory state.
- **Polish.** Brand colours, icons, animation. The review becomes about paint.
- **A switcher that can reach production.** Gate it on a development check.
- **Merging the prototype branch**, or copying variant code into the real
  page. It was written without tests; rewrite it.
