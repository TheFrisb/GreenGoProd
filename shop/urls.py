from django.urls import path, include
from .views import ProductListView, CheckoutView, SearchResultsView
from . import views
from shop.controller import cart, checkout, shopmanager

urlpatterns = [
     # path('', views.home, name='shop-home'),
    path('', views.ProductListView, name='shop-home'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path('product-category/<str:slug>/', views.CategoryView, name='category-page'),
    
    path('product/<str:slug>/', views.ProductView, name='product-page'),

    path('add-to-cart', cart.addtocart, name="addtocart" ),
    path('variable-add-to-cart', cart.variableaddtocart, name="variableaddtocart"),
    path('offer-add-to-cart', cart.offeraddtocart, name="offeraddtocart"),
    path('update-cart', cart.updatecart, name="updatecart"),
    path('delete-cart-item', cart.deletecartitem, name="deletecartitem"),

    path('checkout/', CheckoutView, name='checkout'),

    path('add-or-delete-fee', cart.addordeletefee, name="addordeletefee"),

    path('place-order', checkout.placeorder, name="placeorder"),
    path('add-to-order', checkout.addtoorder, name="addtoorder"),
    
    path('thank-you/<str:slug>/', views.ThankYouView, name='thank-you-view'),

    path('shopmanager/login', views.login_shopmanager, name='login'),
    path('shopmanager/logout', views.logout_shopmanager, name='logout'),
    path('shopmanager/dashboard', views.shopmanager_dashboard, name='shopmanagerhome'),
    path('shopmanager/confirmed', views.shopmanager_confirmed, name='shconfirmed'),
    path('shopmanager/deleted', views.shopmanager_deleted, name='shdeleted'),
    path('update-order', shopmanager.updateOrderStatus, name="updateorder" ),
    path('export-excel', views.export_excel, name="export_excel"),


    path('dostava/', views.Dostava, name='dostava-page'),
    path('reklamacija/', views.Reklamacija, name='reklamacija-page'),
    path('pravila-na-koristenje/', views.Pravila_Na_Koristenje, name='rights-of-usage-page'),
    path('politika-na-privatnost-i-kolacinja', views.Cookies_Page, name='cookies-page'),
]
