from django.shortcuts import redirect, render
from django.contrib import messages
from shop.models import Product, CartItems, Cart, CheckoutFees, CartFees, ProductAttribute
from django.http import HttpResponse, JsonResponse
from facebook_business.adobjects.event import Event
from facebook_business.api import FacebookAdsApi
import time

FacebookAdsApi.init(access_token='EAAEBgQEZCiHkBAAPhGXJZBgZAYgvk4fUZAzlvkYHhY6mXG2465FwckOyJZCH7CpHG1CPgWYHtCsMl9SIycZBiBn6MlZClOowT8qWWQsDcGL8HZCAc1yKsusOCZCFo8yZARzc3bg6AuJsgEGftU1Ap5Jz1cH3mfuQKwSV1M6vn5atiVvyHb41ZAmCibW')
account_id = '3944984375629692'


def addtocart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(session = request.session['nonuser'])
        if cart:
            CartHolder = Cart.objects.get(session = request.session['nonuser'])
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(CartItems.objects.filter(cart = CartHolder, product_id=prod_id)):
                    prod_qty = int(request.POST.get('product_qty'))
                    cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder)
                    cartItem.product_qty = cartItem.product_qty + prod_qty
                    cartItem.save()
                    return JsonResponse({'status': "Product added with quantity saved"})
                else:
                    # Check Stock
                    # if product.check .quantity >= prod_qty: Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                    prod_qty = int(request.POST.get('product_qty'))
                    CartItems.objects.create(cart = CartHolder, product_id=prod_id, product_qty=prod_qty)
                   
                    return JsonResponse({'status': "Product added successfuly"})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('/')


def offeraddtocart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(session = request.session['nonuser'])
        if cart:
            CartHolder = Cart.objects.get(session = request.session['nonuser'])
            prod_id = int(request.POST.get('product_id'))
            offer_price = int(request.POST.get('product_price'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(CartItems.objects.filter(cart = CartHolder, product_id=prod_id)):
                    prod_qty = int(request.POST.get('product_qty'))
                    cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder, offer_price = offer_price)
                    cartItem.product_qty = cartItem.product_qty + prod_qty
                    cartItem.save()
                    return JsonResponse({'status': "Product added with quantity saved"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    CartItems.objects.create(cart = CartHolder, product_id=prod_id, product_qty=prod_qty, offer_price=offer_price)
                    return JsonResponse({'status': "Product added successfuly"})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('/')


def variableaddtocart(request):
    if request.method == 'POST':
        CartHolder = Cart.objects.get(session = request.session['nonuser'])
        if CartHolder:  
            prod_id = int(request.POST.get('product_id'))
            prod_attr = int(request.POST.get('attribute_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check and product_check.status=='VARIABLE'):
                if(CartItems.objects.filter(cart = CartHolder, product_id=prod_id, attribute_id = prod_attr)):
                    prod_qty = int(request.POST.get('product_qty'))
                    cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder, attribute_id = prod_attr)
                    cartItem.product_qty = cartItem.product_qty + prod_qty
                    cartItem.save()
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    newattribute = ProductAttribute.objects.get(id=prod_attr)
                    attributeprice = newattribute.price
                    CartItems.objects.create(cart = CartHolder, product_id=prod_id, product_qty = prod_qty, attribute = newattribute, attributename = ' - ' + newattribute.checkattribute, attributeprice = attributeprice)
                    return JsonResponse({'status': "Product added successfuly"})

            else:
                return JsonResponse({'status': "Product not found!"})
        else:
                return JsonResponse({'status': "Cart does not exist!"})

    return redirect('/')

def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        prod_attr = int(request.POST.get('attribute_id'))
        CartHolder = Cart.objects.get(session = request.session['nonuser'])
        if(CartItems.objects.filter(cart = CartHolder, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            if(prod_attr > 0):
                cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder, attribute_id = prod_attr)
                cartItem.product_qty = prod_qty
                cartItem.save()
            else:
                cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder)
                cartItem.product_qty = prod_qty
                cartItem.save()
            return JsonResponse({'status': "Updated Successfully!"})
    return redirect('/')


def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        prod_attr = int(request.POST.get('attribute_id'))
        CartHolder = Cart.objects.get(session = request.session['nonuser'])
        if(CartItems.objects.filter(cart = CartHolder, product_id=prod_id)):
            if(prod_attr > 0):
                cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder, attribute_id = prod_attr)
                cartItem.delete()
            else:
                cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder, attribute = None)
                cartItem.delete()
        return JsonResponse({'status': "Updated Successfully!"})
    return redirect('/')


def addordeletefee(request):
    if request.method == 'POST':
        CartHolder = Cart.objects.get(session = request.session['nonuser'])
        if CartHolder:
            fee_id = int(request.POST.get('fee_id'))
            action = str(request.POST.get('action'))   
            FeeHolder = CheckoutFees.objects.get(id=fee_id)     
            if FeeHolder:
                try:
                    CartFee = CartFees.objects.get(cart=CartHolder, fee=FeeHolder)
                except:
                    CartFee = None
                if CartFee:             
                    CartFee.delete()
                else:
                    CartFee = CartFees.objects.create(cart = CartHolder, fee = FeeHolder, title = FeeHolder.title, price = FeeHolder.price)
                    return JsonResponse({'status': "Fee added successfuly"})
            else:
                return JsonResponse({'status': "No such fee found"})
    return redirect('/')
