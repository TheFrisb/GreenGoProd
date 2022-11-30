from .models import Cart, Category, CartItems, CartOffers
import uuid

def cart_renderer(request):
    try:
        cart = Cart.objects.get(session=request.session['nonuser'])
    except:
        request.session['nonuser'] = str(uuid.uuid4())
        cart = Cart.objects.create(session=request.session['nonuser'])
        

    return {
        'cart': cart
    }


def extras(request):
    categories = Category.objects.filter(published=True)
    cartItems = CartItems.objects.filter(cart__session=request.session['nonuser'])
    itemscount = 0
    free_shipping = False
    cartOffers = CartOffers.objects.all()
    if cartOffers:
        for offer in cartOffers:
            for item in cartItems:
                if(offer.product.title == item.product.title ):
                    offer.is_added = True
    total = 0
    if cartItems:
        for item in cartItems:
            if(item.product.free_shipping == True):
                free_shipping = True
            if(item.attributeprice is not None):
                total = total + (item.attributeprice * item.product_qty)
                itemscount = itemscount + item.product_qty
            else:
                total = total + (item.product.sale_price * item.product_qty)
                itemscount = itemscount + item.product_qty
    if(itemscount >= 2):
        free_shipping = True
    return {'categories': categories, 'cart': cartItems, 'cart_total': total, 'cartOffers': cartOffers, 'itemscount': itemscount, 'free_shipping': free_shipping}
    