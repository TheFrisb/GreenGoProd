from django.shortcuts import redirect, render
from django.contrib import messages
from shop.models import *
from django.http import HttpResponse, JsonResponse
import datetime
import random
from . import facebook_pixel

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
        countProducts = 0
        trackno = 'id-'+str(random.randint(1111111,9999999))
        for item in neworderitems:
            if item.has_attributes == True:
                cart_total_price += item.attributeprice * item.product_qty
            elif item.has_offer == True:
                cart_total_price += item.offer_price * item.product_qty
            else:
                cart_total_price += item.product.sale_price * item.product_qty
                
            if(item.product.free_shipping == True):
                countProducts += 5 + item.product_qty
            elif(item.product.free_shipping == False):
                countProducts += item.product_qty
            
                
        for fee in neworderfees:
                cart_total_price = cart_total_price + fee.price
        neworder.subtotal_price = cart_total_price
        if countProducts >= 2:
            neworder.shipping = False

        if(countProducts == 1):
            neworder.total_price = cart_total_price + neworder.shipping_price + 20 #provizija
            neworder.shipping = True
        else:
            neworder.total_price = cart_total_price + 20 #provizija
        neworder.tracking_no = trackno
        neworder.save()
        for item in neworderitems:
            if (item.has_attributes==True):
                item_label = item.product.sku + ' ' + item.attribute.label
                OrderItem.objects.create(
                order = neworder,
                product = item.product,
                attribute_name = item.attribute.checkattribute,
                price = item.attributeprice,
                quantity = item.product_qty,
                label = item_label,
                supplier = item.product.supplier,
                attribute_price = item.attributeprice,
            )
            elif(item.has_offer==True):
                OrderItem.objects.create(
                    order = neworder,
                    product = item.product,
                    price = item.offer_price,
                    quantity = item.product_qty,
                    label = item.product.sku,
                    supplier = item.product.supplier,
                    is_cart_offer = True,
                )
            else:
                OrderItem.objects.create(
                    order = neworder,
                    product = item.product,
                    price = item.product.sale_price,
                    quantity = item.product_qty,
                    label = item.product.sku,
                    supplier = item.product.supplier,
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
        try:
            facebook_pixel.PurchaseEvent(request=request, order_items=neworderitems, order_total=neworder.total_price, number=str(request.POST.get('number')).lower(), city=str(request.POST.get('city')).lower(), name=str(request.POST.get('name')).lower())
        except:
            pass
        return redirect('thank-you-view', slug=neworder.tracking_no)
    return redirect('/')


def addtoorder(request):
    if request.method != 'POST':
        return redirect('/')
    
    product = Product.objects.get(id=request.POST.get('product_id'))
    product_qty = int(request.POST.get('product_qty'))
    order = Order.objects.get(id = request.POST.get('order_id'))
    if order:
        orderItem = OrderItem.objects.filter(order = order, product = product).first();
        if(orderItem):
            if orderItem.attribute_price is not None:
                
                OrderItem.objects.create(
                    order = orderItem.order,
                    product = orderItem.product,
                    price = orderItem.attribute_price - orderItem.attribute_price * 20 // 100,
                    quantity = 1,
                    label = orderItem.label,
                    supplier = orderItem.product.supplier,
                    attribute_name = orderItem.attribute_name,
                    is_thankyou_offer = True,
                )
                if(order.shipping == True):
                    order.shipping = False
                    order.subtotal_price = order.subtotal_price + (orderItem.attribute_price - orderItem.attribute_price * 20 // 100)
                    order.total_price = order.total_price + (orderItem.attribute_price - orderItem.attribute_price * 20 // 100) - order.shipping_price
                else:
                    order.shipping = False
                    order.subtotal_price = order.subtotal_price + (orderItem.attribute_price - orderItem.attribute_price * 20 // 100)
                    order.total_price = order.total_price + (orderItem.attribute_price - orderItem.attribute_price * 20 // 100)

            else:
                OrderItem.objects.create(
                    order = orderItem.order,
                    product = orderItem.product,
                    price = orderItem.product.sale_price - orderItem.product.sale_price * 20 // 100,
                    quantity = 1,
                    label = orderItem.product.sku,
                    supplier = orderItem.product.supplier,
                    is_thankyou_offer = True,
                )
                if(order.shipping == True):
                    order.shipping = False
                    order.subtotal_price = order.subtotal_price + (orderItem.product.sale_price - orderItem.product.sale_price * 20 // 100)
                    order.total_price = order.total_price + (orderItem.product.sale_price - orderItem.product.sale_price * 20 // 100) - order.shipping_price
                else:
                    order.shipping = False
                    order.subtotal_price = order.total_price + (orderItem.product.sale_price - orderItem.product.sale_price * 20 // 100)
                    order.total_price = order.total_price + (orderItem.product.sale_price - orderItem.product.sale_price * 20 // 100)

            order.save()
        return JsonResponse({'status': "Product added successfully"})

    return redirect('/')
    
