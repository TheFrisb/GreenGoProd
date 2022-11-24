from django.shortcuts import redirect, render
from django.contrib import messages
from shop.models import Product, CartItems, Cart
from django.http import HttpResponse, JsonResponse

def addtocart(request):
    if request.method == 'POST':
        if Cart.objects.filter(session = request.session['nonuser']):
            CartHolder = Cart.objects.get(session = request.session['nonuser'])
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(CartItems.objects.filter(cart = CartHolder, product_id=prod_id)):
                    print('CART FOUND')
                    prod_qty = int(request.POST.get('product_qty'))
                    cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder)
                    cartItem.product_qty = cartItem.product_qty + prod_qty
                    cartItem.save()
                    return JsonResponse({'status': "Product added with quantity saved"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    # Check Stock
                    # if product.check .quantity >= prod_qty: Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                    
                    CartItems.objects.create(cart = CartHolder, product_id=prod_id, product_qty=prod_qty)

                    return JsonResponse({'status': "Product added successfuly"})

            else:
                return JsonResponse({'status': "No such product found"})

        else:
            return JsonResponse({'status': "Login to continue"})



    return redirect('/')


def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        CartHolder = Cart.objects.get(session = request.session['nonuser'])
        if(CartItems.objects.filter(cart = CartHolder, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder)
            cartItem.product_qty = prod_qty
            cartItem.save()
            return JsonResponse({'status': "Updated Successfully!"})
    return redirect('/')


def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        CartHolder = Cart.objects.get(session = request.session['nonuser'])
        if(CartItems.objects.filter(cart = CartHolder, product_id=prod_id)): # check for inspect element kidz
            cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder)
            cartItem.delete()
        return JsonResponse({'status': "Updated Successfully!"})
    return redirect('/')