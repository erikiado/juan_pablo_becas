# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-29 01:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0017_auto_20170328_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familia',
            name='estado_civil',
            field=models.CharField(choices=[('soltero', 'Soltero'), ('viudo', 'Viudo'), ('union_libre', 'Unión Libre'), ('casado_civil', 'Casado-Civil'), ('casado_iglesia', 'Casado-Iglesia'), ('vuelto_a_casar', 'Divorciado Vuelto a Casar')], max_length=100),
        ),
        migrations.AlterField(
            model_name='familia',
            name='localidad',
            field=models.CharField(choices=[('poblado_jurica', 'Poblado Juríca'), ('nabo', 'Nabo'), ('salitre', 'Salitre'), ('la_campana', 'La Campana'), ('otro', 'Otro')], max_length=100),
        ),
        migrations.AlterField(
            model_name='familia',
            name='numero_hijos_diferentes_papas',
            field=models.IntegerField(),
        ),
    ]
