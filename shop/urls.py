from django.urls import path

from shop.controller import cart, checkout, shopmanager
from . import views
from .views import CheckoutView, SearchResultsView

urlpatterns = [
    # path('', views.home, name='shop-home'),
    path('', views.ProductListView, name='shop-home'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path('product-category/<str:slug>/', views.CategoryView, name='category-page'),
    path('export-csv/', views.export_products_csv),
    path('product/<str:slug>/', views.ProductView, name='product-page'),
    path('call-pixel-checkout', views.call_pixel_checkout, name='call_pixel_checkout'),

    path('add-to-cart', cart.addtocart, name="addtocart"),
    path('variable-add-to-cart', cart.variableaddtocart, name="variableaddtocart"),
    path('offer-add-to-cart', cart.offeraddtocart, name="offeraddtocart"),
    path('update-cart', cart.updatecart, name="updatecart"),
    path('delete-cart-item', cart.deletecartitem, name="deletecartitem"),
    path('add-upsell-to-cart', cart.add_upsell_to_cart, name="addupselltocart"),

    path('accept-checkout-offer', views.accept_checkout_offer, name='accept_checkout_offer'),
    path('get-checkout-offer-status', views.get_checkout_offer_status, name='get_checkout_offer_status'),
    path('checkout/', CheckoutView, name='checkout'),
    path('check-abandoned-carts', views.create_or_check_abandoned_cart, name="create_or_check_abandoned_cart"),
    path('remove-abandoned-cart', views.remove_abandoned_cart, name='removeabandonedcart'),
    path('get_recent_ordered', views.get_recent_ordered, name="getrecentordered"),

    path('add-or-delete-fee', cart.addordeletefee, name="addordeletefee"),

    path('place-order', checkout.placeorder, name="placeorder"),
    path('add-to-order', checkout.addtoorder, name="addtoorder"),
    path('change-offer-checkout-qty', views.change_offer_checkout_qty, name='change_offer_checkout_qty'),

    path('thank-you/<str:slug>/', views.ThankYouView, name='thank-you-view'),

    path('shopmanager/login', views.login_shopmanager, name='login'),
    path('shopmanager/logout', views.logout_shopmanager, name='logout'),
    path('shopmanager/dashboard', views.shopmanager_dashboard, name='shopmanagerhome'),
    path('shopmanager/confirmed', views.shopmanager_confirmed, name='shconfirmed'),
    path('shopmanager/deleted', views.shopmanager_deleted, name='shdeleted'),
    path('shopmanager/abandoned-carts', views.shopmanager_abandoned_carts, name='shabandonedcarts'),
    path('update-order', shopmanager.updateOrderStatus, name="updateorder"),
    # path('export-excel', views.export_excel, name="export_excel"),

    path('dostava/', views.Dostava, name='dostava-page'),
    path('reklamacija/', views.Reklamacija, name='reklamacija-page'),
    path('pravila-na-koristenje/', views.Pravila_Na_Koristenje, name='rights-of-usage-page'),
    path('politika-na-privatnost-i-kolacinja', views.Cookies_Page, name='cookies-page'),
]
