from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils.html import mark_safe
from django_resized import ResizedImageField
from PIL import Image
import datetime, os
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from uuid import uuid4
from datetime import datetime
from random import randint

# Create your models here.

def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('products/', filename)

class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False, verbose_name='Име на категорија')
    published = models.BooleanField(default=True, verbose_name='Видливост:')
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категорија"
        verbose_name_plural = "Категории"

class Dobavuvac(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, verbose_name='Име на добавувач')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Добавувач"
        verbose_name_plural = "Добавувачи"


class Product(models.Model):  
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"


    status_choices = (
        ('PRIVATE', 'PRIVATE'),
        ('PUBLISHED', 'PUBLISHED'),
        ('VARIABLE', 'VARIABLE'),       
    )
    attributes_choices = (
        ('COLOR', 'COLOR'),
        ('SIZE', 'SIZE'),
        ('OFFER', 'OFFER')
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, verbose_name='Категорија', null=True)
    status = models.CharField( choices=status_choices, default = 'PRIVATE', max_length=50, verbose_name='СТАТУС')
    thumbnail = ProcessedImageField(upload_to='products/%Y/%m/%d/', processors=[ResizeToFill(550,550)], format='WEBP', options={'quality':95}, null=True)
    thumbnail_as_jpeg = ImageSpecField(source='thumbnail',format='JPEG')
    thumbnail_loop = ImageSpecField(source='thumbnail', processors=[ResizeToFill(250,250)], format='WEBP', options={'quality':95})
    thumbnail_loop_as_jpeg = ImageSpecField(source='thumbnail', processors=[ResizeToFill(250,250)], format='JPEG', options={'quality':95})
    export_image = ImageSpecField(source='thumbnail', processors=[ResizeToFill(150,150)], format='PNG', options={'quality':95})
    title = models.CharField(max_length = 100, verbose_name='Име')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='Содржина');
    regular_price = models.IntegerField(verbose_name='Стара цена')
    sale_price = models.IntegerField(verbose_name='Цена')
    free_shipping = models.BooleanField(default=False, blank=True, verbose_name='Бесплатна достава')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата на креирање')
    title_slug = models.CharField(max_length = 100,verbose_name='Url исто како на другио Website')
    slug =  models.SlugField(unique=True, max_length=250, blank = True)
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Залиха')
    attributes_type = models.CharField(choices=attributes_choices, max_length=50, blank=True, verbose_name='Одбери тип')
    fake_quantity = models.IntegerField(null=True)
    review_average = models.IntegerField(default=0)
    gallery_is_verified = models.BooleanField(default=False, blank=True, verbose_name='Верифицирани слика од производ')
    is_best_seller = models.BooleanField(default=False, blank=True, verbose_name='Прикажи голема побарувачка на product page')
    #Product Data

    supplier = models.ForeignKey(Dobavuvac, on_delete=models.CASCADE, verbose_name='Добавувач')
    supplier_stock_price = models.IntegerField(verbose_name='Набавна цена', null=True)

    sku = models.CharField(max_length = 100, verbose_name='Лабел')
    

    def save(self, *args, **kwargs):
        self.slug = self.title_slug
        self.fake_quantity = randint(2, 6)
        reviews = Review.objects.filter(product=self)
        total_rating = 0
        for review in reviews:
            total_rating += int(review.rating)
        if reviews.count() > 0:
            self.review_average = total_rating // reviews.count()
        else:
            self.review_average = 0
        super(Product, self).save(*args, **kwargs)
        self.thumbnail2 = self.thumbnail
        
        
    def __str__(self):
        return self.title

    def get_percentage_off(self):
        return int(100 - (self.sale_price / self.regular_price * 100))
    
    
    def get_absolute_url(self):
        return reverse('product-page', kwargs={'slug': self.slug})


    
class product_campaigns(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Продукт')
    campaign_id = models.CharField(max_length=100,null=True, blank=True, unique=True)
    def __str__(self):
        return self.product.title
    
    
class ProductFAQ(models.Model):
    class Meta:
        verbose_name = "Често поставувани прашања"
        verbose_name_plural = "Често поставувани прашања"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    question = models.CharField(max_length=100, verbose_name="Прашање")
    content = models.TextField(verbose_name="Одговор")
    
    
class ProductGallery(models.Model):
    class Meta:
        verbose_name = "Галерија"
        verbose_name_plural = "Галерии"


    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    galleryimg = ProcessedImageField(upload_to='products/product-gallery/%Y/%m/%d/', processors=[ResizeToFill(550,550)], format='WEBP', options={'quality':95}, null=True, verbose_name='Слика за галерија')


class Color(models.Model):
    class Meta:
        verbose_name = "Боја"
        verbose_name_plural = "Бои"


    title = models.CharField(max_length=100, null=True, verbose_name='Име')
    color_code = models.CharField(max_length=100,verbose_name='Одбери боја')

    def __str__(self):
        return '{}'.format(self.title)


class Size(models.Model):
    class Meta:
        verbose_name = "Големина"
        verbose_name_plural = "Големини"


    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Име')


    def __str__(self):
        return ' - {}'.format(self.title)


class Offer(models.Model):
    class Meta:
        verbose_name = "Понуда"
        verbose_name_plural = "Понуди"


    title = models.CharField(max_length=100, null=True, verbose_name='Име')
    incentive = models.CharField(max_length=100, blank=True, verbose_name='Додатен текст')


    def __str__(self):
        return ' - {}'.format(self.title)


class ProductAttribute(models.Model):
    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибути"

        
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Одбери продукт')
    thumbnail = ProcessedImageField(upload_to='products_attributes/%Y/%m/%d/', processors=[ResizeToFill(550,550)], format='WEBP', options={'quality':95}, null=True, blank=True, verbose_name='Слика')
    thumbnail_as_jpeg = ImageSpecField(source='thumbnail',format='JPEG')
    color = models.ForeignKey(Color , on_delete=models.SET_NULL,  null = True, blank=True, verbose_name='Боја')
    size = models.ForeignKey(Size, on_delete = models.SET_NULL,  null = True, blank=True, verbose_name='Големина')
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL,  null = True, blank=True, verbose_name='Понуда')
    price = models.IntegerField(blank=True, null=True, verbose_name='Цена')
    label = models.CharField(max_length=50, null=True, verbose_name='Лабел')
    supplier_stock_price = models.IntegerField(verbose_name='Набавна цена', null=True)
    is_disabled = models.BooleanField(default = False, blank=True)
    is_checked = models.BooleanField(default=False, blank=True)
    @property
    def checkattribute(self):
        if(self.color is not None):
            return self.color.title

        if(self.size is not None):
            return self.size.title

        if(self.offer is not None):
            return self.offer.title

        return 1
    
    
    def check_type_of_attribute(self):
        if(self.color is not None):
            return 'COLOR'

        if(self.size is not None):
            return 'SIZE'

        if(self.offer is not None):
            return 'OFFER'
        
        

    def __str__(self):
        return 'Атрибут за {} - {} - {}'.format(self.product, self.checkattribute, self.price)


class Review(models.Model):
    rating_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, verbose_name='Продукт')
    image = ProcessedImageField(upload_to='review/%Y/%m/%d/', processors=[ResizeToFit(width=400, upscale=False)], format='WEBP', options={'quality':95}, null=True, blank=True)
    image2 = ProcessedImageField(upload_to='review/%Y/%m/%d/', processors=[ResizeToFit(width=400, upscale=False)], format='WEBP', options={'quality':95}, null=True, blank=True)
    image_as_jpeg = ImageSpecField(source='image',format='JPEG')
    iamge2_as_jpeg = ImageSpecField(source='image2',format='JPEG')
    name = models.CharField(max_length=150, verbose_name='Име на reviewer')
    avatar_name = models.CharField(max_length=5, blank=True)
    content = models.TextField(verbose_name='Содржина', blank=True, null = True) 
    rating = models.CharField(choices=rating_choices, default='5', verbose_name='Оценка', max_length=5)
    date_created = models.DateField(auto_now=True)
        

    def save(self, *args, **kwargs):
        words = self.name.split()

        if len(words) == 1:
            self.avatar_name = words[0][0]
        else:
            self.avatar_name = words[0][0] + words[-1][0]


        super(Review, self).save(*args, **kwargs)
        
        
    def __str__(self):
        return 'Review за продукт: {} со име: {} и оценка: {}'.format(self.product.title,self.name, self.rating)


    @property
    def Product_Title(self):
        return self.product.title


class Cart(models.Model):
    session = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Креирана во:')
    @property
    def session_id(self):
        return self.session


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attributename = models.CharField(max_length=100, null = True, default='')
    product_qty = models.IntegerField(null=False, blank=False)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, null = True)
    attributeprice = models.IntegerField(null=True)
    offer_price = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    upsell_title = models.CharField(max_length = 100, verbose_name='Име', null=True)
    upsell_thumbnail = models.TextField(null=True)
    

    @property
    def get_session(self):
        return self.cart.session

    @property
    def has_attributes(self):
        if(self.attribute is not None):
            return True
        else:
            return False
        
    @property
    def has_offer(self):
        if(self.offer_price is not None):
            return True
        else:
            return False
        
    @property
    def is_upsell(self):
        if(self.upsell_title is not None):
            return True
        else:
            return False
        
    @property
    def getItemTotal(self):
        if(self.has_offer):
            return self.offer_price * self.product_qty
        
        elif self.has_attributes:
            return self.attributeprice * self.product_qty
        
        else:
            return self.product.sale_price * self.product_qty
        
    class Meta:
        verbose_name = "Cart Items"
        verbose_name_plural = "Cart Items"


class CartOffers(models.Model):
    class Meta:
        verbose_name = "Понуди за кошничка"
        verbose_name_plural = "Понуди за кошничка"
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Одбери продукт')
    offer_text = models.CharField(max_length=40, blank=True, verbose_name='Текст на понуда')
    price = models.IntegerField(verbose_name='Цена')
    is_added = models.BooleanField(default=False, verbose_name='Не мени!')
    def __str__(self):
        return 'Понуда во кошничка за продукт {} со текст {} IS ADDED {}'.format(self.product.title, self.offer_text, self.is_added)

    
class Order(models.Model):
    user = models.CharField( max_length=150 )
    name = models.CharField(max_length=150, null=False, verbose_name='Име')
    address = models.CharField(max_length=150, null=False, verbose_name='Адреса')
    city = models.CharField(max_length=150, null=False, verbose_name='Град')
    number = models.CharField(max_length=150, null=False, verbose_name='Број')
    subtotal_price = models.IntegerField(null=False, verbose_name='Вкупна цена без достава')
    total_price = models.IntegerField(null=False, verbose_name='Вкупна цена')
    shipping = models.BooleanField(default=True, verbose_name='Достава')
    shipping_price = models.IntegerField(default=130, blank=True)
    orderstatuses = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Refunded', 'Refunded'),
        ('Deleted', 'Deleted')
    )
    status = models.CharField(max_length=50, choices=orderstatuses, default='Pending', verbose_name='Статус')
    message = models.TextField(null=True, blank=True, verbose_name='Коментар на муштеријја')
    tracking_no = models.CharField(max_length = 150, null=True, verbose_name='Tracking number')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Креирана во:')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Променет статус:')
    
   
    @property
    def get_shipping(self):
        if self.shipping == True:
            return 'До врата: 130 ден'
        else:
            return 'Бесплатна достава'

    @property
    def get_status(self):
        if self.status == 'Pending':
            return 'Непотврдена'
        if self.status == 'Confirmed':
            return 'Потврдена'
        if self.status == 'Refunded':
            return 'Рефундирана'
        if self.status == 'Deleted':
            return 'Избришена'
    class Meta:
        verbose_name = "Порачка"
        verbose_name_plural = "Порачки"


    def __str__(self):
        return '{} - Порачка број: {} за {}, {}, со статус {}'.format(self.id, self.tracking_no, self.name, self.number, self.get_status)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name='Продукт', null=True)
    price = models.IntegerField(null=False, verbose_name='Цена')
    quantity = models.IntegerField(null=False, verbose_name='Количина')
    label = models.CharField(max_length=150, null= True)
    supplier = models.ForeignKey(Dobavuvac, on_delete=models.CASCADE, null=True)
    attribute_name = models.CharField(max_length=150, null= True)
    attribute_price = models.IntegerField(null = True)
    is_cart_offer = models.BooleanField(default = False)
    is_upsell_offer = models.BooleanField(default = False)
    is_thankyou_offer = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Креиран во:', null=True)
    item_name = models.CharField(max_length=150,null=True)
    upsell_thumbnail = models.TextField(null=True)
    
    @property
    def get_product_total(self):
        return self.price*self.quantity

    @property
    def get_orderItem_title(self):
        if(self.attribute_name is not None):
            return '{} - {}'.format(self.product__title, self.attribute_name)
        else:
            return self.product__title
        

    def __str__(self):
        return '{}({} ден) х {} - Вкупно {} ден'.format(self.product, self.price, self.quantity, self.get_product_total)


class CheckoutFees(models.Model):
    title = models.CharField(max_length=100, verbose_name='Име', null=False)
    content = models.TextField(verbose_name='Содржина', null=False)
    price = models.IntegerField(verbose_name='Цена', null = False)
    is_added = models.BooleanField(default = False)
    emoji = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return 'Order fee: {} ({} ден)'.format(self.title, self.price)


class CartFees(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    fee = models.ForeignKey(CheckoutFees, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, verbose_name='Име')
    price = models.IntegerField(verbose_name='Цена')


class OrderFeesItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fee = models.ForeignKey(CheckoutFees, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, verbose_name='Име')
    price = models.IntegerField(verbose_name='Цена')

   
    def __str__(self):
        return '{} ({} ден)'.format(self.title, self.price)
    
    
    
class Abandoned_Carts(models.Model):
    session = models.CharField(max_length=100)

    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Креирана во:')
    @property
    def session_id(self):
        return self.session
    

    @property
    def possible_number(self):
        order = Order.objects.filter(name__iexact=self.name).first()
        if not order:
            return False
        else:
            return str(order.number)

    
class Abandoned_CartItems(models.Model):
    cart = models.ForeignKey(Abandoned_Carts, on_delete=models.CASCADE, null=True, related_name='abandoned_cartitem_set')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attributename = models.CharField(max_length=100, null = True, default='')
    product_qty = models.IntegerField(null=False, blank=False)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, null = True)
    attributeprice = models.IntegerField(null=True)
    offer_price = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_session(self):
        return self.cart.session

    @property
    def has_attributes(self):
        if(self.attribute is not None):
            return True
        else:
            return False
        
    @property
    def has_offer(self):
        if(self.offer_price is not None):
            return True
        else:
            return False

    class Meta:
        verbose_name = "Abandoned Cart Items"
        verbose_name_plural = "Abandoned Cart Items"
        
        
        
class ProductUpsells(models.Model):
    class Meta:
        verbose_name = "Upsells"
        verbose_name_plural = "Upsells"

    parent_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт на кој да се прикажат', related_name='parent_product', )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Upsell продукт')
    title = models.CharField(max_length = 100, verbose_name='Име')
    thumbnail = ProcessedImageField(upload_to='upsells/%Y/%m/%d/', processors=[ResizeToFill(70,70)], format='WEBP', options={'quality':95}, null=True, verbose_name="Слика", blank=True)
    thumbnail_as_jpeg = ImageSpecField(source='thumbnail',format='JPEG')
    regular_price = models.IntegerField(verbose_name='Стара цена', blank=True, null=True)
    sale_price = models.IntegerField(verbose_name='Цена', blank=True, null=True)
    is_free = models.BooleanField(default=False, blank=True, verbose_name="Бесплатен")
    
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.is_free:
                self.regular_price = 0
                self.sale_price = 0
            else:
                linked_product = Product.objects.get(id=self.product.id)
                if self.regular_price is None:
                    self.regular_price = linked_product.regular_price
                if self.sale_price is None:
                    self.sale_price = linked_product.sale_price
                
        super(ProductUpsells, self).save(*args, **kwargs)
        
        
    def __str__(self):
        return self.title
    
