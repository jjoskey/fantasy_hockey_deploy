# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-19 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0009_auto_20190314_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result_players',
            name='points',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='result_profiles',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]