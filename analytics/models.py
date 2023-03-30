from django.db import models
from shop.models import Product, OrderItem
import datetime
from django.urls import reverse
from django.utils import timezone
import os
# Create your models here.


class daily_items(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Продукт')
    slug =  models.SlugField(unique=True, max_length=250, blank = True, null=True)

    def get_absolute_url(self):
        return reverse('daily_ad_spend_by_id', args=[str(self.slug)])
    
    def __str__(self):
        return 'Item - {} {}'.format(self.product.sku, self.slug)


class daily_row(models.Model):
    owner = models.ForeignKey(daily_items, on_delete=models.SET_NULL, null=True, verbose_name='Дневен ред на информации')
    quantity = models.IntegerField(verbose_name='Количина', null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена на продукт', null=True, blank=True,)
    neto_price = models.IntegerField(verbose_name='Нето вредност', null=True, blank=True,)
    stock_price = models.IntegerField(verbose_name='Набавка', null=True, blank=True,)
    fixed_cost = models.IntegerField(verbose_name='Фиксен трошок', null=True, blank=True)
    ad_cost = models.FloatField(verbose_name='Трошок за реклама', null=True, blank=True,)
    neto_total = models.IntegerField(verbose_name='NETO total', null=True, blank=True)
    profit = models.IntegerField(verbose_name='Профит(ЌЕШ)', null=True, blank=True,)
    cost_per_purchase = models.FloatField(verbose_name='Cost per purchase', null=True, blank=True,)
    be_roas = models.FloatField(verbose_name='BE ROAS', null=True, blank=True,)
    roas = models.FloatField(verbose_name='ROAS', null=True,  blank=True,)
    roi = models.FloatField(verbose_name='ROI', null=True)
    comment = models.TextField(null=True, blank=True, verbose_name='Коментар')

    created_at = models.DateTimeField(default=timezone.now, editable=True, verbose_name='Креиран во')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Упдејтиран/Импортиран во')


    def save(self, *args, **kwargs):
        if self.pk is None:
           pass
        else:
            self.neto_total = self.quantity * self.neto_price
            self.profit = self.neto_total - self.ad_cost
            if(self.quantity != 0):
                self.cost_per_purchase = self.ad_cost / self.quantity
            else:
                self.cost_per_purchase = self.ad_cost
            self.be_roas = self.price / self.neto_price
            if(self.ad_cost!=0):
                self.roas = (self.quantity * self.price) / (self.ad_cost)
                self.roi = (self.neto_price * self.quantity) / (self.ad_cost)
            else:
                self.roas = (self.quantity * self.price)
                self.roi = (self.neto_price * self.quantity)
            print('Save called')
        super(daily_row, self).save(*args, **kwargs)



    def __str__(self):
        return 'Daily row за - {} - {}'.format(self.owner, self.created_at)


    
class ad(models.Model):
    main_image = models.ImageField(upload_to='campaigns/ads/ad_images/%Y/%m/%d/', null=True, verbose_name='Слика на реклама')
    main_video = models.FileField(upload_to='campaigns/ads/ad_videos/%Y/%m/%d/', null=True, verbose_name='Видео на реклама')
    video_thumbnail = models.ImageField(upload_to='campaigns/ads/ad_videos/thumbnails/%Y/%m/%d/', null=True, verbose_name='Thumbnail на видео')
    main_video_link = models.TextField(null=True, blank=True, verbose_name='Видео линк')
    @property
    def video_filename(self):
        return str(os.path.basename(self.main_video.name))
    
