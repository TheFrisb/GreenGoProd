# Generated by Django 4.1.3 on 2022-11-22 14:40

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0050_productgallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='desc2',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
