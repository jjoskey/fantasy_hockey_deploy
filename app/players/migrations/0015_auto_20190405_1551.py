# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-05 15:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0014_auto_20190405_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='end_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]