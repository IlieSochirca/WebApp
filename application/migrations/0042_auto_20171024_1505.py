# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0041_auto_20171024_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='/media/images/avatar.png', upload_to='media/images'),
        ),
    ]
