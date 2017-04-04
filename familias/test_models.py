from django.test import TestCase
from administracion.models import Escuela
from .models import Familia, Integrante, Alumno


class TestFamiliaModel(TestCase):
    """ Unit test suite for testing the Beca model in .models
    """

    def setUp(self):
        """ Setup required for the tests in this suite.

        """
        escuela = Escuela.objects.create(nombre='Juan Pablo')
        self.familia = Familia.objects.create(numero_hijos_diferentes_papas=2,
                                         estado_civil='soltero',
                                         localidad='Nabo')
        self.familiaNoAlumno = Familia.objects.create(numero_hijos_diferentes_papas=2,
                                         estado_civil='soltero',
                                         localidad='Nabo')
        integrante = Integrante.objects.create(familia=self.familia,
                                               nombres='Mario',
                                               apellidos='Molina',
                                               nivel_estudios='doctorado',
                                               fecha_de_nacimiento='1943-03-19')
        alumno = Alumno.objects.create(integrante=integrante, escuela=escuela)


    def test_str_familia_con_alumno(self):
        """ Checks that this method __str__ method returns the name
        of the object.
        """
        self.assertEqual(str(self.familia), 'Molina')

    def test_str_familia_sin_alumno(self):
        """ Checks that this method __str__ method returns the proper
        string in case a family has no children.
        """
        self.assertEqual(str(self.familiaNoAlumno), 'Aún no se crean alumnos en el estudio')
