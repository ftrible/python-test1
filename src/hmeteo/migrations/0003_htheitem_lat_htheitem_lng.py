# Generated by Django 5.0.1 on 2024-01-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmeteo', '0002_rename_theitem_htheitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='htheitem',
            name='lat',
            field=models.FloatField(editable=False, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='htheitem',
            name='lng',
            field=models.FloatField(editable=False, null=True, verbose_name='Longitude'),
        ),
    ]
