# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0040_auto_20171024_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='media/images'),
        ),
    ]
