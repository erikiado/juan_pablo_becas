# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Tutorial = apps.get_model('base', 'Tutorial')
    db_alias = schema_editor.connection.alias
    Tutorial.objects.using(db_alias).bulk_create([
        Tutorial(titulo='¿Cómo hacer login por primera vez?',
                 descripcion='En este tutorial se muestra cómo hacer login una vez que el administrador crea tu cuenta.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='general'),
        Tutorial(titulo='¿Cómo hacer login a la página?',
                 descripcion='En este tutorial se muestra cómo entrar a tu cuenta.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='general'),
        Tutorial(titulo='¿Cómo hacer logout de la página?',
                 descripcion='En este tutorial se muestra cómo cerrar tu sesión.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='general'),
        Tutorial(titulo='¿Cómo recuperar tu contraseña?',
                 descripcion='En este tutorial se muestra cómo recuparar tu contraseña, en caso de que sea olvidada.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='general'),

        # Carga de sección de administración
        Tutorial(titulo='¿Cómo crear un nuevo usuario?',
                 descripcion='En este tutorial se muestra cómo crear un nuevo usuario.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='administracion'),
        Tutorial(titulo='¿Cómo editar un nuevo usuario?',
                 descripcion='En este tutorial se muestra editar un nuevo usuario.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='administracion'),
        Tutorial(titulo='¿Cómo funciona la pestaña de estudios?',
                 descripcion='En este tutorial se explica cómo funciona la pestaña de estudios en el panel de administracion.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='administracion'),
        Tutorial(titulo='¿Cómo buscar a un niño?',
                 descripcion='Se muestran las diferentes formas de encontrar a un niño y la información que se obtiene.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='administracion'),
        Tutorial(titulo='¿Cómo buscar a una familia?',
                 descripcion='En este tutorial se muestran las formas de encontrar una familia y la información que se obtiene.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='administracion'),
        Tutorial(titulo='¿Cómo retroalimentar un estudio?',
                 descripcion='En este tutorial se muestra cómo rechazar y retroalimentar un estudio.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='administracion'),
        Tutorial(titulo='¿Cómo aprobar un estudio?',
                 descripcion='En este tutorial se muestra cómo aprobar un estudio y los cambios que genera.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='administracion'),
        Tutorial(titulo='¿Cómo asignar una beca?',
                 descripcion='En este tutorial se muestra cómo se le otorga una beca a la familia.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='administracion'),
        Tutorial(titulo='¿Cómo reasignar una beca?',
                 descripcion='En este tutorial se muestra cambiar la beca de una familia.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='administracion'),
        Tutorial(titulo='¿Cómo generar la carta de beca de un niño?',
                 descripcion='En este tutorial se muestra cómo crear la carta de beca para un alumno.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='administracion'),

        # Carga de sección de capturista
        Tutorial(titulo='¿Creación de un nuevo estudio socioeconómico?',
                 descripcion='En este tutorial se muestra cómo crear un nuevo estudio socioeconómico.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='captura'),
        Tutorial(titulo='¿Cómo llenar al sección de integrantes?',
                 descripcion='En este tutorial se muestra cómo llenar la sección de integrantes.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='captura'),
        Tutorial(titulo='¿Cómo llenar los egresos e ingresos?',
                 descripcion='En este tutorial se muestra cómo desglosar los egresos e ingresos de la familia.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='captura'),
        Tutorial(titulo='¿Cómo subir las imágenes de la vivienda?',
                 descripcion='En este tutorial se muestra cómo subir las imágenes tomadas de la vivienda.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='captura'),
        Tutorial(titulo='¿Cómo llenar el resto del estudio socioeconómico?',
                 descripcion='En este tutorial se muestra cómo llenar el resto de la información de la familia.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='captura'),
        Tutorial(titulo='¿Cómo subir el estudio a revisión?',
                 descripcion='En este tutorial se muestra cómo subir un estudio socioeconómico, y que hay que checar antes de subirlo.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='captura'),
        Tutorial(titulo='¿Cómo lidiar con el proceso de retroalimentación?',
                 descripcion='En este tutorial se explica cómo funciona el proceso de retroalimentación',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='captura'),
        Tutorial(titulo='¿Qué significan los diferentes estados del estudio socioeconómico?',
                 descripcion='En este tutorial se explica cada uno de los estados y su significado.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='captura'),

        # Carga de sección dirección
        Tutorial(titulo='¿Cómo descargar el resumen completo de información de la plataforma?',
                 descripcion='En este tutorial se muestra cómo descargar un resumen total de los datos de la escuela.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='direccion'),

        # Carga de sección de servicios escolares
        Tutorial(titulo='¿Cómo marcar un alumno que ha empezado el proceso de reinscripción?',
                 descripcion='En este tutorial se muestra cómo marcar que un alumno ha empezado el proceso de reinscripción y requiere una carta de beca.',
                 video='https://www.youtube.com/embed/dQw4w9WgXcQ',
                 seccion='servicios escolares'),
        ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    Tutorial = apps.get_model('base', 'Tutorial')
    db_alias = schema_editor.connection.alias
    # Borrado de sección general
    Tutorial.objects.using(db_alias).filter(periodicidad='¿Cómo hacer login por primera vez?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo hacer login por primera vez?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo hacer login a la página?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo hacer logout de la página?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo recuperar tu contraseña?').delete()

    # Borrado de sección de administración
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo crear un nuevo usuario?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo editar un nuevo usuario?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo funciona la pestaña de estudios?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo buscar a un niño?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo buscar a una familia?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo retroalimentar un estudio?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo aprobar un estudio?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo asignar una beca?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo reasignar una beca?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo generar la carta de beca de un niño?').delete()

    # Borrado de sección de capturista
    Tutorial.objects.using(db_alias).filter(titulo='¿Creación de un nuevo estudio socioeconómico?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo llenar al sección de integrantes?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo llenar los egresos e ingresos?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo subir las imágenes de la vivienda?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo llenar el resto del estudio socioeconómico?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo subir el estudio a revisión?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo lidiar con el proceso de retroalimentación?').delete()
    Tutorial.objects.using(db_alias).filter(titulo='¿Qué significan los diferentes estados del estudio socioeconómico?').delete()

    # Borrado de sección de dirección
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo descargar el resumen completo de información de la plataforma?').delete()

    # Borrado de sección de servicios escolares
    Tutorial.objects.using(db_alias).filter(titulo='¿Cómo marcar un alumno que ha empezado el proceso de reinscripción?').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]