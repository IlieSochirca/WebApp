# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0035_auto_20171020_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='added_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Profile'),
        ),
    ]
