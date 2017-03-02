from django.test import TestCase
from .models import Pregunta, Seccion, Subseccion
from .load import load_data


class TestLoadPreguntas(TestCase):
    """ Suite to test the script to load questions.

    """

    def test_load_preguntas(self):
        """ Test that the script to load questions works properly.

        We assert that the number of objects inserted is the same as we
        expect.
        """
        load_data()
        self.assertEqual(142, len(Pregunta.objects.all()))
        self.assertEqual(7, len(Seccion.objects.all()))
        self.assertEqual(18, len(Subseccion.objects.all()))
