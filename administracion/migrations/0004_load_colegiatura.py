# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Colegiatura = apps.get_model('administracion', 'Colegiatura')
    db_alias = schema_editor.connection.alias
    Colegiatura.objects.using(db_alias).bulk_create([
        Colegiatura(monto='1500'),
    ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    Colegiatura = apps.get_model('administracion', 'Colegiatura')
    db_alias = schema_editor.connection.alias
    Colegiatura.objects.using(db_alias).filter(active=True).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0003_colegiatura'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]