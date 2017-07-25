from django.test import TestCase
from .models import Familia, Integrante, Oficio, Sacramento


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


class TestSacramento(TestCase):
    """ Unit test suite for testing the Sacramento model in .models

    """

    def setUp(self):
        """ Setup required for all the tests in this suite.

        This setup creates a new Sacramento object.
        """
        self.nombre = 'Confesión'
        Sacramento.objects.create(nombre=self.nombre)

    def test_str(self):
        """ Test for the Sacramento __str__ method.

        This tests that it returns the name of the sacramento.
        """
        sacramento = Sacramento.objects.get(nombre=self.nombre)
        self.assertEqual(str(sacramento), self.nombre)


class TestIntegranteModel(TestCase):
    """ Unit test suite for testing the Integrante moden in .models

    Attributes:
    -----------
    familia : Familia
        The family to which new members will be linked.
    integrante : Integrante
        Integrante created as a subject for the tests.
    """

    def setUp(self):
        """ Setup required for the tests in this suite.

        """
        self.familia = Familia.objects.create(nombre_familiar='Molina',
                                              numero_hijos_diferentes_papas=2,
                                              estado_civil='soltero',
                                              localidad='Nabo')
        self.integrante = Integrante.objects.create(familia=self.familia,
                                                    nombres='Rick',
                                                    apellidos='Astley',
                                                    nivel_estudios='doctorado',
                                                    fecha_de_nacimiento='1996-02-26')

    def test_str(self):
        """ Test for the integrante __str__ method.

        This tests that it returns the full name of the integrante.
        """
        self.assertEqual(str(self.integrante), 'Rick Astley')

    def test_kindergarten_option(self):
        """ Test that kindergarten is an option for scholarity

        The new tests refer to the ability to have kindergarten as an
        option for the scholarity level of a family member
        """
        self.assertTrue(Integrante.OPCION_ESTUDIOS_PREESCOLAR_1)
        self.assertTrue(Integrante.OPCION_ESTUDIOS_PREESCOLAR_2)
        self.assertTrue(Integrante.OPCION_ESTUDIOS_PREESCOLAR_3)
