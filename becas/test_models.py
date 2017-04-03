import decimal
from django.test import TestCase
from administracion.models import Escuela
from familias.models import Familia, Integrante, Alumno
from .models import Beca


class TestBeca(TestCase):
    """ Unit test suite for testing the Beca model in .models
    """

    def setUp(self):
        """ Setup required for the tests in this suite.

        """
        escuela = Escuela.objects.create(nombre='Juan Pablo')
        familia = Familia.objects.create(numero_hijos_diferentes_papas=2,
                                         estado_civil='soltero',
                                         localidad='Nabo')
        integrante = Integrante.objects.create(familia=familia,
                                               nombres='Mario',
                                               apellidos='Molina',
                                               nivel_estudios='doctorado',
                                               fecha_de_nacimiento='1943-03-19')
        alumno = Alumno.objects.create(integrante=integrante, escuela=escuela)
        Beca.objects.create(alumno=alumno,
                            monto=decimal.Decimal('250'))

    def test_str(self):
        """ Checks that this method __str__ method returns the name
        of the object.
        """
        beca = Beca.objects.get(monto=decimal.Decimal('250.0'))
        self.assertEqual(str(beca), '$250.00 mensuales')
