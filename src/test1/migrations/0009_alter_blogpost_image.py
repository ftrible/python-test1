# Generated by Django 5.0.1 on 2024-01-03 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0008_blogpost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
    ]
