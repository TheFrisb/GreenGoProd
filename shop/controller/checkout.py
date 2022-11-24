from django.shortcuts import redirect, render
from django.contrib import messages
from shop.models import *
from django.http import HttpResponse, JsonResponse

import random


def placeorder(request):
    if request.method == 'POST':
        CartHolder = Cart.objects.get(session = request.session['nonuser'])
        neworder = Order()
        neworder.user = request.session['nonuser']
        neworder.name = request.POST.get('name')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.number = request.POST.get('number')
        neworder.status= 'Pending'
        neworder.message= request.POST.get('order_comments')

        neworderitems = CartItems.objects.filter(cart=CartHolder)
        neworderfees = CartFees.objects.filter(cart=CartHolder)
        cart_total_price = 0
        enable_shipping = 1
        countProducts = 0
        neworder.shipping = enable_shipping
        
        trackno = 'id-'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'id-'+str(random.randint(1111111,9999999))

        for item in neworderitems:
            cart_total_price = cart_total_price + item.product.sale_price * item.product_qty
            if(item.product.free_shipping == True):
                countProducts = countProducts + 5
            else:
                countProducts = countProducts + 1



        for fee in neworderfees:
                cart_total_price = cart_total_price + fee.price

        if countProducts >= 2:
            enable_shipping = 0

        if(enable_shipping == 1):
            neworder.total_price = cart_total_price + neworder.shipping_price
        else:
            neworder.total_price = cart_total_price
        neworder.tracking_no = trackno
        neworder.save()

        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                price = item.product.sale_price,
                quantity = item.product_qty,

            )
            

        
        for fee in neworderfees:
            OrderFeesItem.objects.create(
                order = neworder,
                fee = fee.fee,
                title = fee.title,
                price = fee.price
            )




            # decrease product stock ?
        CartFees.objects.filter(cart=CartHolder).delete()
        CartItems.objects.filter(cart=CartHolder).delete()
        Cart.objects.filter(session = request.session['nonuser']).delete()
        del request.session['nonuser']

        messages.success(request, "Your order has been placed successfully")
        return redirect('thank-you-view', slug=neworder.tracking_no)

    return redirect('/')



def addtoorder(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        product = Product.objects.get(id=request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        order = Order.objects.get(id = request.POST.get('order_id'))
        if order:
            orderItem = OrderItem.objects.get(order = order, product = product)
            if(orderItem):
                orderItem.quantity = orderItem.quantity + product_qty
                orderItem.price = orderItem.price + product.sale_price
                orderItem.save()
                if(order.shipping == True):
                    order.shipping = False
                    order.total_price = order.total_price + (product.sale_price * product_qty) - order.shipping_price
                else:
                    order.shipping = False
                    order.total_price = order.total_price + (product.sale_price * product_qty)

                order.save()
            return JsonResponse({'status': "Product added successfully"})

    return redirect('/')