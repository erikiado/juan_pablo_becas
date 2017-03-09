from django.test import TestCase
from .models import Escuela


class TestEscuela(TestCase):
    """ Unit test suite for testing the Escuela model in .models
    """

    def setUp(self):
        """ Setup required for the tests in this suite.

        """
        Escuela.objects.create(nombre='San Juan Pablo')

    def test_str(self):
        """ Checks that this method __str__ method returns the name
        of the object.
        """
        escuela = Escuela.objects.get(nombre='San Juan Pablo')
        self.assertTrue(str(escuela) == 'San Juan Pablo')
