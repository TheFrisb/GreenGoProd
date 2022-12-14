# Generated by Django 4.1.3 on 2022-11-30 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0129_cartoffers_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='offerprice',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartoffers',
            name='is_added',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_slug',
            field=models.CharField(max_length=100, verbose_name='Url исто како на другио Website'),
        ),
    ]
