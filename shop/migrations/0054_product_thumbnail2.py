# Generated by Django 4.1.3 on 2022-11-23 02:00

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0053_cartoffers'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='thumbnail2',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[600, 600], upload_to='products/'),
        ),
    ]
