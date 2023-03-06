from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import json
from django.http import HttpResponse, JsonResponse
from .facebook_api import daily_spend
from datetime import datetime, timedelta
from shop.models import Product
import requests
import logging
from decouple import config


logger = logging.getLogger(__file__)


@login_required
def daily_ad_spend(request):
    daily_item = daily_items.objects.filter().first()
    daily_rows = daily_row.objects.filter(owner=daily_item).order_by('created_at')
    total_quantity = 0
    total_ad_spend = 0
    total_profit = 0
    total_cpp = 0
    total_roas = 0
    total_roi = 0
    yesterday_row = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_row_2 = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    search_options = daily_row.objects.filter(created_at__date = yesterday_row).order_by('-owner__id')
    search_options2 = daily_items.objects.all().order_by('-id')
    if(daily_rows):
        for row in daily_rows:
            total_quantity += row.quantity
            total_ad_spend += row.ad_cost
            total_profit += row.profit
            total_cpp += row.cost_per_purchase
            total_roas += row.roas
            total_roi += row.roi
        number_of_rows = daily_rows.count()
        total_cpp = total_cpp / number_of_rows
        total_roas = total_roas / number_of_rows
        total_roi = total_roi / number_of_rows
    

    context = {
        'daily_item': daily_item,
        'daily_rows': daily_rows,
        'search_options': search_options,
        'search_options2': search_options2,
        'total_quantity': total_quantity,
        'total_ad_spend':  total_ad_spend,
        'total_profit':  total_profit,
        'total_cpp':  total_cpp,
        'total_roas':  total_roas,
        'total_roi':  total_roi,
    }
    return render(request, 'analytics/daily_ad_spend.html', context)


def daily_ad_spend_by_id(request, pk):
    daily_item = daily_items.objects.get(slug=pk)
    daily_rows = daily_row.objects.filter(owner=daily_item).order_by('created_at')
    total_quantity = 0
    total_ad_spend = 0
    total_profit = 0
    total_cpp = 0
    total_roas = 0
    total_roi = 0
    yesterday_row = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_row_2 = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    search_options = daily_row.objects.filter(created_at__date = yesterday_row).order_by('-owner__id')
    search_options2 = daily_items.objects.all().order_by('-id')
    if(daily_rows):
        for row in daily_rows:
            total_quantity += row.quantity
            total_ad_spend += row.ad_cost
            total_profit += row.profit
            total_cpp += row.cost_per_purchase
            total_roas += row.roas
            total_roi += row.roi
        number_of_rows = daily_rows.count()
        total_cpp = total_cpp / number_of_rows
        total_roas = total_roas / number_of_rows
        total_roi = total_roi / number_of_rows
    

    context = {
        'daily_item': daily_item,
        'daily_rows': daily_rows,
        'search_options': search_options,
        'search_options2': search_options2,
        'total_quantity': total_quantity,
        'total_ad_spend':  total_ad_spend,
        'total_profit':  total_profit,
        'total_cpp':  total_cpp,
        'total_roas':  total_roas,
        'total_roi':  total_roi,
    }
    return render(request, 'analytics/daily_ad_spend.html', context)



def user_login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("daily_ad_spend")
    else:
        if request.method =='POST':
            name = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=name, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("daily_ad_spend")
            else:
                messages.error(request, "Invalid username or Password")
                return redirect('/')
        return render(request, "analytics/login.html")
        
    

def index(request):
    if request.user.is_authenticated:
        return redirect('daily_ad_spend')
    else:
        return redirect('login')
    


def add_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        id = request.POST.get('id')
        print(comment, id)
        daily_rw = daily_row.objects.get(id = id)

        daily_rw.comment = comment
        daily_rw.save()
        return JsonResponse({'status': "Added comment successfully"})
    else:
        return JsonResponse({'status': "Unsuccessfully comment"})
        pass



def add_old_row(request):
    if request.method == 'POST':
        owner_id = int(request.POST.get('owner'))
        ad_spend = float(request.POST.get('ad_spend'))
        date = request.POST.get('date')
        quantity = int(request.POST.get('quantity'))
        print(owner_id)
        owner = daily_items.objects.get(id=owner_id)
        product = owner.product
        
        product_price = product.sale_price - 100
        stock_price = product.supplier_stock_price
        fixed_cost = 0

        neto_price = product_price - stock_price
        yesterdays_ad_spend = ad_spend
        neto_total = quantity * neto_price
        print(neto_total, quantity, yesterdays_ad_spend)
        profit = neto_total - yesterdays_ad_spend

        if quantity != 0:
            cost_per_purchase = yesterdays_ad_spend / quantity
        else:
            cost_per_purchase = yesterdays_ad_spend
        be_roas = product_price / neto_price
        if yesterdays_ad_spend != 0:
            roas = (quantity * product_price) / yesterdays_ad_spend
            roi = (neto_price * quantity) / yesterdays_ad_spend
        else:
            roas = (quantity * product_price)
            roi = (neto_price * quantity)
        daily_row_new = daily_row(owner=owner, quantity=quantity, price=product_price, stock_price=stock_price, fixed_cost=fixed_cost,
                                ad_cost=yesterdays_ad_spend,neto_price=neto_price, neto_total=neto_total, profit=profit, cost_per_purchase = cost_per_purchase,
                                be_roas = be_roas, roas=roas, roi=roi, created_at=date)
        daily_row_new.save()
        print('Created')
        return JsonResponse({'status': "Created older row successfuly"})
    else: 
        return JsonResponse({'status': "Unsuccessful older row creation"})


# def add_old_row(request):
#     if request.method == 'POST':
#         owner_id = int(request.POST.get('owner'))
#         ad_spend = float(request.POST.get('ad_spend'))
#         date = request.POST.get('date')
#         quantity = int(request.POST.get('quantity'))
#         owner = daily_items.objects.get(id=owner_id)
#         product = owner.product
        
#         row = daily_row.objects.filter(created_at__date=date).first()
#         if(row):
#             print('Row found!')
#             row.ad_cost = ad_spend
#             row.save()
#             return JsonResponse({'status': "Created older row successfuly"})

#         else:
#             print('Row not found!')
#             product_price = product.sale_price
#             stock_price = product.supplier_stock_price
#             fixed_cost = 84

#             neto_price = product_price - stock_price - fixed_cost
#             yesterdays_ad_spend = ad_spend
#             neto_total = quantity * neto_price
#             print(neto_total, quantity, yesterdays_ad_spend)
#             profit = neto_total - yesterdays_ad_spend

#             if quantity != 0:
#                 cost_per_purchase = yesterdays_ad_spend / quantity
#             else:
#                 cost_per_purchase = yesterdays_ad_spend
#             be_roas = product_price / neto_price
#             if yesterdays_ad_spend != 0:
#                 roas = (quantity * product_price) / yesterdays_ad_spend
#                 roi = (neto_price * quantity) / yesterdays_ad_spend
#             else:
#                 roas = (quantity * product_price)
#                 roi = (neto_price * quantity)
#             daily_row_new = daily_row(owner=owner, quantity=quantity, price=product_price, stock_price=stock_price, fixed_cost=fixed_cost,
#                                     ad_cost=yesterdays_ad_spend,neto_price=neto_price, neto_total=neto_total, profit=profit, cost_per_purchase = cost_per_purchase,
#                                     be_roas = be_roas, roas=roas, roi=roi, created_at=date)
#             daily_row_new.save()
#             print('Created')
#             return JsonResponse({'status': "Created older row successfuly"})
#     else: 
#         return JsonResponse({'status': "Unsuccessful older row creation"})


def retrieve_adspend(request):
    if request.method == 'GET':
        date_1 = request.GET.get('date_from'),
        date_2 = request.GET.get('date_till'),
        date_from = date_1[0]
        date_till = date_2[0]
        
        print(date_from, date_till)

        access_token = config('MARKETING_API_SECRET_KEY')
        ad_account_id = config('MARKETING_AD_ACCOUNT')

        url = f'https://graph.facebook.com/v16.0/{ad_account_id}/insights'
        params = {
            'level': 'account',
            'time_range': f"{{'since':'{date_from}','until':'{date_till}'}}",
            'fields': 'spend',
            'access_token': access_token,
            'filtering': '[{"field":"campaign.name","operator":"CONTAIN", "value":"(MK"}]'
            
        }   
        response = requests.get(url, params=params)
        response_json = response.json()
        total_spend = float(response_json['data'][0]['spend'])
        
        

        return JsonResponse({'USD_Val': str(total_spend)})
        print(date_from, ' ', date_till)

    else:
        return JsonResponse({'status': 'Wrong request!'})

    
   
