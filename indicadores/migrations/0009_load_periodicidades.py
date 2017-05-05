# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Periodo = apps.get_model('indicadores', 'Periodo')
    db_alias = schema_editor.connection.alias
    Periodo.objects.using(db_alias).bulk_create([
        Periodo(periodicidad='Diario', factor=30, multiplica=True),
        Periodo(periodicidad='Semanal', factor=4.3, multiplica=True),
        Periodo(periodicidad='Quincenal', factor=2, multiplica=True),
        Periodo(periodicidad='Mensual', factor=1, multiplica=True),
        Periodo(periodicidad='Bimensual', factor=2, multiplica=False),
        Periodo(periodicidad='Trimestral', factor=3, multiplica=False),
        Periodo(periodicidad='Cuatrimestral', factor=4, multiplica=False),
        Periodo(periodicidad='Semestral', factor=6, multiplica=False),
        Periodo(periodicidad='Anual', factor=12, multiplica=False),
    ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    Periodo = apps.get_model('indicadores', 'Periodo')
    db_alias = schema_editor.connection.alias
    Periodo.objects.using(db_alias).filter(periodicidad='Diario', factor=30, multiplica=True).delete()
    Periodo.objects.using(db_alias).filter(periodicidad='Semanal', factor=4, multiplica=True).delete()
    Periodo.objects.using(db_alias).filter(periodicidad='Quincenal', factor=2, multiplica=True).delete()
    Periodo.objects.using(db_alias).filter(periodicidad='Mensual', factor=1, multiplica=True).delete()
    Periodo.objects.using(db_alias).filter(periodicidad='Bimensual', factor=2, multiplica=False).delete()
    Periodo.objects.using(db_alias).filter(periodicidad='Trimestral', factor=3, multiplica=False).delete()
    Periodo.objects.using(db_alias).filter(periodicidad='Cuatrimestral', factor=4, multiplica=False).delete()
    Periodo.objects.using(db_alias).filter(periodicidad='Semestral', factor=6, multiplica=False).delete()
    Periodo.objects.using(db_alias).filter(periodicidad='Anual', factor=12, multiplica=False).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('indicadores', '0008_merge_20170417_2320'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]