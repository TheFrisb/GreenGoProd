# Generated by Django 4.1.3 on 2022-11-24 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0087_rename_orderfees_checkoutfees_orderfeesitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shipping_price',
            field=models.IntegerField(blank=True, default=130),
        ),
    ]
