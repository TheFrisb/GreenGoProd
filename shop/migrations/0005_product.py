# Generated by Django 4.1.3 on 2022-11-15 16:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_delete_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumnail', models.ImageField(default='default.jpg', upload_to='products/')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('regular_price', models.IntegerField()),
                ('sale_price', models.IntegerField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('quantity', models.IntegerField()),
                ('supplier', models.CharField(max_length=100)),
                ('sku', models.CharField(max_length=100)),
                ('free_shipping', models.BooleanField(default=False, null=True)),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
        ),
    ]
