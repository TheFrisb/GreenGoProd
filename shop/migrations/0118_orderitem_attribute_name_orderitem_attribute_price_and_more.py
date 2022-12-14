# Generated by Django 4.1.3 on 2022-11-25 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0117_cartitems_attributeprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='attribute_name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='attribute_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.color'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.offer'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.size'),
        ),
    ]
