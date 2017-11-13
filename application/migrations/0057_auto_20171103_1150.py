# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-03 09:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0056_auto_20171103_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='follow',
            field=models.ManyToManyField(blank=True, default=None, related_name='follow', to=settings.AUTH_USER_MODEL),
        ),
    ]
