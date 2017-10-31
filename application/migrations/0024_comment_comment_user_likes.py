# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 08:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0023_auto_20171015_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_user_likes',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
