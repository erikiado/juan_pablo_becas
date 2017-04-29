# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Escuela = apps.get_model('administracion', 'Escuela')
    db_alias = schema_editor.connection.alias
    Escuela.objects.using(db_alias).bulk_create([
        Escuela(nombre='Plantel Jurica'),
        Escuela(nombre='Plantel Buenavista'),
    ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    Escuela = apps.get_model('indicadores', 'Escuela')
    db_alias = schema_editor.connection.alias
    Escuela.objects.using(db_alias).filter(nombre='Plantel Jurica').delete()
    Escuela.objects.using(db_alias).filter(nombre='Plantel Buenavista').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]