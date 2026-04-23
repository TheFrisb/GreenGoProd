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
