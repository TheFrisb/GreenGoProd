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
# Create your models here.

def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('products/', filename)

class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False, verbose_name='Име на категорија')

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, verbose_name='Категорија')
    thumbnail = models.ImageField(default='default.jpg', upload_to='products/')
    title = models.CharField(max_length = 100, verbose_name='Име')
    content = models.TextField(verbose_name='Детален опис')
    regular_price = models.IntegerField(verbose_name='Стара цена')
    sale_price = models.IntegerField(verbose_name='Цена')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата на креирање')
    title_slug = models.CharField(max_length = 100,verbose_name='Име на продукт во латиница')
    slug =  models.SlugField(unique=True, max_length=250, blank = True)
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Залиха')
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
    desc2 = RichTextUploadingField(blank=True, null=True);
    attributes_type = models.CharField(choices=attributes_choices, max_length=50, blank=True)
    status = models.CharField( choices=status_choices, default = 'PRIVATE', max_length=50, verbose_name='СТАТУС')
    #Product Data
    supplier = models.ForeignKey(Dobavuvac, on_delete=models.CASCADE, verbose_name='Добавувач')
    sku = models.CharField(max_length = 100, verbose_name='Лабел')
    free_shipping = models.BooleanField(default=False, blank=True, verbose_name='Бесплатна достава')
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_slug)
        
        super(Product, self).save(*args, **kwargs)
        
        
    #Kak da kreiram variabilni produkti ( po golemina, boja? )
    # Kak da kreiram kopijja od thumbnail samo u pomalecok size 150px 150px i da ga storiram u field
    # How to display in admin panel da gi pokazuva order items ?
    # how to add product galerija array od imgs za product page
    # Kak da kreiram xlsx file od admin panelo i dali ima potreba da e od admin panelo?

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-page', kwargs={'slug': self.slug})

    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    galleryimg = models.ImageField(default='default.jpg', upload_to='products/product-gallery/')


class Color(models.Model):
    title = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    def __str__(self):
        return '{}  -  {}'.format(self.title, self.color_code)


class Size(models.Model):
    title = models.CharField(max_length=100, blank=True)
    #color_code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title


class Offer(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    incentive = models.CharField(max_length=100, blank=True)

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color , on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete = models.CASCADE, null = True, blank= True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(blank=True)

    def __str__(self):
        return 'Атрибут за {} - {} - {}'.format(self.product, self.color, self.price)
    



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, verbose_name='Продукт')
    image = models.ImageField(upload_to='reviews/', verbose_name='Слика')
    name = models.CharField(max_length=150, verbose_name='Име на reviewer')
    content = models.TextField(verbose_name='Содржина')
    rating_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    rating = models.CharField(choices=rating_choices, default='5', verbose_name='Оценка', max_length=5)


    date_created = models.DateField(auto_now=True)
        

    def __str__(self):
        return 'Review за продукт: {} со име: {} и оценка: {}'.format(self.product.title,self.name, self.rating)




    @property
    def Product_Title(self):
        return self.product.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, verbose_name='Име')
    address = models.CharField(max_length=150, null=False, verbose_name='Адреса')
    city = models.CharField(max_length=150, null=False, verbose_name='Град')
    number = models.CharField(max_length=150, null=False, verbose_name='Број')
    total_price = models.IntegerField(null=False, verbose_name='Вкупна цена')
    shipping = models.BooleanField(default=True, verbose_name='Достава')
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    price = models.FloatField(null=False, verbose_name='Цена')
    quantity = models.IntegerField(null=False, verbose_name='Количина')


    @property
    def get_product_total(self):
        return self.price*self.quantity

    def __str__(self):
        return '--- {}({} ден) х {} - Вкупно {} ден'.format(self.product, self.price, self.quantity, self.get_product_total)















