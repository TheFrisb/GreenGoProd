# Generated by Django 4.1.3 on 2022-11-19 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0040_remove_productattribute_size_product_has_attributes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='has_attributes',
        ),
        migrations.AddField(
            model_name='product',
            name='attributes_type',
            field=models.CharField(blank=True, max_length=50, verbose_name=(('COLOR', 'COLOR'), ('SIZE', 'SIZE'), ('OFFER', 'OFFER'))),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('PRIVATE', 'PRIVATE'), ('PUBLISHED', 'PUBLISHED'), ('VARIABLE', 'VARIABLE')], default='PRIVATE', max_length=50, verbose_name='СТАТУС'),
        ),
    ]
