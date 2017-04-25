from django.test import TestCase
from .models import Tutorial


class TestLoadTutorials(TestCase):
    """ Unit test suite for testing that initial data of
    Tutorials is created
    """

    def test_tutorials_created(self):
        """ Checks that this method __str__ method returns the name
        of the object.
        """
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo hacer login por primera vez?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo hacer login por primera vez?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo hacer login a la página?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo hacer logout de la página?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo recuperar tu contraseña?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo crear un nuevo usuario?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo editar un nuevo usuario?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo funciona la pestaña de estudios?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo buscar a un niño?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo buscar a una familia?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo editar un nuevo usuario?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo retroalimentar un estudio?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo aprovar un estudio?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo asignar una beca?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo reasignar una beca?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo generar la carta de beca de un niño?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Creación de un nuevo estudio socioeconómico?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo llenar al sección de integrantes?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo llenar los egresos e ingresos?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo subir las imágenes de la vivienda?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo llenar el resto del estudio socioeconómico?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo subir el estudio a revisión?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo lidear con el proceso de retroalimentación?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Que significan los diferentes estados del estudio socioeconómico?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo descargar el resumen completo de información de la plataforma?'))
        self.assertTrue(Tutorial.objects.get(titulo='¿Cómo marcar un alumno que ha empezado el proceso de reinscripción?'))
