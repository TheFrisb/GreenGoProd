# Generated by Django 4.1.3 on 2022-11-24 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0094_cartoffers_is_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='is_added',
        ),
    ]
