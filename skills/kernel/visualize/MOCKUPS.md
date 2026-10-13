# Mockups

A mockup shows where things sit on one screen. It does not decide behaviour.
The canonical record is the Mermaid screen flow in the requirements or story;
each screen in it links to one HTML sidecar. If the mockup and the story
disagree about what happens, the story wins and the mockup gets fixed.

## The contract

- **Path:** `docs/planning/<slug>/mockups/<screen-slug>.html`. One file per
  screen, kebab-case, named after the screen's glossary term.
- **Self-contained:** one file, the CSS kit below inline in a `<style>`
  block, no scripts, no images, no web fonts, no external links.
- **Low fidelity:** grayscale boxes, system font, no brand colors or logos.
  Real labels, taken from `GLOSSARY.md`, and realistic sample data
  ("Ada Lovelace, 3 items, $42.00"), never lorem ipsum.
- **Header comment:** the first thing in the file names the story and the
  screen-flow node id it renders:

```html
<!-- mockup: payment
     story: 01-02 Shopper pays for the basket
     flow: docs/planning/checkout/requirements.md, node id "payment" -->
```

- **Notes:** questions and assumptions go in `.note` callouts on the screen
  itself, next to the thing they are about.

## Linking from the screen flow

The node id in the flowchart is the screen slug's id; `click` points at the
file, relative to the markdown that holds the diagram:

```text
flowchart LR
  basket["Basket"] --> payment["Payment"]
  click basket "mockups/basket.html"
  click payment "mockups/payment.html"
```

GitHub ignores `click`; the viewer opens the mockup in a framed preview. Also
list the links in prose under the caption so a plain markdown reader can
follow them: `Mockups: [Basket](mockups/basket.html), [Payment](mockups/payment.html).`

## The CSS kit

Use these classes and nothing else. If a screen needs something the kit
cannot show, a `.note` saying so is better than new CSS.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Payment (mockup)</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 24px; background: #f2f2f2; color: #222;
         font: 15px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif; }
  .screen { max-width: 420px; margin: 0 auto; background: #fff;
            border: 2px solid #444; border-radius: 10px; overflow: hidden; }
  .screen.wide { max-width: 960px; }
  .bar { display: flex; align-items: center; justify-content: space-between;
         gap: 12px; padding: 12px 16px; background: #ddd;
         border-bottom: 1px solid #999; font-weight: 600; }
  .panel { padding: 16px; border-bottom: 1px solid #ddd; }
  .panel h2 { margin: 0 0 8px; font-size: 16px; }
  .row { display: flex; gap: 12px; align-items: center; }
  .row > * { flex: 1; }
  .btn { display: inline-block; padding: 10px 16px; border: 2px solid #444;
         border-radius: 6px; background: #fff; font-weight: 600;
         text-align: center; }
  .btn.primary { background: #444; color: #fff; }
  .field { display: block; margin: 0 0 12px; }
  .field > span { display: block; font-size: 13px; color: #555;
                  margin-bottom: 4px; }
  .field > div { border: 1px solid #888; border-radius: 4px;
                 padding: 8px 10px; min-height: 38px; background: #fafafa; }
  .field.error > div { border: 2px solid #222; }
  .list { list-style: none; margin: 0; padding: 0; }
  .list li { display: flex; justify-content: space-between; gap: 12px;
             padding: 10px 0; border-bottom: 1px dashed #bbb; }
  .muted { color: #777; font-size: 13px; }
  .box { background: #e6e6e6; border: 1px dashed #999; border-radius: 4px;
         min-height: 80px; display: grid; place-items: center; color: #777; }
  .note { margin: 12px 0; padding: 8px 10px; background: #fffbe6;
          border-left: 4px solid #b59f00; font-size: 13px; }
  .note::before { content: "Note: "; font-weight: 700; }
</style>
</head>
<body>
<!-- mockup: payment
     story: 01-02 Shopper pays for the basket
     flow: docs/planning/checkout/requirements.md, node id "payment" -->
<div class="screen">
  <div class="bar"><span>Payment</span><span class="muted">Step 3 of 3</span></div>
  <div class="panel">
    <h2>Basket total</h2>
    <ul class="list">
      <li><span>Blue mug x2</span><span>$24.00</span></li>
      <li><span>Delivery</span><span>$4.00</span></li>
      <li><strong>Total</strong><strong>$28.00</strong></li>
    </ul>
  </div>
  <div class="panel">
    <label class="field"><span>Card number</span><div>4242 4242 4242 4242</div></label>
    <div class="row">
      <label class="field"><span>Expiry</span><div>12 / 28</div></label>
      <label class="field"><span>CVC</span><div>123</div></label>
    </div>
    <p class="note">On a declined card we stay on this screen; see the screen flow.</p>
  </div>
  <div class="panel row">
    <span class="btn">Back</span><span class="btn primary">Pay $28.00</span>
  </div>
</div>
</body>
</html>
```

`.screen.wide` is for desktop layouts; `.box` stands in for any chart, map, or
image. `.field.error` marks a field in its error state.

## Process

1. Draw or update the screen flow first and validate it.
2. Write one mockup per screen node that the story touches, from the kit.
3. Open it in the viewer (or a browser) and look at it at phone width.
4. Ask the user what is wrong with the screen, not whether they like it.
