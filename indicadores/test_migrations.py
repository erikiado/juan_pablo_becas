from django.test import TestCase
from .models import Periodo


class TestLoadPeriodos(TestCase):
    """ Unit test suite for testing that initial data of
    periodos is created
    """

    def test_escuelas_created(self):
        """ Checks that this method __str__ method returns the name
        of the object.
        """
        self.assertTrue(Periodo.objects.get(periodicidad='Diario', factor=30, multiplica=True))
        self.assertTrue(Periodo.objects.get(periodicidad='Semanal', factor='4.3', multiplica=True))
        self.assertTrue(Periodo.objects.get(periodicidad='Quincenal', factor=2, multiplica=True))
        self.assertTrue(Periodo.objects.get(periodicidad='Mensual', factor=1, multiplica=True))
        self.assertTrue(Periodo.objects.get(periodicidad='Bimensual', factor=2, multiplica=False))
        self.assertTrue(Periodo.objects.get(periodicidad='Trimestral', factor=3, multiplica=False))
        self.assertTrue(Periodo.objects.get(periodicidad='Cuatrimestral',
                                            factor=4,
                                            multiplica=False))
        self.assertTrue(Periodo.objects.get(periodicidad='Semestral', factor=6, multiplica=False))
        self.assertTrue(Periodo.objects.get(periodicidad='Anual', factor=12, multiplica=False))
