from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.

class InformationInline(admin.StackedInline):
    model = OrderItem
    list_display = ("Product_Title", "name",  "rating", "date_created")


class ProductAttributesInLine(admin.TabularInline):
    model = ProductAttribute
    list_display=("product", "color", "size", "price")

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address', 'city','number', 'tracking_no']
    list_display = ("tracking_no", "name", "created_at", "get_status", "total_price", "get_shipping")
    inlines = [InformationInline]


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title', 'sku', 'supplier']
    exclude = ("slug",)
    list_display = ("title", "sale_price",  "date_posted")
    inlines = [ProductAttributesInLine]
    # list_editable 
    
  
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['product__title', 'product__sku', 'name', 'rating', ]
    list_display = ("Product_Title", "name",  "rating", "date_created")


class ColorAdmin(admin.ModelAdmin):
    form = ColorForm




class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'color', 'price')


admin.site.register(Category)
admin.site.register(Dobavuvac)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductGallery)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size)
admin.site.register(Offer)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cart)
admin.site.register(CartOffers)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)


