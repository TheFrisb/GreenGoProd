# Generated by Django 4.1.3 on 2022-11-23 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0079_rename_cart_cartitems_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.CharField(max_length=150),
        ),
    ]
