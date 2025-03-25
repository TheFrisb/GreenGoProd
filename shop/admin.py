from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.


class FAQInline(admin.TabularInline):
    model = ProductFAQ
    
    
class InformationInline(admin.StackedInline):
    model = OrderItem
    list_display = ("Product_Title", "name",  "rating", "date_created")


class ProductUpsellsInline(admin.StackedInline):
    model = ProductUpsells
    fk_name = "parent_product"
    autocomplete_fields = ["product"]
    list_display = ("product", "title", "thumbnail", "regular_price", "sale_price", "is_free")
    
    
class CampaignItems(admin.StackedInline):
    model = ProductCampaigns
    
    
class InformationInline2(admin.StackedInline):
    model = OrderFeesItem
    list_display = ("title", "price")


class GalleryInline(admin.StackedInline):
    model = ProductGallery
    
    
class CartItemInline(admin.StackedInline):
    model = CartItems
    

class ProductAttributesInLine(admin.TabularInline):
    model = ProductAttribute
    exclude = ('is_checked',)
    list_display=("product", "color", "size", "supplier_stock_price", "price", "thumbnail", "is_disabled")

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address', 'city','number', 'tracking_no']
    list_display = ("tracking_no", "name", "created_at", "get_status", "total_price", "get_shipping")
    inlines = [InformationInline, InformationInline2]
    change_list_template = 'admin/redirect_to_shopmanager.html'
    

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title', 'sku', 'supplier__name']
    list_filter = ['category', 'status']
    readonly_fields = ['slug']
    list_display = ("title", "sale_price",  "date_posted")
    fieldsets = (
        ('Задолжителни:', {
            'fields': ('status', 'category', 'title', 'slug', 'thumbnail',  'content', 'regular_price', 'sale_price',
            'supplier', 'sku', 'supplier_stock_price', 'date_posted',),
        }),
        ('Widgets:', {
            'fields': ('gallery_is_verified', 'is_best_seller',),
           'description': 'Прикажи widgets на product page',
        }),
        ('Атрибути и Понуди:',{
            'fields': ('attributes_type',),
        }),
        )
    inlines = [ProductAttributesInLine, GalleryInline, FAQInline, CampaignItems, ProductUpsellsInline]
    # list_editable 
    
  
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['product__title', 'product__sku', 'name', 'rating', ]
    autocomplete_fields = ["product"]
    list_display = ("Product_Title", "name",  "rating", "date_created")


class ColorAdmin(admin.ModelAdmin):
    form = ColorForm


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'color', 'price')

    
class CartOfferAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]
    exclude = ['is_added']
    
    
class CartAdmin(admin.ModelAdmin):
    search_fields = ['session', 'name', 'name', 'phone', ]
    list_display = ('session', 'name', 'name', 'phone')
    inlines = [CartItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(CartOffers, CartOfferAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Offer)
admin.site.register(Size)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Cart, CartAdmin)
admin.site.register(CheckoutFees)
admin.site.register(ProductCampaigns)
admin.site.register(AbandonedCartItems)
admin.site.register(AbandonedCarts)
