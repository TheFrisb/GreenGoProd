# Generated by Django 4.1.3 on 2022-11-17 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
