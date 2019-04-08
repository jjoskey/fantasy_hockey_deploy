# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-01 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20190329_0737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='refresh_changes',
        ),
        migrations.AlterField(
            model_name='profile',
            name='budget',
            field=models.FloatField(default=100, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='changes_count',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='points',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]