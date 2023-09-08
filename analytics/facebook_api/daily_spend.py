from django.http import HttpResponse, JsonResponse
import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from datetime import date, datetime, timedelta
from analytics.models import *
from datetime import datetime
from shop.models import product_campaigns, Product, ProductUpsells
from decouple import config
from django.db.models import Q


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

            campaign_id = campaign['id']
            populate_daily_rows(campaign_id, ad_spend)

                

    return 'Campaign not found'



def populate_daily_rows(campaign_id, ad_spend):
    try:
        product_campaign_ob = product_campaigns.objects.get(campaign_id=campaign_id)
        campaigns_product = product_campaign_ob.product
        product_campaign = product_campaigns.objects.filter(product=campaigns_product)


    except:
        return 1
    if product_campaign.count() == 1:
        
        product = product_campaign[0].product
        owner_of_campaign = daily_items.objects.filter(product=product).first()
        product_price = product.sale_price - 130
        stock_price = product.supplier_stock_price
        related_upsells = ProductUpsells.objects.filter(parent_product=product)
        if related_upsells:
            for upsell in related_upsells:
                if upsell.is_free:
                    stock_price += upsell.product.supplier_stock_price
                    
        fixed_cost = 0
        quantity = 0

        start_time = date.today() - timedelta(days=1)
        end_time = date.today()
        yesterday = start_time
        print(owner_of_campaign)
        ordered_products = OrderItem.objects.filter(Q(order__status='Pending', product=product, created_at__range=(start_time, end_time)) | Q(order__status='Confirmed', product=product, created_at__range=(start_time, end_time)))
        print(ordered_products)
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

        daily_row_new = daily_row(owner=owner_of_campaign, quantity=quantity, price=product_price, stock_price=stock_price, fixed_cost=fixed_cost,
                                ad_cost=yesterdays_ad_spend,neto_price=neto_price, neto_total=neto_total, profit=profit, cost_per_purchase = cost_per_purchase,
                                be_roas = be_roas, roas=roas, roi=roi, created_at=yesterday)
        
        daily_row_new.save()
    
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
            product_price = product.sale_price - 130
            stock_price = product.supplier_stock_price
            related_upsells = ProductUpsells.objects.filter(parent_product=product)
            if related_upsells:
                for upsell in related_upsells:
                    if upsell.is_free:
                        stock_price += upsell.product.supplier_stock_price
                        
            fixed_cost = 0
            quantity = 0
            
            start_time = date.today() - timedelta(days=1)
            yesterday = start_time
            end_time = date.today()
            print(owner_of_campaign)
            ordered_products = OrderItem.objects.filter(Q(order__status='Pending', product=product, created_at__range=(start_time, end_time)) | Q(order__status='Confirmed', product=product, created_at__range=(start_time, end_time)))
            print(ordered_products)
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

            daily_row_new = daily_row(owner=owner_of_campaign, quantity=quantity, price=product_price, stock_price=stock_price, fixed_cost=fixed_cost,
                                    ad_cost=yesterdays_ad_spend,neto_price=neto_price, neto_total=neto_total, profit=profit, cost_per_purchase = cost_per_purchase,
                                    be_roas = be_roas, roas=roas, roi=roi, created_at=yesterday)
            
            daily_row_new.save()

        
    else:
        return 1
    return 1



def testing_populate_daily_rows(campaign_id, ad_spend):
    try:
        product_campaign_ob = product_campaigns.objects.get(campaign_id=campaign_id)
        campaigns_product = product_campaign_ob.product
        product_campaign = product_campaigns.objects.filter(product=campaigns_product)


    except:
        return 1
    if product_campaign.count() == 1:
        
        product = product_campaign[0].product
        owner_of_campaign = daily_items.objects.filter(product=product).first()
        product_price = product.sale_price - 130
        stock_price = product.supplier_stock_price
        related_upsells = ProductUpsells.objects.filter(parent_product=product)
        if related_upsells:
            for upsell in related_upsells:
                if upsell.is_free:
                    stock_price += upsell.product.supplier_stock_price
                    
        fixed_cost = 0
        quantity = 0

        start_time = date.today() - timedelta(days=1)
        end_time = date.today()
        yesterday = start_time
        print(owner_of_campaign)
        ordered_products = OrderItem.objects.filter(Q(order__status='Pending', product=product, created_at__range=(start_time, end_time)) | Q(order__status='Confirmed', product=product, created_at__range=(start_time, end_time)))
        print(ordered_products)
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

        return 1
    
    elif product_campaign.count() > 1:
        yesterday_row = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        product = product_campaign[0].product
        owner_of_campaign = daily_items.objects.filter(product=product).first()
        row = daily_row.objects.filter(created_at__date=yesterday_row, owner=owner_of_campaign).first()

        if(row):

        

            return JsonResponse({'status': "Updated existing row for yesterday's date"})
        else:

            product = product_campaign[0].product
            owner_of_campaign = daily_items.objects.filter(product=product).first()
            product_price = product.sale_price - 130
            stock_price = product.supplier_stock_price
            related_upsells = ProductUpsells.objects.filter(parent_product=product)
            if related_upsells:
                for upsell in related_upsells:
                    if upsell.is_free:
                        stock_price += upsell.product.supplier_stock_price
                        
            fixed_cost = 0
            quantity = 0
            
            start_time = date.today() - timedelta(days=1)
            end_time = date.today()
            print(owner_of_campaign)
            yesterday = start_time
            ordered_products = OrderItem.objects.filter(Q(order__status='Pending', product=product, created_at__range=(start_time, end_time)) | Q(order__status='Confirmed', product=product, created_at__range=(start_time, end_time)))
            print(ordered_products)
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

            return 1
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
    ob = product_campaigns.objects.all()
    for campaign in campaigns:
        campaign_id = campaign['id']
        campaign_obj = Campaign(campaign_id)
        
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')

        
        insights = campaign_obj.get_insights(fields=['spend'],params={'date_preset': 'yesterday'})
        if insights:
            
            campaign_data = {'name': campaign['name'], 'id': campaign_id, 'spend': insights[0]['spend']}
            ad_spend = float(campaign_data['spend'])
            name_of_campaign = campaign['name']

            campaign_id = campaign['id']
            print(campaign_id, ' - ', name_of_campaign)
            testing_populate_daily_rows(campaign_id, ad_spend)

                

    return 'Campaign not found'
