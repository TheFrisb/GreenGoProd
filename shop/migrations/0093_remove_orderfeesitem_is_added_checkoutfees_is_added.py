# Generated by Django 4.1.3 on 2022-11-24 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0092_orderfeesitem_is_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderfeesitem',
            name='is_added',
        ),
        migrations.AddField(
            model_name='checkoutfees',
            name='is_added',
            field=models.BooleanField(default=False),
        ),
    ]
