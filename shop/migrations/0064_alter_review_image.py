# Generated by Django 4.1.3 on 2022-11-23 02:51

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0063_remove_product_desc2_alter_product_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to='review/'),
        ),
    ]
