# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0042_auto_20171024_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='/media/media/images/avatar.png', upload_to='media/images'),
        ),
    ]
