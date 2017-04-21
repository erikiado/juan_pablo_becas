from django.test import TestCase
from .models import Escuela, Colegiatura


class TestModels(TestCase):
    """ Unit test suite for testing the models.
    """

    def setUp(self):
        """ Setup required for the tests in this suite.

        """
        Escuela.objects.create(nombre='San Juan Pablo')

    def test_str_escuela(self):
        """ Checks that this method __str__ method returns the name
        of the object.
        """
        escuela = Escuela.objects.get(nombre='San Juan Pablo')
        self.assertTrue(str(escuela) == 'San Juan Pablo')

    def test_str_colegiatura(self):
        """ check __str__ of Colegiatura

        """
        colegiatura = Colegiatura.objects.create(monto=1700.00)
        self.assertEqual(str(colegiatura), '1700.00')

    def test_migration(self):
        """  test that the migration is adding the element.

        """
        colegiatura = Colegiatura.objects.all()
        self.assertEqual(len(colegiatura), 1)
        self.assertEqual(str(colegiatura[0]), '1500.00')
