# Generated by Django 4.1.3 on 2022-11-30 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0128_category_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartoffers',
            name='price',
            field=models.IntegerField(default=10, verbose_name='Цена'),
            preserve_default=False,
        ),
    ]
