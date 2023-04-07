from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebook_business.adobjects.adcreativevideodata import AdCreativeVideoData
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.advideo import AdVideo
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.adobjects.targetingsearch import TargetingSearch
from datetime import datetime
import datetime
import requests, json
import random 
from decouple import config
import logging


def create_facebook_campaign(campaign_name):
    try:
        access_token = config('CAMPAIGNS_SECRET')
        ad_account_id = config('MARKETING_AD_ACCOUNT')
        FacebookAdsApi.init(access_token=access_token)
        fields = [
        ]
        params = {
        'name': campaign_name,
        'objective': 'OUTCOME_SALES',
        'status': 'PAUSED',
        'special_ad_categories': [],
        }
        campaign = AdAccount(ad_account_id).create_campaign(
        fields=fields,
        params=params,
        )
        return campaign
    except Exception as e:
        # Log the exception using the Django logger
        logger.exception(f"An error occurred while creating a Facebook CAMPAIGN: {e}")
        return {"error": str(e)}


def create_facebook_adset(campaign_id, name, budget, max_age, min_age, interest_id, interest_name, genders=None):
    try:
        access_token = config('CAMPAIGNS_SECRET')
        ad_account_id = config('MARKETING_AD_ACCOUNT')
        instagram_account_id = '5225011497548175'
        pixel_id = config('PIXEL_ID')
        selected_genders = []
        if genders is None:
            selected_genders = [1, 2]
        else:
            selected_genders = genders


        FacebookAdsApi.init(access_token=access_token)

        if interest_id != 'OPEN_AUDIENCE':
            ad_set = AdAccount(ad_account_id).create_ad_set(
            fields=[],
            params={
                'name': name,
                'optimization_goal': 'OFFSITE_CONVERSIONS',
                'billing_event': 'IMPRESSIONS',
                'promoted_object': {
                    'pixel_id': pixel_id,
                    'custom_event_type': 'PURCHASE',
                },
                'lifetime_budget': 0,
                'daily_budget': budget,
                'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
                'campaign_id': campaign_id,
                'targeting': {
                    'age_max': max_age,
                    'age_min': min_age,
                    'genders': selected_genders,
                    'geo_locations': {
                        'countries': ['MK'],
                        'location_types': ['home', 'recent'],
                    },
                    "flexible_spec": [
                        {
                            'interests': [
                                {
                                    'id': interest_id,
                                    'name': interest_name,
                                },
                            ]
                        }
                    ]
                },
                'status': 'PAUSED',
            },
            )
            return ad_set
        else:
            ad_set = AdAccount(ad_account_id).create_ad_set(
            fields=[],
            params={
                'name': name,
                'optimization_goal': 'OFFSITE_CONVERSIONS',
                'billing_event': 'IMPRESSIONS',
                'promoted_object': {
                    'pixel_id': pixel_id,
                    'custom_event_type': 'PURCHASE',
                },
                'lifetime_budget': 0,
                'daily_budget': budget,
                'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
                'campaign_id': campaign_id,
                'targeting': {
                    'age_max': max_age,
                    'age_min': min_age,
                    'genders': selected_genders,
                    'geo_locations': {
                        'countries': ['MK'],
                        'location_types': ['home', 'recent'],
                    },
                    "flexible_spec": [],
                },
                'status': 'PAUSED',
            },
            )
            return ad_set
        except Exception as e:
        # Log the exception using the Django logger
        logger.exception(f"An error occurred while creating a Facebook ADSET: {e}")
        return {"error": str(e)}
        


def create_facebook_ad(ad_set_id, ad_type, ad_name, ad_primary_text, ad_description_text, ad_headline_text,ad_link_url, ad_image=None, ad_video = None, ad_thumbnail=None):
    try:
        access_token = config('CAMPAIGNS_SECRET')
        ad_account_id = config('MARKETING_AD_ACCOUNT')
        instagram_account_id = '5225011497548175'
        pixel_id = config('PIXEL_ID')
        FacebookAdsApi.init(access_token=access_token)



        if(ad_type == 'image'):
            print('is_image')
            image = AdImage(parent_id=ad_account_id)
            image[AdImage.Field.filename] = ad_image[1:]
            image.remote_create()

            # Create creative
            link_data = AdCreativeLinkData()
            link_data[AdCreativeLinkData.Field.link] = ad_link_url
            link_data[AdCreativeLinkData.Field.message] = ad_primary_text #Primary text
            link_data[AdCreativeLinkData.Field.description] = ad_description_text #Description
            link_data[AdCreativeLinkData.Field.name] = ad_headline_text #Headline
            link_data[AdCreativeLinkData.Field.caption] = 'www.greengoshop.mk'

            link_data[AdCreativeLinkData.Field.image_hash] = image.get_hash()
            link_data[AdCreativeLinkData.Field.call_to_action] = {
            'type': 'SHOP_NOW',
            'value': {
                'link': ad_link_url
            }
            }
            object_story_spec = AdCreativeObjectStorySpec()
            object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = '110068238444042'
            object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = link_data
            object_story_spec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagram_account_id

            creative = AdCreative(parent_id=ad_account_id)
            creative[AdCreative.Field.name] = 'My ad'
            creative[AdCreative.Field.object_story_spec] = object_story_spec
            creative.remote_create()
            tracking_specs = [{
                'action.type': ['offsite_conversion'],
                'offsite_pixel': [pixel_id],
            }]
            ad = AdAccount(ad_account_id).create_ad(
                fields=[],
                params={
                    'name': ad_name,
                    'adset_id': ad_set_id,
                    'conversion_domain': 'greengoshop.mk',
                    'creative': {'creative_id': creative['id']},
                    'instagram_actor_id': instagram_account_id,
                    'status': 'PAUSED',
                    'pixel_id': pixel_id,
                    'page_id': '110068238444042',
                },
            )
            return ad


        elif(ad_type == 'video'):
            print('is_video')
            video = AdVideo(parent_id=ad_account_id)
            video[AdVideo.Field.filepath] = ad_video[1:]
            video.remote_create()

            thumbnail = AdImage(parent_id=ad_account_id)
            thumbnail[AdImage.Field.filename] = ad_thumbnail[1:]
            created_thumbnail = thumbnail.remote_create()

            video_data = AdCreativeVideoData()
            video_data[AdCreativeVideoData.Field.video_id] = video.get_id()
            video_data[AdCreativeVideoData.Field.image_url] = created_thumbnail["url"]
            video_data[AdCreativeVideoData.Field.message] = ad_primary_text #Primary text
            video_data[AdCreativeVideoData.Field.link_description] = ad_description_text #Description
            video_data[AdCreativeVideoData.Field.title] = ad_headline_text #Headline


            #message,name,caption,description,
            video_data[AdCreativeVideoData.Field.call_to_action] = {
                'type': 'SHOP_NOW',
                'value': {
                    'link': ad_link_url
                    }
            }



            object_story_spec = AdCreativeObjectStorySpec()
            object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = '110068238444042'
            object_story_spec[AdCreativeObjectStorySpec.Field.instagram_actor_id] = instagram_account_id
            object_story_spec[AdCreativeObjectStorySpec.Field.video_data] = video_data

            creative = AdCreative(parent_id=ad_account_id)
            creative[AdCreative.Field.name] = 'My ad'
            creative[AdCreative.Field.object_story_spec] = object_story_spec

            creative.remote_create()

            #generate random int from 1 to 10000
            random_number = random.randint(1, 10000)

            ad = AdAccount(ad_account_id).create_ad(
                fields=[],
                params={
                    'name': ad_name,
                    'adset_id': ad_set_id, # change
                    'conversion_domain': 'greengoshop.mk',
                    'creative': {'creative_id': creative['id']},
                    'instagram_actor_id': instagram_account_id,
                    'status': 'PAUSED',
                    'pixel_id': pixel_id,
                    'page_id': '110068238444042',  
                },
            )
    except Exception as e:
        # Log the exception using the Django logger
        logger.exception(f"An error occurred while creating a Facebook ad: {e}")
        return {"error": str(e)}




def format_number(num):
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num//1000}k"
    else:
        return str(num)
    

def search_ad_interests(request, query):
    if request.method == 'GET':
                           
        access_token = config('CAMPAIGNS_SECRET')
        ad_account_id = config('MARKETING_AD_ACCOUNT')
        instagram_account_id = '5225011497548175'
        pixel_id = config('PIXEL_ID')   
        app_secret = config('CAMPAIGNS_SECRET')
        app_id = config('FACEBOOK_APP_ID')

        FacebookAdsApi.init(access_token=access_token)

        q = query
        params = {
            'q': q,
            'type': 'adinterest',
            'limit': 10,
            'ad_account_id': ad_account_id,
            'targeting_spec': {
                'age_min': 18,
                'age_max': 65,
                'genders': [0, 1, 2],
                'geo_locations': {
                    'countries': ['MK'],
                },
            }
        }
        interests = TargetingSearch.search(params=params)

        results = []
        for interest in interests:
            result = {
                'id': interest['id'],
                'name': interest['name'],
                'lower_reach': interest['audience_size_lower_bound'],
                'upper_reach': interest['audience_size_upper_bound']
            }

            targeting_spec2 = {
                'age_min': 18,
                'age_max': 65,
                'genders': [0, 1, 2],
                'geo_locations': {
                    'countries': ['MK'],
                },
                'interests': [
                    {
                        'id': result['id'],
                        'name': result['name'],
                    }
                ]
            }
            params={
                'targeting_spec': json.dumps(targeting_spec2),
                'app_id': app_id,
                'app_secret': app_secret,
                'access_token': access_token,
            }
            estimated_interest_url = f"https://graph.facebook.com/v16.0/{ad_account_id}/reachestimate"
            response = requests.get(estimated_interest_url, params=params)
            if response.status_code == 200:
                response_json = response.json()
                result['users_lower_bound'] = f"{int(response_json['data']['users_lower_bound']):,}"
                result['users_upper_bound'] = f"{int(response_json['data']['users_upper_bound']):,}"
                result['adset_name'] = f"{result['name']} " + format_number(response_json['data']['users_upper_bound'])
                result['sortable_field'] = response_json['data']['users_upper_bound']
                print(result)
            else:
                print(response.status_code)
                print(response.text)

            results.append(result)

        sorted_result = sorted(results, key=lambda x: x['sortable_field'], reverse=True)
        print(sorted_result)
        return sorted_result


        
def create_ad_preview(ad_primary_text, ad_description_text, ad_headline_text, photo_url):
    access_token = config('CAMPAIGNS_SECRET')
    ad_account_id = config('MARKETING_AD_ACCOUNT')
    
    FacebookAdsApi.init(access_token=access_token)
    fields = [
    ]
    params = {
    'creative': {'object_story_spec':{'link_data':{'call_to_action':{'type':'SHOP_NOW','value':{'link':'https://greengoshop.mk'}},'description':ad_description_text,'link':'https://greengoshop.mk','message':ad_primary_text,'name':ad_headline_text,'picture':photo_url},'page_id':'110068238444042'}},
    'ad_format': 'MOBILE_FEED_STANDARD',
    }
    ad_previews = AdAccount(ad_account_id).get_generate_pre_views(
    fields=fields,
    params=params,
    )


    return ad_previews[0]['body']
    

def get_open_audience(request):
    if request.method == 'GET':
        access_token = config('CAMPAIGNS_SECRET')
        ad_account_id = config('MARKETING_AD_ACCOUNT')
        instagram_account_id = '5225011497548175'
        pixel_id = config('PIXEL_ID')   
        app_secret = config('CAMPAIGNS_SECRET')
        app_id = config('FACEBOOK_APP_ID')
        FacebookAdsApi.init(app_id=app_id, app_secret=app_secret, access_token=access_token)


        targeting_spec2 = {
            'age_min': 20,
            'age_max': 65,
            'geo_locations': {
                'countries': ['MK'],
            },
            
        }
        params={
            'targeting_spec': json.dumps(targeting_spec2),
            'app_id': app_id,
            'app_secret': app_secret,
            'access_token': access_token,
        }
        estimated_interest_url = f"https://graph.facebook.com/v16.0/{ad_account_id}/reachestimate"
        response = requests.get(estimated_interest_url, params=params)
        result = {}
        if response.status_code == 200:
            response_json = response.json()
            result['users_lower_bound'] = f"{int(response_json['data']['users_lower_bound']):,}"
            result['users_upper_bound'] = f"{int(response_json['data']['users_upper_bound']):,}"
            result['adset_name'] = f"Open Audience " + format_number(response_json['data']['users_upper_bound'])
        else:
            pass


        return result
