# Generated by Django 4.1.3 on 2022-11-15 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_product_thumbnail'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
