# Generated by Django 5.0.1 on 2024-01-16 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmeteo', '0003_htheitem_lat_htheitem_lng'),
    ]

    operations = [
        migrations.AlterField(
            model_name='htheitem',
            name='lat',
            field=models.FloatField(null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='htheitem',
            name='lng',
            field=models.FloatField(null=True, verbose_name='Longitude'),
        ),
    ]
