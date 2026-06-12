# Tutorial Step Format

Each step in the tutorial follows this exact structure:

## Step Template

```
## Step N: <behavior name in plain language>

### What you're building

<2–4 sentences explaining what this step adds and WHY. Connect it to the
feature's purpose. Explain what the test will verify at the behavior level,
not the code level.>

### RED: Write the failing test

Open `<filename>` and type the following test:

```<language>
<complete test function — never a partial snippet>
```

Run the tests:

```bash
<test command>
```

Expected output:
```
<exact failure message, e.g.: FAIL: cannot find symbol 'Checkout'>
```

The test fails because <one sentence: the thing you haven't built yet>.

### GREEN: Make it pass

Open `<filename>` and type the following:

```<language>
<minimal implementation — only what this test needs>
```

Run the tests again:

```bash
<test command>
```

Expected output:
```
<passing output, e.g.: PASS: 1 test passed>
```

### Understanding check

> Why did we use <X> instead of <Y> here?
> What would break if we wrote <Z> instead?
```

---

## Good Step

**Good**: The explanation leads with purpose, not mechanism. The test block is complete. The implementation is minimal. The understanding check probes the decision made.

```markdown
## Step 2: User can add an item to the cart

### What you're building

A cart that starts empty and can hold items. The key behavior here is that
adding an item changes what the cart contains — this is the fundamental
"write" operation everything else builds on.

### RED: Write the failing test

Open `cart_test.py` and type:

```python
def test_add_item_to_cart():
    cart = Cart()
    cart.add(Item("apple", price=1.50))
    assert cart.item_count() == 1
```

Run: `pytest cart_test.py`

Expected:
```
FAILED: NameError: name 'Cart' is not defined
```

The test fails because `Cart` doesn't exist yet.

### GREEN: Make it pass

Create `cart.py` and type:

```python
class Cart:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def item_count(self):
        return len(self._items)
```

Run: `pytest cart_test.py`

Expected:
```
PASSED
```

### Understanding check

> Why does `add` return nothing? What would change if it returned `self`?
```

---

## Bad Step

**Bad**: Explanation describes code, not behavior. Implementation is speculative. Code block is a diff fragment.

```markdown
## Step 2: Cart class

We need to implement the Cart class with a list to store items and methods
to add items and count them.

Type this in cart.py:

```python
# Add this to the existing Cart class
def add(self, item):
    self._items.append(item)
```

The test should pass now.
```

Red flags in the bad step:
- Explanation says "implement... with a list" — describes implementation, not behavior
- "Add this to the existing Cart class" implies partial snippet without full context
- No expected failure shown before implementation
- No expected pass output
- No understanding check
- "Should pass now" — vague
- Speculative implementation added without a failing test driving it
