# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 15:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0021_auto_20171015_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_user_likes',
            field=models.ManyToManyField(related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]