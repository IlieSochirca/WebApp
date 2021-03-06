# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 08:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('category', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, default=None, max_length=30, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='group',
            name='post',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.GroupPost'),
        ),
    ]
