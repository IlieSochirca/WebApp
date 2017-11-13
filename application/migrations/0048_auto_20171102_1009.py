# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-02 08:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0047_group_follower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='follower',
            field=models.ManyToManyField(blank=True, default=0, related_name='follow', to=settings.AUTH_USER_MODEL),
        ),
    ]