from django.test import TestCase
from .models import Oficio, Sacramento


class TestLoadOficios(TestCase):
    """ Unit test suite for testing that initial data of
    periodos is created
    """

    def test_oficios_created(self):
        """ Checks that all the original oficios where loaded correctly.
        """
        self.assertTrue(Oficio.objects.get(nombre='Empleado'))
        self.assertTrue(Oficio.objects.get(nombre='Obrero'))
        self.assertTrue(Oficio.objects.get(nombre='Jefe de línea'))
        self.assertTrue(Oficio.objects.get(nombre='Área de limpieza'))
        self.assertTrue(Oficio.objects.get(nombre='Administrativo'))
        self.assertTrue(Oficio.objects.get(nombre='Empleada doméstica'))
        self.assertTrue(Oficio.objects.get(nombre='Jardinero'))
        self.assertTrue(Oficio.objects.get(nombre='Plomero'))
        self.assertTrue(Oficio.objects.get(nombre='Herrero'))
        self.assertTrue(Oficio.objects.get(nombre='Carpintero'))
        self.assertTrue(Oficio.objects.get(nombre='Albañil'))
        self.assertTrue(Oficio.objects.get(nombre='Pintor'))
        self.assertTrue(Oficio.objects.get(nombre='Mesero'))
        self.assertTrue(Oficio.objects.get(nombre='Negocio propio'))
        self.assertTrue(Oficio.objects.get(nombre='Comerciante'))
        self.assertTrue(Oficio.objects.get(nombre='Venta de productos'))
        self.assertTrue(Oficio.objects.get(nombre='Otro'))

    def test_oficio_estudiante_added(self):
        """ Check that the option to use estudiante as oficio has been added
        """

        self.assertTrue(Oficio.objects.get(nombre='Estudiante'))


class TestLoadSacramentos(TestCase):
    """ Unit test suite for testing that initial data of
    sacramentos is created
    """

    def test_sacramentos_created(self):
        """ Checks that all the original sacramentos where loaded correctly.
        """
        self.assertTrue(Sacramento.objects.get(nombre='Bautismo'))
        self.assertTrue(Sacramento.objects.get(nombre='Comunión'))
        self.assertTrue(Sacramento.objects.get(nombre='Confirmación'))
        self.assertTrue(Sacramento.objects.get(nombre='Matrimonio'))
