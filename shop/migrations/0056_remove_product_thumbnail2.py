# Generated by Django 4.1.3 on 2022-11-23 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0055_alter_product_thumbnail2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='thumbnail2',
        ),
    ]
