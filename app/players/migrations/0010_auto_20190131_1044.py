# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-31 05:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20190130_1137'),
        ('players', '0009_auto_20190128_1218'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('user_id', 'player_id', 'tour_start')]),
        ),
    ]
