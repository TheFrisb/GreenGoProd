# Generated by Django 4.1.3 on 2022-11-19 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0038_color_size_productattribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattribute',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.size'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='price',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
