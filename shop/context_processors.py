import uuid

from .models import Cart, CartFees, CartItems, CartOffers, CheckoutFees, Category
from .utils import cart_qualifies_for_free_shipping


def cart_renderer(request):
    try:
        cart = Cart.objects.get(session=request.session["nonuser"])
    except:
        request.session["nonuser"] = str(uuid.uuid4())
        cart = Cart.objects.create(session=request.session["nonuser"])

    return {"cart": cart}


def extras(request):
    cartItems = CartItems.objects.filter(
        cart__session=request.session["nonuser"]
    ).order_by("-date_added")
    itemscount = 0
    cartOffers = CartOffers.objects.all()
    if cartOffers:
        for offer in cartOffers:
            for item in cartItems:
                if offer.product == item.product:
                    offer.is_added = True
    total = 0
    try:
        cartFees = CartFees.objects.filter(cart__session=request.session["nonuser"])
    except:
        cartFees = None
    orderFees = CheckoutFees.objects.all()

    feetotal = 0
    for orderfee in orderFees:
        for cartfee in cartFees or []:
            if orderfee == cartfee.fee:
                orderfee.is_added = True
                feetotal += cartfee.price
                if cartfee.is_free:
                    orderfee.is_free = True

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
    free_shipping = cart_qualifies_for_free_shipping(cartItems)
    return {
        "cart": cartItems,
        "cart_total": total,
        "cartOffers": cartOffers,
        "itemscount": itemscount,
        "free_shipping": free_shipping,
        "orderFees": orderFees,
        "cartFees": cartFees,
        "feetotal": feetotal,
        "categories": Category.objects.filter(published=True).order_by("sort_order")
    }
