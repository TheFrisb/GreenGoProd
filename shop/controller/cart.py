from django.shortcuts import redirect, render
from django.contrib import messages
from shop.models import Product, CartItems, Cart, CheckoutFees, CartFees, ProductAttribute
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
                    print('cartItem product: ', cartItem.product)
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



def variableaddtocart(request):
    if request.method == 'POST':
        if Cart.objects.filter(session = request.session['nonuser']):
            CartHolder = Cart.objects.get(session = request.session['nonuser'])
            prod_id = int(request.POST.get('product_id'))
            prod_attr = int(request.POST.get('attribute_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check and product_check.status=='VARIABLE'):
                if(CartItems.objects.filter(cart = CartHolder, product_id=prod_id, attribute_id = prod_attr)):
                    print('Product', product_check, 'is already in cart!')
                    prod_qty = int(request.POST.get('product_qty'))
                    cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder, attribute_id = prod_attr)
                    cartItem.product_qty = cartItem.product_qty + prod_qty
                    cartItem.save()
                else:
                    print("Else")
                    prod_qty = int(request.POST.get('product_qty'))
                    newattribute = ProductAttribute.objects.get(id=prod_attr)
                    attributeprice = newattribute.price
                    CartItems.objects.create(cart = CartHolder, product_id=prod_id, product_qty = prod_qty, attribute = newattribute, attributename = ' - ' + newattribute.checkattribute, attributeprice = attributeprice)
                    print('New product with attribute added to cart')
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
        print(prod_attr)
        CartHolder = Cart.objects.get(session = request.session['nonuser'])
        if(CartItems.objects.filter(cart = CartHolder, product_id=prod_id)):
            if(prod_attr > 0):
                cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder, attribute_id = prod_attr)
                print(prod_attr)
                cartItem.delete()
            else:
                cartItem = CartItems.objects.get(product_id=prod_id, cart = CartHolder, attribute = None)
                print('cartItem product: ', cartItem.product)
                cartItem.delete()
        return JsonResponse({'status': "Updated Successfully!"})
    return redirect('/')


def addordeletefee(request):
    if request.method == 'POST':
        print('Fee initiated')
        if Cart.objects.filter(session = request.session['nonuser']):
            CartHolder = Cart.objects.get(session = request.session['nonuser'])
            print('Cart fee Found')
            fee_id = int(request.POST.get('fee_id'))
            action = str(request.POST.get('action'))        
            if(CheckoutFees.objects.filter(id=fee_id)):
                print('Check for fee')
                FeeHolder = CheckoutFees.objects.get(id=fee_id)
                print('FeeHolder found: ', FeeHolder)
                if(CartFees.objects.filter(cart=CartHolder, fee=FeeHolder)):
                    CartFee = CartFees.objects.get(cart=CartHolder, fee=FeeHolder)
                    CartFee.delete()
                    print('Fee deleted from cart!')
                else:
                    CartFee = CartFees.objects.create(cart = CartHolder, fee = FeeHolder, title = FeeHolder.title, price = FeeHolder.price)
                    print('Fee: ', CartFee, ' added to cart!')
                    return JsonResponse({'status': "Fee added successfuly"})
            else:
                return JsonResponse({'status': "No such fee found"})




    return redirect('/')

