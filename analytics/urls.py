from django.urls import path, include
from . import views


urlpatterns = [
    path('create-already-existing-campaign-ad/', views.create_already_existing_campaign_ad, name='create_already_existing_campaign_ad'),
    path('get-campaign-adsets', views.get_campaign_adsets, name='get_campaign_adsets'),
    path('remove-stored-audience', views.remove_stored_audience, name='remove_stored_audience'),
    path('store-new-audience', views.store_new_audience, name='store_new_audience'),
    path('get-open-audience', views.get_open_audience, name='get_open_audience'),
    path('get-ad-preview', views.get_ad_preview, name='get_ad_preview'),
    path('save-new-campaign-id', views.save_new_campaign_id, name='save_new_campaign_id'),
    path('create-campaign', views.create_campaign, name='create_campaign'),
    path('search-ad-audiences', views.search_ad_audiences, name='search_ad_audiences'),
    path('generate-ad-video-thumbnail', views.generate_ad_video_thumbnail, name='generate_ad_video_thumbnail'),
    path('get-video-thumbnails', views.get_video_thumbnails, name='get_video_thumbnails'),
    path('upload-campaign-photo', views.upload_campaign_photo, name='upload_campaign_photo'),
    path('upload-campaign-video', views.upload_campaign_video, name='upload_campaign_video'),
    path('get-product', views.get_product, name='get_product'),
    path('create-new-ad', views.create_new_ad, name='create_new_ad'),
    path('retrieve_adspend', views.retrieve_adspend, name='retrieve_adspend'),
    path('daily_ad_spend/<int:pk>/', views.daily_ad_spend_by_id, name='daily_ad_spend_by_id'),
    path('daily_ad_spend/', views.daily_ad_spend, name='daily_ad_spend'),
    path('login/', views.user_login, name='login'),
    path('add_comment', views.add_comment, name="addcomment"),
    path('delete-comment', views.remove_comment, name="remove-comment"),
    path('add_old_row', views.add_old_row, name="add_old_row"),
    path('', views.index, name='index'),
]
