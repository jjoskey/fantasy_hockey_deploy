# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-14 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20190312_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='budget',
            field=models.FloatField(default=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='team_name',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
