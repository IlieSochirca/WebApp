# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-02 07:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0046_auto_20171030_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='follower',
            field=models.ManyToManyField(related_name='follow', to=settings.AUTH_USER_MODEL),
        ),
    ]