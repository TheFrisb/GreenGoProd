# Generated by Django 4.1.3 on 2022-11-27 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0127_remove_cartitems_created_at_remove_order_date_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='published',
            field=models.BooleanField(default=True, verbose_name='Видливост:'),
        ),
    ]
