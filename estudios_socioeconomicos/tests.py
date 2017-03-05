from django.test import TestCase
from .models import Pregunta, Seccion, Subseccion, OpcionRespuesta
from .load import load_data


class TestLoadPreguntas(TestCase):
    """ Suite to test the script to load questions.

    """

    def setUp(self):
        load_data()

    def test_load_preguntas(self):
        """ Test that the script to load questions works properly.

        We assert that the number of objects inserted is the same as we
        expect.
        """
        self.assertEqual(140, len(Pregunta.objects.all()))
        self.assertEqual(7, len(Seccion.objects.all()))
        self.assertEqual(18, len(Subseccion.objects.all()))
        self.assertEqual(96, len(OpcionRespuesta.objects.all()))

    def test_no_duplicates(self):
        """ Test that load_data deletes everything before inserting.

        We call the function again and assert that the counts are the same
        as above.
        """
        load_data()
        self.assertEqual(140, len(Pregunta.objects.all()))
        self.assertEqual(7, len(Seccion.objects.all()))
        self.assertEqual(18, len(Subseccion.objects.all()))
        self.assertEqual(96, len(OpcionRespuesta.objects.all()))

    def test_opciones(self):
        """ Test that a particular questions has options assigned.

        We assert that the number of options for the question 'El piso es de:'
        is 4.
        """
        p = Pregunta.objects.get(texto='El piso es de:')
        opts = OpcionRespuesta.objects.filter(pregunta=p).count()
        self.assertEqual(4, opts)
