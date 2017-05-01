from django.test import TestCase
from .models import Escuela


class TestLoadEscuelas(TestCase):
    """ Unit test suite for testing that initial data of
    schools is created
    """

    def test_escuelas_created(self):
        """ Checks that this method __str__ method returns the name
        of the object.
        """
        self.assertTrue(Escuela.objects.get(nombre='Plantel Jurica'))
        self.assertTrue(Escuela.objects.get(nombre='Plantel Buenavista'))
