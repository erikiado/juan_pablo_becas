# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Oficio = apps.get_model('familias', 'Oficio')
    db_alias = schema_editor.connection.alias
    Oficio.objects.using(db_alias).bulk_create([
        Oficio(nombre='Empleado'),
        Oficio(nombre='Obrero'),
        Oficio(nombre='Jefe de línea'),
        Oficio(nombre='Área de limpieza'),
        Oficio(nombre='Administrativo'),
        Oficio(nombre='Empleada doméstica'),
        Oficio(nombre='Jardinero'),
        Oficio(nombre='Plomero'),
        Oficio(nombre='Herrero'),
        Oficio(nombre='Carpintero'),
        Oficio(nombre='Albañil'),
        Oficio(nombre='Pintor'),
        Oficio(nombre='Mesero'),
        Oficio(nombre='Negocio propio'),
        Oficio(nombre='Comerciante'),
        Oficio(nombre='Venta de productos'),
        Oficio(nombre='Otro'),
    ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    Oficio = apps.get_model('familias', 'Oficio')
    db_alias = schema_editor.connection.alias
    Oficio.objects.using(db_alias).filter(nombre='Empleado').delete()
    Oficio.objects.using(db_alias).filter(nombre='Obrero').delete()
    Oficio.objects.using(db_alias).filter(nombre='Jefe de línea').delete()
    Oficio.objects.using(db_alias).filter(nombre='Área de limpieza').delete()
    Oficio.objects.using(db_alias).filter(nombre='Administrativo').delete()
    Oficio.objects.using(db_alias).filter(nombre='Empleada doméstica').delete()
    Oficio.objects.using(db_alias).filter(nombre='Jardinero').delete()
    Oficio.objects.using(db_alias).filter(nombre='Plomero').delete()
    Oficio.objects.using(db_alias).filter(nombre='Carpintero').delete()
    Oficio.objects.using(db_alias).filter(nombre='Herrero').delete()
    Oficio.objects.using(db_alias).filter(nombre='Albañil').delete()
    Oficio.objects.using(db_alias).filter(nombre='Pintor').delete()
    Oficio.objects.using(db_alias).filter(nombre='Mesero').delete()
    Oficio.objects.using(db_alias).filter(nombre='Negocio propio').delete()
    Oficio.objects.using(db_alias).filter(nombre='Comerciante').delete()
    Oficio.objects.using(db_alias).filter(nombre='Venta de productos').delete()
    Oficio.objects.using(db_alias).filter(nombre='Otro').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('familias', '0027_auto_20170425_1411'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]