# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0012_auto_20171006_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
