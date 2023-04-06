import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from shop.models import Product, product_campaigns
import json
from django.http import HttpResponse, JsonResponse
from .facebook_api import daily_spend, ad_campaigns
from datetime import datetime, timedelta
from shop.models import Product
import requests
import logging
from decouple import config
from moviepy.video.io.VideoFileClip import VideoFileClip
import random
from django.conf import settings
from PIL import Image
from io import BytesIO
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

    
   
def create_new_ad(request):
    context={
        'products': Product.objects.filter(status__in=['PUBLISHED', 'VARIABLE']),
    }
    print('yeah')
    #ad_campaigns.create_ad_campaign()
    return render(request, 'analytics/create_new_ad.html', context)


def get_product(request):
    if request.method == 'GET':
        #get product id from request
        product_id = request.GET.get('product_id')
        
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'url': product.get_absolute_url(),
            'thumbnail': product.thumbnail.url,
            'title': product.title,
            'regular_price': product.regular_price,
            'sale_price': product.sale_price,
            'label': product.sku
            })
    else:
        print('whoops')
        return redirect('/')



def upload_campaign_photo(request):
    if request.method == 'POST':
        ad_image = request.FILES['ad_image']
        ad_image_name = ad_image.name
        
        # date_today = datetime.now().strftime('%Y/%m/%d')
        # print(date_today)
        # check_path = os.path.join(settings.MEDIA_ROOT, 'campaigns/ads/ad_images/{date_today}/{ad_image_name}'.format(
        #     date_today=date_today,
        #     ad_image_name=ad_image_name
        # ))
        # if os.path.exists(check_path):
        #     media_url = os.path.relpath(check_path, settings.MEDIA_ROOT)
        #     image_url = os.path.join(settings.MEDIA_URL, media_url)
        #     print('EXISTS')
        #     return JsonResponse({ 'image_url': image_url})

        # get current time in hours, minutes and seconds as a string
        file_extension = ad_image.name.split('.')[-1]
        current_time = datetime.now().strftime('%H%M%S')
        new_file_name = ad_image_name + '_' + current_time + '.' + file_extension
        # save the image to the media folder
        new_ad = ad.objects.create(main_image=ad_image)
        new_ad.save()
        print(new_ad.main_image.url)
        return JsonResponse({ 'image_url': new_ad.main_image.url, 'image_id': new_ad.id })
    else:
        return redirect('/')


def upload_campaign_video(request):
    if request.method == 'POST':
        ad_video = request.FILES['ad_video']
        ad_video_name = ad_video.name
        # get current time in hours, minutes and seconds as a string
        file_extension = ad_video.name.split('.')[-1]
        current_time = datetime.now().strftime('%H%M%S')
        new_file_name = ad_video_name + '_' + current_time + '.' + file_extension
        # save the image to the media folder
        new_ad = ad.objects.create(main_video=ad_video)
        new_ad.save()
        

        return JsonResponse({
             'video_url': new_ad.main_video.url, 
             'video_id': new_ad.id,})
    else:
        return redirect('/')
    

def get_video_thumbnails(request):
    if request.method == 'GET':
        thumbnail_urls = []
        ad_id = int(request.GET.get('ad_id'))
        old_ad = ad.objects.get(id=ad_id)
        video_file_path = old_ad.main_video.path
        new_file_name = old_ad.video_filename.split('.')[0]
        with VideoFileClip(video_file_path) as video:
            video_width, video_height = video.size
            for i in range(6):
                thumbnail = video.get_frame(random.uniform(0, video.duration))
                thumbnail = Image.fromarray(thumbnail)
                thumbnail = thumbnail.resize((video_width, video_height))
                thumbnail_name = new_file_name + '_thumbnail_' + str(i+1) + '.png'
                thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'campaigns', 'ads', 'ad_videos', 'thumbnails', datetime.now().strftime('%Y/%m/%d'))
                thumbnail_path = os.path.join(thumbnail_dir, thumbnail_name)
                os.makedirs(thumbnail_dir, exist_ok=True)
                thumbnail.save(thumbnail_path, 'PNG')
                thumbnail_url = os.path.join(settings.MEDIA_URL, 'campaigns', 'ads', 'ad_videos', 'thumbnails', datetime.now().strftime('%Y/%m/%d'), thumbnail_name)
                thumbnail_urls.append(thumbnail_url)
        return JsonResponse({
                'thumbnail_urls': thumbnail_urls,
        })
    else:
        return redirect('/')

    
def generate_ad_video_thumbnail(request):
    if request.method == 'GET':
        ad_id = int(request.GET.get('ad_id'))
        current_time = float(request.GET.get('current_time'))
        old_ad = ad.objects.get(id=ad_id)
        video_file_path = old_ad.main_video.path
        new_file_name = old_ad.video_filename.split('.')[0]
        with VideoFileClip(video_file_path) as video:
            video_width, video_height = video.size
            thumbnail = video.get_frame(current_time)
            thumbnail = Image.fromarray(thumbnail)
            thumbnail = thumbnail.resize((video_width, video_height))
            thumbnail_name = new_file_name + '_thumbnail' + str(int(current_time)) + '.png'
            thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'campaigns', 'ads', 'ad_videos', 'thumbnails', datetime.now().strftime('%Y/%m/%d'))
            thumbnail_path = os.path.join(thumbnail_dir, thumbnail_name)
            os.makedirs(thumbnail_dir, exist_ok=True)
            thumbnail.save(thumbnail_path, 'PNG')
            thumbnail_url = os.path.join(settings.MEDIA_URL, 'campaigns', 'ads', 'ad_videos', 'thumbnails', datetime.now().strftime('%Y/%m/%d'), thumbnail_name)
        return JsonResponse({
                'thumbnail_url': thumbnail_url
        })
    else:
        return redirect('/')


def upload_video_thumbnail(request):
    if request.method == 'POST':
        ad_image = request.FILES['ad_image']
        new_ad = ad.objects.create(video_thumbnail=ad_image)
        new_ad.save()
        return JsonResponse({ 'image_url': new_ad.video_thumbnail.url})
    else:
        return redirect('/')



def search_ad_audiences(request):
    if request.method == 'GET':
        search_term = str(request.GET.get('search_term'))
        audiences = ad_campaigns.search_ad_interests(request, search_term)
        return JsonResponse({ 'audiences': audiences })
        

    else:
        return redirect('/')



def create_campaign(request):
    if request.method == 'POST':
        campaign_name = request.POST.get('campaign_name')
        product_id = request.POST.get('product_id')
        link_url = 'https://greengoshop.mk' + Product.objects.get(id=product_id).get_absolute_url()
        print(link_url)
        adsets = json.loads(request.POST.get('adsets'))
        
        
        campaign = ad_campaigns.create_facebook_campaign(campaign_name=campaign_name)
        campaign_id = campaign['id']
        print(campaign)
        


        for adset in adsets:
            adset_name = adset['adset_name']
            budget = int(adset['adset_budget'])
            min_age = int(adset['adset_minage'])
            max_age = int(adset['adset_maxage'])
            audience_id = adset['adset_audience_id']
            audience_name = adset['adset_audience_name']
            
            if "genders" in adset:
                genders = adset['genders']
            budget = budget * 100
            created_adset = ad_campaigns.create_facebook_adset(campaign_id=campaign_id, name=adset_name, budget=budget, max_age = max_age,
                                                       min_age = min_age, interest_id=audience_id, interest_name=audience_name)
            created_adset_id = created_adset['id']
            for ad in adset['ads']:
                ad_image = ''
                ad_video = ''
                ad_thumbnail = ''
                ad_name = ad['ad_name']
                ad_primary = ad['ad_primary_text']
                ad_headline = ad['ad_headline']
                ad_description = ad['ad_description']
                ad_type = ad['ad_type']

                if ad_type == 'photo':
                    ad_image = ad['ad_image_path']
                    created_ad = ad_campaigns.create_facebook_ad(ad_set_id=created_adset_id, ad_type='image', ad_name=ad_name,ad_primary_text=ad_primary,
                                                                 ad_description_text=ad_description, ad_headline_text=ad_headline, ad_image=ad_image, ad_link_url=link_url)
                    
                elif ad_type == 'video':
                    ad_video = ad['ad_video_path']
                    ad_thumbnail = ad['thumbnail_path']
                    print(ad_video, ad_thumbnail)
                    print('CREEATE AD CALLED')
                    created_ad = ad_campaigns.create_facebook_ad(ad_set_id=created_adset_id, ad_type='video', ad_name=ad_name,ad_primary_text=ad_primary,
                                                                 ad_description_text=ad_description, ad_headline_text=ad_headline, ad_video = ad_video, ad_thumbnail = ad_thumbnail, ad_link_url=link_url)



        return JsonResponse({ 'campaign_id': campaign_id })
    else:
        return redirect('/')
        


def save_new_campaign_id(request):
    if request.method == 'POST':
        campaign_id = str(request.POST.get('campaign_id'))
        prod_id = request.POST.get('product_id')
        product = Product.objects.get(id=prod_id)
        product_campaigns.objects.create(product=product, campaign_id=campaign_id)

        return JsonResponse({'success': 'success'})

    else:
        redirect('/')


def get_ad_preview(request):
    if request.method == 'GET':
        ad_primary_text = request.GET.get('ad_primary_text')
        ad_description_text = request.GET.get('ad_description_text')
        ad_headline_text = request.GET.get('ad_headline_text')
        photo_url = 'https://greengoshop.mk' + str(request.GET.get('photo_url'))

        result = ad_campaigns.create_ad_preview(ad_primary_text=ad_primary_text, ad_description_text=ad_description_text, ad_headline_text=ad_headline_text, photo_url=photo_url)
        return JsonResponse({'ad_preview': result})
    else:
        return JsonResponse({'status': 'Wrong request!'})

