# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-12 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_adbanners_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='adbanners',
            name='large_image',
            field=models.ImageField(blank=True, null=True, upload_to='banners/'),
        ),
        migrations.AddField(
            model_name='adbanners',
            name='medium_image',
            field=models.ImageField(blank=True, null=True, upload_to='banners/'),
        ),
    ]