# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-05 06:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20190221_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]