# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Oficio = apps.get_model('familias', 'Oficio')
    db_alias = schema_editor.connection.alias
    Oficio.objects.using(db_alias).bulk_create([
        Oficio(nombre='Estudiante'),
    ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    Oficio = apps.get_model('familias', 'Oficio')
    db_alias = schema_editor.connection.alias
    Oficio.objects.using(db_alias).filter(nombre='Estudiante').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0033_auto_20170429_2310'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]