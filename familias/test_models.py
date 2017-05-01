from django.test import TestCase
from .models import Familia, Oficio


class TestFamiliaModel(TestCase):
    """ Unit test suite for testing the Beca model in .models
    """

    def setUp(self):
        """ Setup required for the tests in this suite.

        """
        self.familia = Familia.objects.create(nombre_familiar='Molina',
                                              numero_hijos_diferentes_papas=2,
                                              estado_civil='soltero',
                                              localidad='Nabo')

    def test_str_familia_con_alumno(self):
        """ Checks that this method __str__ method returns the name
        of the object.
        """
        self.assertEqual(str(self.familia), 'Molina')


class TestOficio(TestCase):
    """ Unit test suite for testing the Oficio model in .models

    """

    def setUp(self):
        """ Setup required for all the tests in this suite.

        This setup creates a new Oficio object.
        """
        self.nombre = 'Electricista'
        Oficio.objects.create(nombre=self.nombre)

    def test_str(self):
        """ Test for the oficio __str__ method.

        This tests that it returns the name of the oficio.
        """
        oficio = Oficio.objects.get(nombre=self.nombre)
        self.assertEqual(str(oficio), self.nombre)
