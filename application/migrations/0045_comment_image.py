# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0044_auto_20171024_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
