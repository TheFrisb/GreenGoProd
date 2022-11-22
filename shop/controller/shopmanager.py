from django.shortcuts import redirect, render
from django.contrib import messages
from shop.models import *
from django.http import HttpResponse, JsonResponse


def updateOrderStatus(request):
    
    if request.method == 'POST':
        
        order_id = int(request.POST.get('orderId'))
        action = str(request.POST.get('action'))
        print(order_id, ' - ', action)
        if(Order.objects.filter(id=order_id)):
            
            order = Order.objects.get(id = order_id)
            
            if action == 'confirm':
                order.status = 'Confirmed'
                order.save()
                return JsonResponse({'status': "Order Confirmed and Saved"})
            if action == 'delete':
                order.status = 'Deleted'
                order.save()
                return JsonResponse({'status': "Order Removed and Saved"})
            if action == 'return':
                order.status = 'Pending'
                order.save()
                return JsonResponse({'status': "Order is Pending and Saved"})

    return redirect('/')
            