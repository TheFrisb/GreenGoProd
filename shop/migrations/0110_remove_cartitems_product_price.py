# Generated by Django 4.1.3 on 2022-11-24 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0109_cartitems_attribute_cartitems_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='product_price',
        ),
    ]
