# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Sacramento = apps.get_model('familias', 'Sacramento')
    db_alias = schema_editor.connection.alias
    Sacramento.objects.using(db_alias).bulk_create([
        Sacramento(nombre='Bautismo'),
        Sacramento(nombre='Comunión'),
        Sacramento(nombre='Confirmación'),
        Sacramento(nombre='Matrimonio'),
    ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    Sacramento = apps.get_model('familias', 'Sacramento')
    db_alias = schema_editor.connection.alias
    Sacramento.objects.using(db_alias).filter(nombre='Bautismo').delete()
    Sacramento.objects.using(db_alias).filter(nombre='Comunión').delete()
    Sacramento.objects.using(db_alias).filter(nombre='Confirmación').delete()
    Sacramento.objects.using(db_alias).filter(nombre='Matrimonio').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0038_auto_20170702_0514'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
