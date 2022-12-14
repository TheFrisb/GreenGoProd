# Generated by Django 4.1.3 on 2022-11-19 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0046_remove_size_color_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.color'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.size'),
        ),
    ]
