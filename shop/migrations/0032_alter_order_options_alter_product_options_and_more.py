# Generated by Django 4.1.3 on 2022-11-17 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_alter_product_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': [-1], 'verbose_name': 'Порачка', 'verbose_name_plural': 'Порачки'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': [-1], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукти'},
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Категорија'),
        ),
        migrations.AlterField(
            model_name='product',
            name='content',
            field=models.TextField(verbose_name='Детален опис'),
        ),
        migrations.AlterField(
            model_name='product',
            name='free_shipping',
            field=models.BooleanField(blank=True, default=False, verbose_name='Бесплатна достава'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(blank=True, null=True, verbose_name='Залиха'),
        ),
        migrations.AlterField(
            model_name='product',
            name='regular_price',
            field=models.IntegerField(verbose_name='Стара цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.IntegerField(verbose_name='Нова цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=100, verbose_name='Лабел'),
        ),
        migrations.AlterField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.dobavuvac', verbose_name='Добавувач'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Име'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_slug',
            field=models.CharField(max_length=100, verbose_name='Име на продукт во латиница'),
        ),
    ]
