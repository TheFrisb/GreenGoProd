# Generated by Django 4.1.3 on 2022-11-16 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_rename_product_review_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='image',
            field=models.ImageField(default=0, upload_to='reviews/'),
            preserve_default=False,
        ),
    ]
