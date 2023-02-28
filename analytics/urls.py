from django.urls import path, include
from . import views


urlpatterns = [
    path('get_ad_spend_by_date', views.get_ad_spend_by_date, name='get_ad_spend_by_date'),
    path('daily_ad_spend/<int:pk>/', views.daily_ad_spend_by_id, name='daily_ad_spend_by_id'),
    path('daily_ad_spend/', views.daily_ad_spend, name='daily_ad_spend'),
    path('login/', views.user_login, name='login'),
    path('add_comment', views.add_comment, name="addcomment"),
    path('add_old_row', views.add_old_row, name="add_old_row"),
    path('', views.index, name='index'),
]
