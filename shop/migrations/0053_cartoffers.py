# Generated by Django 4.1.3 on 2022-11-22 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0052_alter_product_desc2'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartOffers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_text', models.CharField(blank=True, max_length=40, verbose_name='Текст на понуда')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Одбери продукт')),
            ],
            options={
                'verbose_name': 'Понуди за кошничка',
                'verbose_name_plural': 'Понуди за кошничка',
            },
        ),
    ]
