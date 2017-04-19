# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.models import Group
from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, \
                                   DIRECTIVO_GROUP, SERVICIOS_ESCOLARES_GROUP

def forwards_func(apps, schema_editor):
    """ Create all the required groups in the database.

    """
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).get_or_create(name=ADMINISTRADOR_GROUP)
    Group.objects.using(db_alias).get_or_create(name=CAPTURISTA_GROUP)
    Group.objects.using(db_alias).get_or_create(name=DIRECTIVO_GROUP)
    Group.objects.using(db_alias).get_or_create(name=SERVICIOS_ESCOLARES_GROUP)

def reverse_func(apps, schema_editor):
    """ Revert changes made in forwards_func
    """
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).filter(name=ADMINISTRADOR_GROUP).delete()
    Group.objects.using(db_alias).filter(name=CAPTURISTA_GROUP).delete()
    Group.objects.using(db_alias).filter(name=DIRECTIVO_GROUP).delete()
    Group.objects.using(db_alias).filter(name=SERVICIOS_ESCOLARES_GROUP).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('perfiles_usuario', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]