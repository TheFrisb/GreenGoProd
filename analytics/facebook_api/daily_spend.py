from django.http import HttpResponse, JsonResponse
import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from datetime import datetime, timedelta
from analytics.models import *
from datetime import datetime
from shop.models import product_campaigns, Product
from decouple import config


def get_campaign_id():
    # Initialize the Facebook Ads SDK with the access token
    FacebookAdsApi.init(access_token=config('MARKETING_API_SECRET_KEY'))
    # Search for campaigns by string and ad account ID
    account = AdAccount(config('MARKETING_AD_ACCOUNT'))
    # campaigns = account.get_campaigns(fields=['name','id'], params={'limit':100})
    campaigns = account.get_campaigns(fields=['name','id','effective_status'], params={'effective_status':['ACTIVE']})
    # print(campaigns)
    # Iterate over all campaigns and find the first campaign that matches the search string
    for campaign in campaigns:
        campaign_id = campaign['id']
        campaign_obj = Campaign(campaign_id)
        # print(campaign_id, ' - ', campaign_obj, ' - ', campaign['name'])
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')

        insights = campaign_obj.get_insights(fields=['spend'],params={'date_preset': 'yesterday'})
        if insights:
            
            campaign_data = {'name': campaign['name'], 'id': campaign_id, 'spend': insights[0]['spend']}
            ad_spend = float(campaign_data['spend'])
            name_of_campaign = campaign['name']
            print(name_of_campaign)
            populate_daily_rows(name_of_campaign, ad_spend)

                

    return 'Campaign not found'



def populate_daily_rows(name_of_campaign, ad_spend):
    try:
        product_campaign_ob = product_campaigns.objects.get(title=name_of_campaign)
        campaigns_product = product_campaign_ob.product
        product_campaign = product_campaigns.objects.filter(product=campaigns_product)
        print('CAMPAIGN_OBJECT', product_campaign_ob, 'CAMPAIGN - PRODUCT', campaigns_product, 'PRODUCT_CAMPAIGN', product_campaign)


    except:
        return 1
    if product_campaign.count() == 1:

        product = product_campaign[0].product
        owner_of_campaign = daily_items.objects.filter(product=product).first()
        product_price = product.sale_price - 100
        stock_price = product.supplier_stock_price
        fixed_cost = 0
        quantity = 0
        print('CAMPAIGN FOUND, PRODUCT: ', product, 'OWNER: ', owner_of_campaign)
        yesterday = timezone.now() - timezone.timedelta(days=1)
        start_time = yesterday.replace(hour=0, minute=0, second=0)
        end_time = yesterday.replace(hour=23, minute=59, second=59)
        
        ordered_products = OrderItem.objects.filter(product=product, created_at__range=(start_time, end_time))
        print('ORDERED PRODUCTS: ', ordered_products)
        for product in ordered_products:
            quantity = quantity + product.quantity


        neto_price = product_price - stock_price
        yesterdays_ad_spend = ad_spend * 56.59
        neto_total = quantity * neto_price
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

     #  daily_row_new = daily_row(owner=owner_of_campaign, quantity=quantity, price=product_price, stock_price=stock_price, fixed_cost=fixed_cost,
       #                         ad_cost=yesterdays_ad_spend,neto_price=neto_price, neto_total=neto_total, profit=profit, cost_per_purchase = cost_per_purchase,
       #                         be_roas = be_roas, roas=roas, roi=roi, created_at=yesterday)
        
       # daily_row_new.save()
    
    elif product_campaign.count() > 1:
        yesterday_row = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        product = product_campaign[0].product
        owner_of_campaign = daily_items.objects.filter(product=product).first()
        row = daily_row.objects.filter(created_at__date=yesterday_row, owner=owner_of_campaign).first()

        if(row):

            row.ad_cost += ad_spend * 56.59

            row.save()

            return JsonResponse({'status': "Updated existing row for yesterday's date"})
        else:

            product = product_campaign[0].product
            owner_of_campaign = daily_items.objects.filter(product=product).first()
            product_price = product.sale_price - 100
            stock_price = product.supplier_stock_price
            fixed_cost = 0
            quantity = 0
            
            yesterday = timezone.now() - timezone.timedelta(days=1)
            start_time = yesterday.replace(hour=0, minute=0, second=0)
            end_time = yesterday.replace(hour=23, minute=59, second=59)
            
            ordered_products = OrderItem.objects.filter(product=product, created_at__range=(start_time, end_time))
            for product in ordered_products:
                print(product, ' - ', product.quantity, ' - ', product.created_at)
                quantity = quantity + product.quantity


            neto_price = product_price - stock_price

            yesterdays_ad_spend = ad_spend * 56.59

            neto_total = quantity * neto_price
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

         #   daily_row_new = daily_row(owner=owner_of_campaign, quantity=quantity, price=product_price, stock_price=stock_price, fixed_cost=fixed_cost,
                             #       ad_cost=yesterdays_ad_spend,neto_price=neto_price, neto_total=neto_total, profit=profit, cost_per_purchase = cost_per_purchase,
                             #       be_roas = be_roas, roas=roas, roi=roi, created_at=yesterday)
            
          #  daily_row_new.save()

        
    else:
        return 1
    return 1



def testing_get_campaign_id():
    # Initialize the Facebook Ads SDK with the access token
    FacebookAdsApi.init(access_token=config('MARKETING_API_SECRET_KEY'))
    # Search for campaigns by string and ad account ID
    account = AdAccount(config('MARKETING_AD_ACCOUNT'))
    # campaigns = account.get_campaigns(fields=['name','id'], params={'limit':100})
    campaigns = account.get_campaigns(fields=['name','id','effective_status'], params={'effective_status':['ACTIVE']})
    # print(campaigns)
    # Iterate over all campaigns and find the first campaign that matches the search string
    for campaign in campaigns:
        campaign_id = campaign['id']
        campaign_obj = Campaign(campaign_id)
        print(campaign_id)
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')

        insights = campaign_obj.get_insights(fields=['spend'],params={'date_preset': 'yesterday'})
        if insights:
            
            campaign_data = {'name': campaign['name'], 'id': campaign_id, 'spend': insights[0]['spend']}
            ad_spend = float(campaign_data['spend'])
            name_of_campaign = campaign['name']
            
            

                

    return 'Campaign not found'
