from django.shortcuts import redirect, render
from django.contrib import messages
from shop.models import Product, CartItems, Cart, CheckoutFees, CartFees, ProductAttribute
from django.http import HttpResponse, JsonResponse
import time
import json
from facebook_business.adobjects.serverside.action_source import ActionSource
from facebook_business.adobjects.serverside.content import Content
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.delivery_category import DeliveryCategory
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.api import FacebookAdsApi
import string
from hashlib import sha256
import logging



logger = logging.getLogger(__file__)

access_token = 'EAAEBgQEZCiHkBADdHkI851cusMTxrZBLh8WA2HbNSlG06N7qeTtNxEKH3fQeMxI9h0nK6HRJJSmt09xI51gfGCS6DZBCuJFcO08Ux4sVDXZCculFpt3BAVbZCABjS2EkzBHJQ4zb8nwfD7RTXvSRv4togCDzHJMEbRVaa8TWR31pmIs5DztfZA'
pixel_id = '201484344738499'
FacebookAdsApi.init(access_token=access_token)


def AddToCartPixelEvent(request, addtocart_type, product, qty, offer_price = None,
     full_product_attribute_name = None, attribute_price = None, attribute_label = None):
    if(addtocart_type == 'NORMAL'):
        total_price = product.sale_price * qty
        user_data = UserData(
                        client_ip_address=request.META.get('REMOTE_ADDR'),
                        client_user_agent=request.headers['User-Agent'],
                        fbc=request.COOKIES.get('_fbc'),
                        fbp=request.COOKIES.get('_fbp'),
                       
                    )
        content = Content(
                        brand='GreenGoShop',
                        product_id=product.id,
                        quantity=qty,
                        item_price = product.sale_price,
                        category=str(product.category.name),
                        delivery_category=DeliveryCategory.HOME_DELIVERY,
                    )

        custom_data = CustomData(
                        contents=[content],
                        content_type = 'product',
                        currency='MKD',
                        value=total_price,
                        content_name= product.title,
                        content_category= str(product.category.name),
                        content_ids= product.id,
                        delivery_category= DeliveryCategory.HOME_DELIVERY,
                        
                    )

        event = Event(
                        event_name='AddToCart',
                        event_time=int(time.time()),
                        user_data=user_data,
                        custom_data=custom_data,
                        event_source_url= request.build_absolute_uri(),
                        action_source=ActionSource.WEBSITE,
                        
                    )

        #logger.info(event)
        events = [event]

        event_request = EventRequest(
                        events=events,
                        pixel_id=pixel_id,
                        test_event_code = 'TEST31193',
                    )

        event_response = event_request.execute()
        #logger.info(event_response)


    if(addtocart_type == 'OFFER'):

        total_price = offer_price * qty
        user_data = UserData(
                    client_ip_address=request.META.get('REMOTE_ADDR'),
                    client_user_agent=request.headers['User-Agent'],
                    fbc=request.COOKIES.get('_fbc'),
                    fbp=request.COOKIES.get('_fbp'),
                    
                )
        content = Content(
                    brand='GreenGoShop',
                    product_id=product.id,
                    quantity=qty,
                    item_price = offer_price,
                    category=str(product.category.name),
                    delivery_category=DeliveryCategory.HOME_DELIVERY,
                )

        custom_data = CustomData(
                    contents=[content],
                    content_type = 'product',
                    currency='MKD',
                    value=total_price,
                    content_name= product.title,
                    content_category= str(product.category.name),
                    content_ids= product.id,
                    delivery_category= DeliveryCategory.HOME_DELIVERY,
                )

        event = Event(
                    event_name='AddToCart',
                    event_time=int(time.time()),
                    user_data=user_data,
                    custom_data=custom_data,
                    event_source_url= request.build_absolute_uri(),
                    action_source=ActionSource.WEBSITE,
                )


        events = [event]

        event_request = EventRequest(
                    events=events,
                    pixel_id=pixel_id,
                    test_event_code = 'TEST14802',
                )

        event_response = event_request.execute()

    

    if(addtocart_type == 'VARIABLE'):
        catalogue_attribute_label = str(product.id) + '_' + attribute_label
        total_price = attribute_price * qty
        user_data = UserData(
            client_ip_address=request.META.get('REMOTE_ADDR'),
            client_user_agent=request.headers['User-Agent'],
            fbc=request.COOKIES.get('_fbc'),
            fbp=request.COOKIES.get('_fbp'),
            
        )
        content = Content(
            brand='GreenGoShop',
            product_id=product.id, #fix
            quantity=qty,
            item_price = attribute_price,
            category=str(product.category.name),
            delivery_category=DeliveryCategory.HOME_DELIVERY,
        )

        custom_data = CustomData(
            contents=[content],
            content_type = 'product',
            currency='MKD',
            value=total_price,
            content_name= full_product_attribute_name,
            content_category= str(product.category.name),
            content_ids= catalogue_attribute_label,
            delivery_category= DeliveryCategory.HOME_DELIVERY,
        )

        event = Event(
            event_name='AddToCart',
            event_time=int(time.time()),
            user_data=user_data,
            custom_data=custom_data,
            event_source_url= request.build_absolute_uri(),
            action_source=ActionSource.WEBSITE,
        )


        events = [event]

        event_request = EventRequest(
            events=events,
            pixel_id=pixel_id,
            test_event_code = 'TEST31193',
        )

        event_response = event_request.execute()
        print(event_response)


def InitiateCheckoutEvent(request): 
    cartItems = CartItems.objects.filter(cart__session=request.session['nonuser'])
    print(cartItems)
    print(request.session['nonuser'])
    cart_total = 0
    content_ids = []
    content_names = []
    content_category = []
    custom_content_list = []
    itemscount = 0
    if cartItems:
        for item in cartItems:
            content_ids.append(str(item.product.id))
            
            content_category.append(str(item.product.category.name))
            if(item.attributeprice is not None):
                cart_total = cart_total + (item.attributeprice * item.product_qty)
                itemscount = itemscount + item.product_qty
                content_names.append(item.product.title  + item.attributename)
                custom_content_list.append(Content(
                    product_id=str(item.product.id), #fix
                    quantity=str(item.product_qty),
                    item_price = str(item.attributeprice),
                    category=str(item.product.category.name),
                    delivery_category=DeliveryCategory.HOME_DELIVERY,))
            elif(item.offer_price is not None):
                cart_total = cart_total + (item.offer_price * item.product_qty)
                itemscount = itemscount + item.product_qty
                content_names.append(item.product.title)
                custom_content_list.append(Content(
                    product_id=str(item.product.id), #fix
                    quantity=str(item.product_qty),
                    item_price = str(item.offer_price),
                    category=str(item.product.category.name),
                    delivery_category=DeliveryCategory.HOME_DELIVERY,))
            else:
                cart_total = cart_total + (item.product.sale_price * item.product_qty)
                itemscount = itemscount + item.product_qty
                content_names.append(item.product.title)
                custom_content_list.append(Content(
                    product_id=str(item.product.id), #fix
                    quantity=str(item.product_qty),
                    item_price = str(item.product.sale_price),
                    category=str(item.product.category.name),
                    delivery_category=DeliveryCategory.HOME_DELIVERY,))

    user_data = UserData(
                        client_ip_address=request.META.get('REMOTE_ADDR'),
                        client_user_agent=request.headers['User-Agent'],
                        fbc=request.COOKIES.get('_fbc'),
                        fbp=request.COOKIES.get('_fbp'),
                       
                    )

    custom_data = CustomData(
                    contents=custom_content_list,
                    content_type = 'product',
                    currency='mkd',
                    value=cart_total,
                    content_name= json.dumps(content_names, ensure_ascii=False),
                    content_category= json.dumps(content_category, ensure_ascii=False),
                    content_ids= json.dumps(content_ids),
                    delivery_category= DeliveryCategory.HOME_DELIVERY,
                    num_items = itemscount,
                )

    event = Event(
                    event_name='InitiateCheckout',
                    event_time=int(time.time()),
                    user_data=user_data,
                    custom_data=custom_data,
                    event_source_url= request.build_absolute_uri(),
                    action_source=ActionSource.WEBSITE,
                    
                )

    events = [event]

    event_request = EventRequest(
                    events=events,
                    pixel_id=pixel_id,
                    test_event_code = 'TEST31193',
                )

    event_response = event_request.execute()
    
    
def PurchaseEvent(request, order_items, order_total, number, city, name):
    splitted_name = name.split(" ")
    user_name = ''
    user_lastname = ''
    try:
        user_name = splitted_name[0].translate(str.maketrans('', '', string.punctuation))
        print(user_name)
    except:
        user_name = ''
    
    try:
        user_lastname = splitted_name[1].translate(str.maketrans('', '', string.punctuation))
        print(user_lastname)
    except:
        user_lastname = ''
    try:
        user_city = city
    except:
        user_city = ''
    try:  
        user_phone_number = str(int(''.join(filter(str.isdigit, number))))
    except:
        user_phone_number = ''
    if user_phone_number.startswith('3') == False:
        user_phone_number = '389' + user_phone_number



    cart_total = 0
    content_ids = []
    content_names = []
    content_category = []
    custom_content_list = []
    itemscount = 0
    for item in order_items:
        content_ids.append(str(item.product.id))
        
        content_category.append(str(item.product.category.name))
        if item.has_attributes == True:
            itemscount = itemscount + item.product_qty
            content_names.append(item.product.title + item.attributename)
            custom_content_list.append(Content(
                product_id=str(item.product.id), #fix
                quantity=str(item.product_qty),
                item_price = str(item.attributeprice),
                category=str(item.product.category.name),
                delivery_category=DeliveryCategory.HOME_DELIVERY,))
        elif item.has_offer == True:
            itemscount = itemscount + item.product_qty
            content_names.append(item.product.title)
            custom_content_list.append(Content(
                product_id=str(item.product.id), #fix
                quantity=str(item.product_qty),
                item_price = str(item.offer_price),
                category=str(item.product.category.name),
                delivery_category=DeliveryCategory.HOME_DELIVERY,))
        else:
            itemscount = itemscount + item.product_qty
            content_names.append(item.product.title)
            custom_content_list.append(Content(
                product_id=str(item.product.id), #fix
                quantity=str(item.product_qty),
                item_price = str(item.product.sale_price),
                category=str(item.product.category.name),
                delivery_category=DeliveryCategory.HOME_DELIVERY,))
        
    user_data = UserData(
                        client_ip_address=request.META.get('REMOTE_ADDR'),
                        client_user_agent=request.headers['User-Agent'],
                        fbc=request.COOKIES.get('_fbc'),
                        fbp=request.COOKIES.get('_fbp'),
                        first_name=sha256(user_name.encode('utf-8')).hexdigest(),
                        last_name=sha256(user_lastname.encode('utf-8')).hexdigest(),
                        city=sha256(user_city.encode('utf-8')).hexdigest(),
                        country_code=sha256('mk'.encode('utf-8')).hexdigest(),
                        phone=sha256(user_phone_number.encode('utf-8')).hexdigest(),    
                    )


    custom_data = CustomData(
                    contents=custom_content_list,
                    content_type = 'product',
                    currency='MKD',
                    value=order_total,
                    content_name= json.dumps(content_names, ensure_ascii=False),
                    content_category= json.dumps(content_category, ensure_ascii=False),
                    content_ids= json.dumps(content_ids),
                    delivery_category= DeliveryCategory.HOME_DELIVERY,
                    num_items = itemscount,
                    
                )

    event = Event(
                    event_name='Purchase',
                    event_time=int(time.time()),
                    user_data=user_data,
                    custom_data=custom_data,
                    event_source_url= request.build_absolute_uri(),
                    action_source=ActionSource.WEBSITE,
                    
                )

    events = [event]

    event_request = EventRequest(
                    events=events,
                    pixel_id=pixel_id,
                    test_event_code = 'TEST31193',
                )

    event_response = event_request.execute()
