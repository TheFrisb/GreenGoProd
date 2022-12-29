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
    thumbnail = ProcessedImageField(upload_to='products/%Y/%m/%d/', processors=[ResizeToFill(550,550)], format='WEBP', options={'quality':85}, null=True)
    thumbnail_loop = ImageSpecField(source='thumbnail', processors=[ResizeToFill(250,250)], format='WEBP', options={'quality':80})
    
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
    fake_quantity = models.IntegerField(default=randint(2, 20))
    review_average = models.IntegerField(default=0)
    #Product Data

    supplier = models.ForeignKey(Dobavuvac, on_delete=models.CASCADE, verbose_name='Добавувач')
    sku = models.CharField(max_length = 100, verbose_name='Лабел')
    

    def save(self, *args, **kwargs):
        self.slug = self.title_slug
        self.fake_quantity = randint(2, 20)
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


    def get_absolute_url(self):
        return reverse('product-page', kwargs={'slug': self.slug})


class ProductGallery(models.Model):
    class Meta:
        verbose_name = "Галерија"
        verbose_name_plural = "Галерии"


    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    galleryimg = ProcessedImageField(upload_to='products/product-gallery/%Y/%m/%d/', processors=[ResizeToFill(550,550)], format='WEBP', options={'quality':75}, null=True, verbose_name='Слика за галерија')


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
    color = models.ForeignKey(Color , on_delete=models.SET_NULL,  null = True, blank=True, verbose_name='Боја')
    size = models.ForeignKey(Size, on_delete = models.SET_NULL,  null = True, blank=True, verbose_name='Големина')
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL,  null = True, blank=True, verbose_name='Понуда')
    price = models.IntegerField(blank=True, null=True, verbose_name='Цена')
    label = models.CharField(max_length=50, null=True, verbose_name='Лабел')

    @property
    def checkattribute(self):
        if(self.color is not None):
            return self.color.title

        if(self.size is not None):
            return self.size.title
## FIIIIIIIX
        if(self.offer is not None):
            return self.offer.title

        return 1

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
    image = ProcessedImageField(upload_to='review/%Y/%m/%d/', processors=[ResizeToFit(width=400, upscale=False)], format='WEBP', options={'quality':85}, null=True, blank=True)
    image2 = ProcessedImageField(upload_to='review/%Y/%m/%d/', processors=[ResizeToFit(width=400, upscale=False)], format='WEBP', options={'quality':85}, null=True, blank=True)

    name = models.CharField(max_length=150, verbose_name='Име на reviewer')
    content = models.TextField(verbose_name='Содржина', blank=True, null = Ture) 
    rating = models.CharField(choices=rating_choices, default='5', verbose_name='Оценка', max_length=5)
    date_created = models.DateField(auto_now=True)
        

    def __str__(self):
        return 'Review за продукт: {} со име: {} и оценка: {}'.format(self.product.title,self.name, self.rating)


    @property
    def Product_Title(self):
        return self.product.title


class Cart(models.Model):
    session = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)

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
    is_thankyou_offer = models.BooleanField(default = False)
    
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
