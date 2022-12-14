# Generated by Django 4.1.3 on 2022-11-24 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0097_alter_cartitems_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='offers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.cartoffers'),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.cart'),
        ),
    ]
