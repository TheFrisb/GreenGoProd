# Generated by Django 4.1.3 on 2022-11-23 02:40

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0060_remove_review_thumbnail_loop'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='thumbnail2',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to='hehe'),
        ),
    ]
