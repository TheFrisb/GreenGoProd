from django.shortcuts import redirect, render
from django.contrib import messages
from shop.models import Product, Cart
from django.http import HttpResponse, JsonResponse

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    prod_qty = int(request.POST.get('product_qty'))
                    cart = Cart.objects.get(product_id=prod_id, user=request.user)
                    cart.product_qty = cart.product_qty + prod_qty
                    cart.save()
                    return JsonResponse({'status': "Product added with quantity saved"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    # Check Stock
                    # if product.check .quantity >= prod_qty: Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                    
                    Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)

                    return JsonResponse({'status': "Product added successfuly"})

            else:
                return JsonResponse({'status': "No such product found"})

        else:
            return JsonResponse({'status': "Login to continue"})



    return redirect('/')


def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status': "Updated Successfully!"})
    return redirect('/')


def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)): # check for inspect element kidz
            cartItem = Cart.objects.get(product_id=prod_id, user=request.user)
            cartItem.delete()
        return JsonResponse({'status': "Updated Successfully!"})
    return redirect('/')