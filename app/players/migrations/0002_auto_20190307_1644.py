# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-07 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='points',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]