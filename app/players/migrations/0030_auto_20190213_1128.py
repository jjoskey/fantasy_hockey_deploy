# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-13 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0029_team_temporary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
