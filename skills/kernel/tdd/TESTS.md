# Good tests, bad tests

The tests `tdd` writes are the spec that outlives the story. They should break
when behaviour breaks and only then.

## Test behaviour at seams

A seam is a place where you can observe behaviour without reaching inside: a
port, an HTTP handler, a CLI entry point, a module's public functions. Stories
name the seam for each test in the TDD plan.

Good:

```python
def test_Cart_AddingSameItemTwice_IncrementsQuantity():
    cart = Cart()
    cart.add("apple")
    cart.add("apple")
    assert cart.quantity_of("apple") == 2
```

Bad:

```python
def test_cart_add():
    cart = Cart()
    cart.add("apple")
    cart.add("apple")
    assert cart._items == {"apple": 2}   # private state: breaks on any refactor
```

The bad test pins the data structure. Change the dict to a list of line items
and it fails while the behaviour is unchanged. That is a test that punishes
refactoring, which is the step TDD depends on.

## One assertion idea per test

Good: one idea, possibly several asserts.

```go
func TestOrder_PaidCart_HasTotalAndLines(t *testing.T) {
    order := checkout(cartWith("apple", "pear"))
    if order.Total != 350 { t.Fatalf("total = %d", order.Total) }
    if len(order.Lines) != 2 { t.Fatalf("lines = %d", len(order.Lines)) }
}
```

Bad: a scenario test that checks creation, discount, tax, and email in one go.
When it fails, the name tells you nothing; split it.

## Names

`Subject_Condition_Outcome`, in glossary terms:

- `Shelf_StockBelowThreshold_AppearsInWeeklyAsk`
- `Checkout_ExpiredCard_RejectsWithoutCreatingOrder`

Not `test1`, `testHappyPath`, or `ShelfRepositoryImpl_findById_works`. Adapt
casing to the language (`test_shelf_stock_below_threshold_appears_in_weekly_ask`
in Python, `it("appears in the weekly ask when stock is below threshold")`
inside `describe("Shelf")` in JS), keeping the three parts.

## Fakes at ports, no mocking what you own

The outside world sits behind ports: the database, the clock, the payment API,
the mailer. For tests, give each port an in-memory fake that honours its
contract, and share the fake across tests.

```ts
class FakeClock implements Clock {
  constructor(private now: Date) {}
  current() { return this.now; }
  advance(ms: number) { this.now = new Date(this.now.getTime() + ms); }
}
```

Do not mock your own classes. If `Checkout` uses `PriceList`, test `Checkout`
with a real `PriceList`. Mocks of your own code assert on calls rather than
outcomes, and they freeze the internal design in place. When a real
collaborator is too awkward to build in a test, that is design feedback: the
seam is in the wrong place.

Mocks are fine for one thing: asserting that a message was sent across a port
when sending it *is* the behaviour (an email went out). Even then, a fake that
records what it received usually reads better.

## Seeing the red

A red that comes from a compile error, a missing import, or a typo in the test
tells you nothing. Before writing production code, make the failure say what
the test is about:

```text
AssertionError: expected quantity_of("apple") == 2, got 1
```

To get there, add the empty function or type first so the test compiles, then
watch the assertion fail.

## Smells

- A test that needs ten lines of setup: the subject has too many collaborators.
- A test that changes every time you refactor: it is testing internals.
- A test that never failed: you did not see the red, so you do not know it can.
- A test with sleeps: inject the clock.
- Tests that pass alone and fail together: shared state; give each test its own.
