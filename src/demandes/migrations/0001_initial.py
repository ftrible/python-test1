# Generated by Django 5.0.1 on 2025-02-25 18:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Demandes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=144)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('publish_date', models.DateTimeField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demandes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-publish_date', '-updated', '-timestamp'],
            },
        ),
    ]
