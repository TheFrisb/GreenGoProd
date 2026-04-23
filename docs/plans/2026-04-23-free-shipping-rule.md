# Free Shipping Rule Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Free shipping qualifies only when the cart has 2+ distinct `CartItems` rows, or any item's `product.free_shipping` is `True`. Quantity alone no longer qualifies.

**Architecture:** One helper in `shop/utils.py`, called from `shop/context_processors.py::extras` (UI display) and `shop/controller/checkout.py::placeorder` (order creation). Each `CartItems` row is already keyed by `(cart, product_id, attribute_id, offer_price)`, so counting rows gives the "different products or variants" semantics for free.

**Tech Stack:** Django 4.1+, Python stdlib `unittest` via `manage.py test` (no pytest in this project).

**Design doc:** `docs/plans/2026-04-23-free-shipping-rule-design.md`

---

## Pre-flight

Run this once before starting; it confirms the dev environment is wired up.

```
python manage.py test shop -v 2 2>&1 | tail -20
```

Expected: either "Ran 0 tests" (OK — `shop/tests.py` is empty) or an existing green suite. If it errors on DB / settings, fix that first — do not proceed.

---

### Task 1: Write failing unit tests for the helper

**Files:**
- Modify: `shop/tests.py` (currently empty — add a fresh test module).

**Step 1: Write the failing tests**

Replace the contents of `shop/tests.py` with:

```python
from types import SimpleNamespace
from unittest import TestCase

from shop.utils import cart_qualifies_for_free_shipping


def _item(free_shipping=False):
    """Minimal stand-in for a CartItems row used by the shipping helper."""
    return SimpleNamespace(product=SimpleNamespace(free_shipping=free_shipping))


class CartQualifiesForFreeShippingTests(TestCase):
    def test_empty_cart_does_not_qualify(self):
        self.assertFalse(cart_qualifies_for_free_shipping([]))

    def test_single_item_without_flag_does_not_qualify(self):
        self.assertFalse(cart_qualifies_for_free_shipping([_item()]))

    def test_single_item_with_free_shipping_flag_qualifies(self):
        self.assertTrue(cart_qualifies_for_free_shipping([_item(free_shipping=True)]))

    def test_two_distinct_items_qualify(self):
        self.assertTrue(cart_qualifies_for_free_shipping([_item(), _item()]))

    def test_three_items_qualify(self):
        self.assertTrue(
            cart_qualifies_for_free_shipping([_item(), _item(), _item()])
        )

    def test_one_flagged_plus_one_unflagged_qualifies(self):
        self.assertTrue(
            cart_qualifies_for_free_shipping([_item(free_shipping=True), _item()])
        )
```

Use `unittest.TestCase` (not `django.test.TestCase`) — the helper is pure Python with no DB access, so we skip test-DB setup entirely.

**Step 2: Run tests, verify they fail**

```
python manage.py test shop.tests.CartQualifiesForFreeShippingTests -v 2
```

Expected: `ImportError: cannot import name 'cart_qualifies_for_free_shipping' from 'shop.utils'`. All six tests should error out on import.

If any test passes, something is already wired up — stop and investigate before continuing.

**Step 3: Do not commit yet** — Tasks 1 and 2 commit together once the tests go green.

---

### Task 2: Implement the helper

**Files:**
- Modify: `shop/utils.py`

**Step 1: Add the helper**

Append to `shop/utils.py` (keep everything already there):

```python
def cart_qualifies_for_free_shipping(cart_items):
    """
    True if the cart earns free shipping.

    Qualifies when any item's product.free_shipping is True, or when the
    cart has two or more distinct CartItems rows. Each row already
    represents a unique (product, attribute, offer_price) slot, so a
    single product with product_qty >= 2 stays one row and does not
    qualify.
    """
    count = 0
    for item in cart_items:
        if item.product.free_shipping:
            return True
        count += 1
        if count >= 2:
            return True
    return False
```

Short-circuiting on the flag and on `count >= 2` means we can stop iterating early in the common case.

**Step 2: Run tests, verify they pass**

```
python manage.py test shop.tests.CartQualifiesForFreeShippingTests -v 2
```

Expected: `Ran 6 tests in 0.00Xs — OK`.

**Step 3: Commit**

```
git add shop/utils.py shop/tests.py
git commit -m "feat: add cart_qualifies_for_free_shipping helper

Two distinct cart rows (or any product flagged free_shipping) now
qualify. Quantity alone does not.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Verify then remove `cart_item_offer_pieces`

**Files:**
- Modify: `shop/utils.py`

**Step 1: Confirm the only remaining callers are the two shipping spots**

```
grep -rn "cart_item_offer_pieces" shop GreenGoShop 2>/dev/null
```

Expected output lists exactly four lines:
- `shop/utils.py:15:def cart_item_offer_pieces(item):`
- `shop/context_processors.py:4:from .utils import cart_item_offer_pieces`
- `shop/context_processors.py:63:            pieces = cart_item_offer_pieces(item)`
- `shop/controller/checkout.py:8:from shop.utils import cart_item_offer_pieces`
- `shop/controller/checkout.py:43:            pieces = cart_item_offer_pieces(item)`

If any other file references it, **stop** and re-read the design — our removal plan is wrong.

**Step 2: Also confirm `parse_offer_pieces` is still needed**

```
grep -rn "parse_offer_pieces" shop GreenGoShop 2>/dev/null
```

Expected: `shop/services.py` imports and calls it in `_get_stock_multiplier`. Keep `parse_offer_pieces`.

**Step 3: Do not delete `cart_item_offer_pieces` yet**

It still has two callers (context_processors.py and controller/checkout.py). We'll delete the callers first in Tasks 4 and 5, then delete the function in Task 6.

**Step 4: No commit yet.**

---

### Task 4: Rewire `shop/context_processors.py::extras`

**Files:**
- Modify: `shop/context_processors.py`

**Step 1: Replace the free-shipping calculation**

Starting file reads (for reference — this is how it looks today):

```python
from .utils import cart_item_offer_pieces
...
def extras(request):
    cartItems = CartItems.objects.filter(
        cart__session=request.session["nonuser"]
    ).order_by("-date_added")
    itemscount = 0
    free_shipping = False
    ...
    if cartItems:
        for item in cartItems:
            if item.attributeprice is not None:
                total = total + (item.attributeprice * item.product_qty)
                itemscount = itemscount + item.product_qty
                if item.product.free_shipping == True:
                    free_shipping = True
            elif item.offer_price is not None:
                total = total + (item.offer_price * item.product_qty)
                itemscount = itemscount + item.product_qty
                if item.product.free_shipping == True:
                    free_shipping = True
            else:
                total = total + (item.product.sale_price * item.product_qty)
                itemscount = itemscount + item.product_qty
                if item.product.free_shipping == True:
                    free_shipping = True

            pieces = cart_item_offer_pieces(item)
            if pieces is not None and pieces >= 2:
                free_shipping = True
    if itemscount >= 2:
        free_shipping = True
```

Apply three edits:

**Edit 1 — swap the import (line 4):**

From:
```python
from .utils import cart_item_offer_pieces
```

To:
```python
from .utils import cart_qualifies_for_free_shipping
```

**Edit 2 — drop the three per-branch `if item.product.free_shipping == True: free_shipping = True` inside the loop, and drop the `pieces = cart_item_offer_pieces(item)` block.** After the edit, the inner loop reads:

```python
    if cartItems:
        for item in cartItems:
            if item.attributeprice is not None:
                total = total + (item.attributeprice * item.product_qty)
                itemscount = itemscount + item.product_qty
            elif item.offer_price is not None:
                total = total + (item.offer_price * item.product_qty)
                itemscount = itemscount + item.product_qty
            else:
                total = total + (item.product.sale_price * item.product_qty)
                itemscount = itemscount + item.product_qty
```

**Edit 3 — replace the post-loop `if itemscount >= 2: free_shipping = True` quantity rule with a single helper call:**

From:
```python
    if itemscount >= 2:
        free_shipping = True
```

To:
```python
    free_shipping = cart_qualifies_for_free_shipping(cartItems)
```

The earlier `free_shipping = False` initialization at the top stays; the helper just overwrites it (and if the cart is empty, we never iterate, so it remains `False` either way — the helper handles empty input).

**Step 2: Re-run the helper tests to confirm no regression from editing the same package**

```
python manage.py test shop.tests -v 2
```

Expected: `Ran 6 tests — OK`.

**Step 3: Syntax sanity check**

```
python -c "from shop import context_processors; print('ok')"
```

Expected: prints `ok`. If it errors on unresolved import or syntax, fix before moving on.

**Step 4: Commit**

```
git add shop/context_processors.py
git commit -m "refactor: use cart_qualifies_for_free_shipping in context processor

Removes the quantity-based rule and the offer-pieces exception.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Rewire `shop/controller/checkout.py::placeorder`

**Files:**
- Modify: `shop/controller/checkout.py`

**Step 1: Replace the shipping calculation**

Starting file reads (lines 8, 24–57):

```python
from shop.utils import cart_item_offer_pieces
...
def placeorder(request):
    if request.method == "POST":
        ...
        neworderitems = CartItems.objects.filter(cart=CartHolder)
        neworderfees = CartFees.objects.filter(cart=CartHolder)
        cart_total_price = 0
        countProducts = 0
        trackno = str(uuid.uuid4())
        qualifies_via_offer = False
        for item in neworderitems:
            if item.has_attributes == True:
                cart_total_price += item.attributeprice * item.product_qty
            elif item.has_offer == True:
                cart_total_price += item.offer_price * item.product_qty
            else:
                cart_total_price += item.product.sale_price * item.product_qty

            if item.product.free_shipping == True:
                countProducts += 5 + item.product_qty
            elif item.product.free_shipping == False:
                countProducts += item.product_qty

            pieces = cart_item_offer_pieces(item)
            if pieces is not None and pieces >= 2:
                qualifies_via_offer = True

        for fee in neworderfees:
            cart_total_price = cart_total_price + fee.price
        neworder.subtotal_price = cart_total_price
        if countProducts >= 2 or qualifies_via_offer:
            neworder.shipping = False
            neworder.total_price = cart_total_price
        elif countProducts == 1:
            neworder.total_price = cart_total_price + neworder.shipping_price
            neworder.shipping = True
        else:
            neworder.total_price = cart_total_price
```

Apply three edits:

**Edit 1 — swap the import (line 8):**

From:
```python
from shop.utils import cart_item_offer_pieces
```

To:
```python
from shop.utils import cart_qualifies_for_free_shipping
```

**Edit 2 — remove `countProducts = 0` and `qualifies_via_offer = False` from the initializers, strip the free-shipping-boost and offer-pieces branches inside the loop.** After the edit, the loop reads:

```python
        neworderitems = CartItems.objects.filter(cart=CartHolder)
        neworderfees = CartFees.objects.filter(cart=CartHolder)
        cart_total_price = 0
        trackno = str(uuid.uuid4())
        for item in neworderitems:
            if item.has_attributes == True:
                cart_total_price += item.attributeprice * item.product_qty
            elif item.has_offer == True:
                cart_total_price += item.offer_price * item.product_qty
            else:
                cart_total_price += item.product.sale_price * item.product_qty

        for fee in neworderfees:
            cart_total_price = cart_total_price + fee.price
        neworder.subtotal_price = cart_total_price
```

**Edit 3 — replace the three-branch shipping decision with a two-branch one keyed off the helper:**

From:
```python
        if countProducts >= 2 or qualifies_via_offer:
            neworder.shipping = False
            neworder.total_price = cart_total_price
        elif countProducts == 1:
            neworder.total_price = cart_total_price + neworder.shipping_price
            neworder.shipping = True
        else:
            neworder.total_price = cart_total_price
```

To:
```python
        if cart_qualifies_for_free_shipping(neworderitems):
            neworder.shipping = False
            neworder.total_price = cart_total_price
        else:
            neworder.shipping = True
            neworder.total_price = cart_total_price + neworder.shipping_price
```

The `neworderitems` queryset is re-evaluated by `cart_qualifies_for_free_shipping`, but Django caches queryset results after the first iteration, so this is not an extra DB hit.

**Step 2: Run the full shop test suite**

```
python manage.py test shop -v 2
```

Expected: 6 tests, all OK.

**Step 3: Syntax sanity check**

```
python -c "from shop.controller import checkout; print('ok')"
```

Expected: prints `ok`.

**Step 4: Commit**

```
git add shop/controller/checkout.py
git commit -m "refactor: use cart_qualifies_for_free_shipping in placeorder

Removes the +5 product-flag boost and offer-pieces branches; collapses
the three-way shipping decision into a single helper call.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Remove the now-dead `cart_item_offer_pieces` helper

**Files:**
- Modify: `shop/utils.py`

**Step 1: Confirm zero remaining references**

```
grep -rn "cart_item_offer_pieces" shop GreenGoShop 2>/dev/null
```

Expected: only `shop/utils.py:def cart_item_offer_pieces(item):` (the definition). If anything else appears, **stop** — a caller was missed.

**Step 2: Delete the function**

In `shop/utils.py`, remove the `cart_item_offer_pieces` function body (and the blank line before it). Keep `parse_offer_pieces` and `_OFFER_PIECES_RE` — `shop/services.py::_get_stock_multiplier` still needs them.

**Step 3: Verify**

```
python manage.py test shop -v 2
python -c "from shop.utils import parse_offer_pieces; from shop.services import ExportOrdersService; print('ok')" 2>&1 | tail -3
```

Expected: tests green, and the sanity import prints `ok` (proves `parse_offer_pieces` survived and services.py still loads).

If the `ExportOrdersService` name doesn't exist, substitute the real class name from `shop/services.py` — just import *something* from that module to prove it still parses.

**Step 4: Commit**

```
git add shop/utils.py
git commit -m "chore: remove unused cart_item_offer_pieces helper

All call sites were migrated to cart_qualifies_for_free_shipping.
parse_offer_pieces stays; services.py still uses it for stock math.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: Manual smoke test

Code can't see the UI, so we validate by interacting with the running app. Do **not** skip this; the unit tests only cover the pure helper.

**Step 1: Start the dev server**

```
python manage.py runserver
```

Expected: "Starting development server at http://127.0.0.1:8000/". Leave it running in another terminal / background.

**Step 2: Run the scenarios in a browser (session cookies keep the cart)**

| # | Setup | Click | Expected result |
|---|---|---|---|
| 1 | Empty cart. Add one normal product with qty=5 on its product page. | Open `/checkout` and watch the shipping row. | Shipping line shows the 190-den price — **not** "бесплатна достава". |
| 2 | From #1, add a second distinct product. | Refresh `/checkout`. | Shipping line flips to "бесплатна достава". |
| 3 | Clear cart. Add a variable product and pick variant A (qty 1). Then add variant B of the same product (qty 1). | Open `/checkout`. | Shows "бесплатна достава" — two rows in `CartItems`. |
| 4 | Clear cart. In the admin, set `Product.free_shipping=True` on some test product. Add one of it, qty=1. | Open `/checkout`. | Shows "бесплатна достава" — flag path. Remember to unset after. |
| 5 | Clear cart. Add a product whose variants include an OFFER attribute titled `x2` or `x3`. Pick that variant only (qty 1). | Open `/checkout`. | Shows the 190-den shipping line — **not** free. This is the deliberately-removed behavior from the old `cart_item_offer_pieces` rule. |
| 6 | From scenario 2, submit the order form. | Open the resulting `Order` in admin. | `shipping=False`, `total_price == subtotal_price`, shipping_price not added. |
| 7 | From scenario 1 (one product, qty=5), submit the order. | Admin. | `shipping=True`, `total_price == subtotal_price + shipping_price`. |

If any row fails, do not proceed — re-read the failing task's diff and fix before the next step.

**Step 3: Stop the dev server** (Ctrl-C).

**Step 4: Record the outcome**

Reply with a short note listing which of the 7 scenarios passed. If they all passed, the feature is verified.

---

### Task 8: Final review and wrap-up

**Step 1: Check the commit stack**

```
git log --oneline origin/main..HEAD
```

Expected (on `extrapopust` branch, assuming it's ahead of main): one design-doc commit plus four feature commits in order:

1. `docs: design for distinct-items free-shipping rule`
2. `feat: add cart_qualifies_for_free_shipping helper`
3. `refactor: use cart_qualifies_for_free_shipping in context processor`
4. `refactor: use cart_qualifies_for_free_shipping in placeorder`
5. `chore: remove unused cart_item_offer_pieces helper`

**Step 2: Diff review**

```
git diff origin/main..HEAD -- shop/
```

Skim for surprises. Things to confirm:

- `shop/utils.py` still exports `parse_offer_pieces`.
- `shop/context_processors.py` loop no longer touches `item.product.free_shipping` or calls `cart_item_offer_pieces`.
- `shop/controller/checkout.py::placeorder` no longer uses `countProducts` or `qualifies_via_offer`.
- No stray `cart_item_offer_pieces` references anywhere.

**Step 3: Final full test run**

```
python manage.py test shop -v 2
```

Expected: all green.

**Step 4: Report done**

Write a summary of what shipped: new helper + 3 edit sites + dead-code removal + 7/7 smoke scenarios passing.

---

## Notes for the implementing engineer

- **No migration needed.** `Product.free_shipping` stays on the model; only the logic that consumes it changed.
- **Keep `parse_offer_pieces`** — `shop/services.py::_get_stock_multiplier` still depends on it for the export pipeline. Only `cart_item_offer_pieces` is being deleted.
- **Django tests** run via `python manage.py test`, not `pytest`. The project has no pytest dependency.
- **Queryset re-iteration**: `cartItems` in `extras` and `neworderitems` in `placeorder` are each iterated once before the helper call, then handed to the helper. Django caches queryset results after first iteration, so the helper's re-iteration doesn't re-hit the DB.
- **Templates unchanged.** `free_shipping` and `itemscount` context variables still surface; only `free_shipping`'s computation rule moved.
