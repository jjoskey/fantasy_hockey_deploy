# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-05 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20190404_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='changes_count',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
