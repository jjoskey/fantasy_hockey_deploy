# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-07 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='team_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
