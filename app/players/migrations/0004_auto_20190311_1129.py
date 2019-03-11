# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-11 06:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_auto_20190311_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result_players',
            name='player_id',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='players.Player'),
        ),
        migrations.AlterField(
            model_name='result_players',
            name='points',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='result_players',
            name='tour_number',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='players.Tour'),
        ),
        migrations.AlterField(
            model_name='result_profiles',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='result_profiles',
            name='tour_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.Tour'),
        ),
        migrations.AlterField(
            model_name='result_profiles',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
    ]
