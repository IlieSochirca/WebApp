# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_auto_20171005_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(max_length=150, null=True),
        ),
    ]
