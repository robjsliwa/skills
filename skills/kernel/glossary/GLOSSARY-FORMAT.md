# GLOSSARY.md format

`GLOSSARY.md` lives at the repo root and holds the system's ubiquitous language:
the words people and agents use for the things the system is about. Every skill
reads it. Story titles, acceptance lines, and diagram node labels use its terms.

## Structure

```markdown
# <Product> Glossary

<One or two sentences: what domain this glossary covers.>

Related: [CONTEXT.md](CONTEXT.md) (system context), [docs/adr](docs/adr/) (decisions).

## Ordering

**Order**:
A purchase a customer has confirmed and paid for.
_Aliases_: purchase
_Avoid_: cart, basket, transaction
_Related_: Cart, Fulfilment
_Example_: "Once the customer pays, the cart becomes an order and is sent for fulfilment."

**Cart**:
The items a customer has chosen but not yet paid for.
_Avoid_: order, basket
_Related_: Order
_Example_: "The cart keeps its items for seven days."

## Fulfilment

**Fulfilment**:
Picking, packing, and shipping one order.
_Avoid_: shipping, dispatch (dispatch is one step of fulfilment)
_Related_: Order, Shipment
_Example_: "Fulfilment starts when an order is paid and ends when the shipment is handed to the carrier."
```

## Fields

| Field | Required | Meaning |
|---|---|---|
| **Term** | yes | The canonical word, bold, followed by a colon. Singular, capitalised as a heading word. |
| Definition | yes | One sentence on the next line. What the thing *is*, not how it works. Uses other glossary terms. |
| `_Aliases_` | no | Acceptable synonyms that mean exactly this. Usually none. |
| `_Avoid_` | yes when any exist | Words people reach for that are wrong or ambiguous here. Add a parenthetical when the reason is not obvious. |
| `_Related_` | no | Other glossary terms this one is defined against. |
| `_Example_` | yes | One sentence a user might actually say, using the term correctly. |

## Rules

- **Only settled terms.** A term goes in when the user has agreed to the word,
  the definition, and what to avoid. A term still in debate stays out.
- **Group by subdomain** under `##` headings once there are more than about ten
  terms. A flat list is fine before that.
- **Be opinionated.** One canonical word per concept. Everything else is an
  alias (rare) or `_Avoid_` (common).
- **One sentence definitions.** If it needs more, it is probably two terms, or
  the extra belongs in an ADR.
- **Resolve ambiguities explicitly.** "Here, *account* always means a billing
  account; a person signing in is a *member*."
- **Challenge conflicting usage.** When code, docs, or conversation use a term
  against its definition, raise it (see SKILL.md). Either the usage changes or
  the definition does, with the user's agreement.
- **Revise in place.** No stale entries.
- **Alphabetical within a group** unless a definitional order reads better.
