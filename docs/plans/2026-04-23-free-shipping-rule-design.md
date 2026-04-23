# Free shipping rule: require 2+ distinct cart items

## Goal

A cart qualifies for free shipping **only** when it contains at least two different products or variants, or when any item in it is a product the admin has marked `free_shipping=True`. Quantity of a single product (or single variant) never qualifies on its own.

## Today's behavior

Free shipping is computed in two places:

- `shop/context_processors.py::extras` — drives the banner/badge visible in the cart, header, and checkout page.
- `shop/controller/checkout.py::placeorder` — sets `Order.shipping` and `Order.total_price` when the customer submits the order.

Both grant free shipping if **any** of the following hold:

1. Any item's `product.free_shipping` is `True`.
2. Any item has an `OFFER` attribute whose title parses as `"x2"`, `"x3"`, etc. (via `shop/utils.py::cart_item_offer_pieces`).
3. Sum of `product_qty` across items is `>= 2` (`itemscount >= 2` in the context processor; `countProducts >= 2` in `placeorder`, with a `+5` boost per `free_shipping` product that skews the count).

Rule 3 is the bug: a single product with `product_qty=2` currently gets free shipping, which contradicts the desired behavior.

## New rule

A helper `cart_qualifies_for_free_shipping(cart_items)` in `shop/utils.py`. Returns `True` iff:

- any item's `product.free_shipping` is `True`, **or**
- `len(cart_items) >= 2`.

### Why counting rows is correct

Each `CartItems` row represents a unique slot keyed by `(cart, product_id, attribute_id, offer_price)`. The add-to-cart controllers enforce this:

- `addtocart` (normal product): filters `(cart, product_id)` before create; same product merges qty into the existing row.
- `variableaddtocart`: filters `(cart, product_id, attribute_id)`; different variants create separate rows, same variant merges qty.
- `offeraddtocart`: filters `(cart, product_id)` then gets by `offer_price`; different offer prices can create separate rows.
- `add_upsell_to_cart`: a separate row per upsell.

Therefore:

| Cart shape | `len(cart_items)` | Free shipping? |
|---|---|---|
| empty | 0 | no |
| 1 product, any qty, not flagged | 1 | no |
| 1 product, any qty, `free_shipping=True` | 1 | yes (via flag) |
| 2 distinct products | 2 | yes |
| 2 variants of one variable product | 2 | yes |
| 1 product + 1 upsell | 2 | yes |
| 1 offer attribute titled `"x2"` | 1 | no |

## Scope of change

### `shop/utils.py`

- Add `cart_qualifies_for_free_shipping(cart_items)`.
- Remove `cart_item_offer_pieces` — only called from the two shipping call sites (both being rewritten).
- Keep `parse_offer_pieces` — `shop/services.py::_get_stock_multiplier` still uses it for export stock math.

### `shop/context_processors.py::extras`

- Drop the three per-branch `if item.product.free_shipping == True: free_shipping = True` assignments inside the existing total/count loop.
- Drop the `pieces = cart_item_offer_pieces(item)` check at the bottom of that loop.
- Drop the post-loop `if itemscount >= 2: free_shipping = True` quantity rule.
- After the loop, call `free_shipping = cart_qualifies_for_free_shipping(cartItems)` once.
- Drop the `from .utils import cart_item_offer_pieces` import; add `cart_qualifies_for_free_shipping`.
- `itemscount` (sum of `product_qty`) stays — still used for the cart badge count.

### `shop/controller/checkout.py::placeorder`

- Drop `countProducts`, `qualifies_via_offer`, the `+5` boost hack, the `cart_item_offer_pieces` call, and the three-branch `if countProducts >= 2 … elif countProducts == 1 … else` shipping decision.
- Replace with:
  ```python
  if cart_qualifies_for_free_shipping(neworderitems):
      neworder.shipping = False
      neworder.total_price = cart_total_price
  else:
      neworder.shipping = True
      neworder.total_price = cart_total_price + neworder.shipping_price
  ```
- Drop the `from shop.utils import cart_item_offer_pieces` import.

### Templates and model

No change. `Order.shipping_price` (default 190) and the `Product.free_shipping` boolean stay. The templates read the `free_shipping` context variable unchanged.

## Verification

Manual smoke on the running dev server:

1. Add one normal product with qty 5 — checkout footer should show the 190-den shipping line (not "бесплатна достава").
2. Add a second distinct product — shipping line should flip to "бесплатна достава".
3. Remove one product, leaving a single variable product with two variants added — free shipping should remain on.
4. Empty the cart, add a product whose `free_shipping=True` flag is set — free shipping on with just one line.
5. Place one of the above orders; confirm `Order.shipping`, `Order.total_price`, and `Order.shipping_price` match what the banner showed.

Each verification step must be evidenced (screenshot or explicit confirmation) before claiming complete.

## Out of scope

- `addtoorder` (thank-you-page upsell) flips `order.shipping = False` unconditionally once it fires. That's a separate code path and not part of this change.
- The `Product.free_shipping` admin flag stays; no migration.
- `parse_offer_pieces` stays; unrelated to shipping.
