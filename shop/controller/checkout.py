from django.shortcuts import redirect, render
from django.contrib import messages
from shop.models import *
from django.http import HttpResponse, JsonResponse

import random


def placeorder(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        neworder.name = request.POST.get('name')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.number = request.POST.get('number')
        neworder.status= 'Pending'
        neworder.message= request.POST.get('order_comments')
        
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        enable_shipping = 1
        count = 0
        for item in cart:
            count = count + 1
            if count >= 2:
                enable_shipping = 0

            elif item.product.free_shipping == 1:
                enable_shipping = 0

            cart_total_price = cart_total_price + item.product.sale_price * item.product_qty

        neworder.shipping = enable_shipping
        neworder.total_price = cart_total_price
        trackno = 'id-'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'id-'+str(random.randint(1111111,9999999))

        neworder.tracking_no = trackno

        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                price = item.product.sale_price,
                quantity = item.product_qty,

            )
            # decrease product stock ?

        Cart.objects.filter(user=request.user).delete()

        messages.success(request, "Your order has been placed successfully")
        return redirect('thank-you-view', slug=neworder.tracking_no)

    return redirect('/')
