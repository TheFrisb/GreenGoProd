# Generated by Django 4.1.3 on 2022-11-24 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0105_delete_cartoffersadded'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='label',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
