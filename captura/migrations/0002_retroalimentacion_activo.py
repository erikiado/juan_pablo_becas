# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-26 02:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('captura', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='retroalimentacion',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
