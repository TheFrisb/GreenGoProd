from .models import Cart, Category, CartItems
import uuid

def cart_renderer(request):
    try:
        cart = Cart.objects.get(session = request.session['nonuser'])
    except:
        request.session['nonuser'] = str(uuid.uuid4())
        cart = Cart.objects.create(session = request.session['nonuser'])
        

    return {
        'cart': cart
    }


def extras(request):
    categories = Category.objects.all()
    cartItems = CartItems.objects.filter(cart__session = request.session['nonuser'])
    total = 0
    if cartItems:
        for item in cartItems:
            total = total + (item.product.sale_price * item.product_qty)

    return {'categories': categories, 'cart': cartItems, 'cart_total': total}