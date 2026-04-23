import re

_OFFER_PIECES_RE = re.compile(r"^\s*[xX]\s*(\d+)\s*$")


def parse_offer_pieces(value):
    if not value:
        return None
    match = _OFFER_PIECES_RE.match(str(value))
    if not match:
        return None
    return int(match.group(1))


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
