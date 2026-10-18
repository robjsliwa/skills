# Notation

Start from the question the reader is asking. The question picks the diagram,
and the diagram has a home artifact where it lives.

| Question | Diagram | Lives in |
|---|---|---|
| Who uses it, what is outside | C4 L1 context: flowchart, person and system classes | `CONTEXT.md`, requirements |
| What the user goes through | `journey` | requirements, phases (story map) |
| Which screens in which order | flowchart screen flow, nodes link to mockups | requirements, stories |
| What the deployables are | C4 L2 containers: flowchart with subgraphs | design |
| What is inside one container | C4 L3 components: flowchart | design (only when needed) |
| How a request flows | `sequenceDiagram` | design, story Picture, task |
| What states it can be in | `stateDiagram-v2` | design, task |
| What the data is | `erDiagram`; `classDiagram` for ports and domain types, sparingly | design, task |
| Which option and why | two or three small diagrams side by side in an options block | interview, ADR |
| What this change did | one diagram of the type that fits (see the `pr` skill) | PR body |

## C4 in one paragraph

C4 zooms in on a system in levels. **L1 context**: the system as one box, the
people who use it, and the systems outside it. **L2 containers**: the things
you deploy or run (web app, API, database, queue, worker) and how they talk.
**L3 components**: the modules inside one container. **L4 code** is the code
itself; do not draw it. Most work needs L1 once (in `CONTEXT.md`) and L2 once
(in the design). Draw L3 only for the container a design actually changes.

## Why flowcharts, not Mermaid's C4 types

Mermaid has `C4Context` and friends, but they are marked experimental, their
styling is fixed, their layout cannot be steered (no direction, no layout
statements, boxes land where they land), and they have no legend or tag
support worth using. Flowcharts render everywhere, take `direction`,
subgraphs, and `classDef`, and diff cleanly. The shared classes and label
convention are in [C4-STYLE.md](C4-STYLE.md).

## UML: what is worth drawing here

- **Sequence diagram.** Yes. The best picture for a request crossing
  components, retries, and who waits on whom.
- **State diagram.** Yes. Any entity with a status field gets one before its
  transitions are coded.
- **Class diagram.** Sparingly. For ports (interfaces) and the few domain
  types they pass, not for every struct. Data shape goes in an ER diagram.
- **Activity diagram.** Draw it as a flowchart with decision diamonds; Mermaid
  has no activity type and a flowchart reads the same.
- **Skip:** use case diagrams (a journey or C4 L1 says more), component and
  deployment diagrams (C4 L2 and L3 replace them), object, package, timing,
  communication, and interaction overview diagrams.

## Examples

Short ids, glossary terms as labels, one caption sentence after each.

### C4 L1 context

```mermaid
flowchart LR
  shopper(["Shopper<br/>[Person]<br/>buys things"]):::person
  clerk(["Clerk<br/>[Person]<br/>packs and ships"]):::person
  shop["Shop<br/>[System]<br/>sells and fulfils orders"]:::system
  pay["Payment provider<br/>[External system]"]:::external
  carrier["Carrier<br/>[External system]"]:::external
  shopper -->|"places orders"| shop
  clerk -->|"fulfils orders"| shop
  shop -->|"charges cards"| pay
  shop -->|"books shipments"| carrier
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef system fill:#1168bd,stroke:#0b4884,color:#fff
  classDef external fill:#8a8a8a,stroke:#5e5e5e,color:#fff
```

Two people use the shop; money and parcels are the two things we hand to
someone else.

### Journey

```mermaid
journey
  title Shopper buys a gift
  section Find
    Search for a product: 4: Shopper
    Compare two products: 2: Shopper
  section Buy
    Add to basket: 5: Shopper
    Check out: 3: Shopper
    Pay: 2: Shopper, Payment provider
  section After
    Track the parcel: 4: Shopper
```

Comparing and paying score lowest, so those are the stories to slice first.

### Screen flow, linked to mockups

```mermaid
flowchart LR
  basket["Basket"] --> address["Delivery address"]
  address --> payment["Payment"]
  payment -->|"card declined"| payment
  payment -->|"paid"| confirm["Order confirmed"]
  click basket "mockups/basket.html"
  click address "mockups/delivery-address.html"
  click payment "mockups/payment.html"
  click confirm "mockups/order-confirmed.html"
```

A declined card returns to Payment, not to the Basket; each box opens its
mockup.

### C4 L2 containers

```mermaid
flowchart LR
  shopper(["Shopper<br/>[Person]"]):::person
  subgraph shop["Shop [System]"]
    web["Storefront<br/>[Container: React]<br/>browse and check out"]:::container
    api["Orders API<br/>[Container: Go]<br/>takes and tracks orders"]:::container
    worker["Fulfilment worker<br/>[Container: Go]<br/>books shipments"]:::container
    db[("Orders DB<br/>[Database: Postgres]")]:::db
  end
  carrier["Carrier<br/>[External system]"]:::external
  shopper -->|"uses<br/>[HTTPS]"| web
  web -->|"places orders<br/>[JSON/HTTPS]"| api
  api -->|"reads and writes<br/>[SQL]"| db
  api -.->|"OrderPlaced<br/>[NATS]"| worker
  worker -->|"books<br/>[REST]"| carrier
  class shop boundary
  classDef person fill:#08427b,stroke:#052e56,color:#fff
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef external fill:#8a8a8a,stroke:#5e5e5e,color:#fff
  classDef db fill:#438dd5,stroke:#2e6295,color:#fff
  classDef boundary fill:none,stroke:#8a8a8a,stroke-dasharray:5 5,color:#444
```

The Orders API never calls the carrier; the dotted message to the worker is
the only bridge.

### C4 L3 components

```mermaid
flowchart LR
  web["Storefront<br/>[Container]"]:::container
  subgraph api["Orders API [Container: Go]"]
    handler["Order handler<br/>[Component: HTTP]<br/>validates requests"]:::component
    orders["Order service<br/>[Component]<br/>order rules"]:::component
    repo["Order store<br/>[Component: port]<br/>loads and saves orders"]:::component
    events["Event publisher<br/>[Component: port]"]:::component
  end
  db[("Orders DB<br/>[Database]")]:::db
  web -->|"POST /orders"| handler
  handler --> orders
  orders --> repo
  orders --> events
  repo -->|"SQL"| db
  class api boundary
  classDef container fill:#438dd5,stroke:#2e6295,color:#fff
  classDef component fill:#85bbf0,stroke:#5d82a8,color:#000
  classDef db fill:#438dd5,stroke:#2e6295,color:#fff
  classDef boundary fill:none,stroke:#8a8a8a,stroke-dasharray:5 5,color:#444
```

The order rules depend on two ports and nothing else, which is what makes
them testable without a database.

### Sequence

```mermaid
sequenceDiagram
  actor shopper as Shopper
  participant api as Orders API
  participant pay as Payment provider
  participant db as Orders DB
  shopper->>api: place order
  api->>db: save order (pending)
  api->>pay: charge card
  alt charge succeeds
    pay-->>api: charged
    api->>db: mark paid
    api-->>shopper: order confirmed
  else card declined
    pay-->>api: declined
    api-->>shopper: ask for another card
  end
```

The order is saved before the charge, so a crash mid-charge leaves a pending
order to reconcile, never a charge with no order.

### State

```mermaid
stateDiagram-v2
  [*] --> pending
  pending --> paid: charge succeeds
  pending --> cancelled: shopper cancels
  paid --> shipped: carrier collects
  paid --> refunded: shopper cancels
  shipped --> [*]
  cancelled --> [*]
  refunded --> [*]
```

Cancelling means two different things depending on whether money has moved.

### Data (ER)

```mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : places
  ORDER ||--|{ ORDER_LINE : contains
  PRODUCT ||--o{ ORDER_LINE : "appears on"
  ORDER {
    uuid id PK
    uuid customer_id FK
    string status
    int total_cents
  }
  ORDER_LINE {
    uuid order_id FK
    uuid product_id FK
    int quantity
    int price_cents
  }
```

The line keeps its own price, so changing a product's price never rewrites an
old order.

### Ports (class diagram, sparingly)

```mermaid
classDiagram
  class OrderStore {
    <<interface>>
    +Load(id) Order
    +Save(order) error
  }
  class EventPublisher {
    <<interface>>
    +Publish(event) error
  }
  class OrderService {
    +Place(cmd) Order
  }
  OrderService --> OrderStore
  OrderService --> EventPublisher
```

Two ports, both owned by the service; adapters implement them, nothing else
does.

### Options pair

Inside an options block (see [SKILL.md](SKILL.md) step 5), each option gets a
diagram at the same zoom with the same ids for shared things:

````markdown
<!-- options: order-events -->
### Option A: API publishes directly
```mermaid
flowchart LR
  api["Orders API"] --> db[("Orders DB")]
  api --> bus["Message bus"]
```
Simple; an event can be lost if the API dies between the save and the publish.

### Option B: outbox table
```mermaid
flowchart LR
  api["Orders API"] --> db[("Orders DB")]
  relay["Outbox relay"] --> db
  relay --> bus["Message bus"]
```
No lost events; one more process to run.
<!-- /options -->
````

### Before and after

One diagram, changed parts marked with a class, for a PR body:

```mermaid
flowchart LR
  api["Orders API"] --> db[("Orders DB")]
  api -. "removed" .-> bus["Message bus"]
  relay["Outbox relay"]:::added --> db
  relay -->|"publishes"| bus
  classDef added fill:#d4f4dd,stroke:#2e7d32,color:#000
  linkStyle 1 stroke:#c62828,stroke-dasharray:4 4
```

The API no longer talks to the bus; the new relay (green) does.
