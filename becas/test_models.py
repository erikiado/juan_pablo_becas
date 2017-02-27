from django.test import TestCase
from familias.models import Familia, Integrante, Alumno
from .models import Beca


class TestBeca(TestCase):
    """ Unit test suite for testing the TestEscuela model in .models
    """

    def setUp(self):
        """ Setup required for the tests in this suite.

        This setup creates a new family, student, and a scholarship.
        """
        familia = Familia.objects.create(estado_civil='soltero', localidad='Nabo')
        integrante = Integrante.objects.create(familia=familia,
                                               nombres='Rigoberta',
                                               apellidos='Menchú',
                                               fecha_de_nacimiento='1959-06-29')
        alumno = Alumno.objects.create(integrante=integrante)
        Beca.objects.create(alumno=alumno, monto=350.0, fecha_de_asignacion='2017-02-03')

    def test_str(self):
        """ This test checks that the string method returns monto in money format.
        """
        beca = Beca.objects.get(monto=350.0)
        self.assertTrue(str(beca) == '$350.00')
