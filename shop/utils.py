import re

_OFFER_PIECES_RE = re.compile(r"^\s*[xX]\s*(\d+)\s*$")


def parse_offer_pieces(value):
    if not value:
        return None
    match = _OFFER_PIECES_RE.match(str(value))
    if not match:
        return None
    return int(match.group(1))


def cart_item_offer_pieces(item):
    attribute = getattr(item, "attribute", None)
    if attribute is None:
        return None
    offer = getattr(attribute, "offer", None)
    if offer is None:
        return None
    pieces = parse_offer_pieces(getattr(offer, "title", None))
    if pieces is not None:
        return pieces
    return parse_offer_pieces(getattr(attribute, "label", None))
