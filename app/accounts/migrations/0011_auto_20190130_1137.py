# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-30 06:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_profile_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='budget',
            field=models.PositiveIntegerField(default=7000000),
        ),
    ]
