# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-29 21:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0029_auto_20170429_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='familia',
            name='offline_id',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
