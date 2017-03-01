import decimal
from django.test import TestCase
from familias.models import Familia
from .models import Oficio, Periodo, Transaccion, Ingreso


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


class TestPeriodo(TestCase):
    """ Unit test suite for testing the Periodo model in .models.

    """

    def setUp(self):
        """ Setup required for all the test in this suite.

        This setup creates a new Periodo object.
        """
        self.periodicidad = 'Anual'
        self.factor = 1.0
        self.multiplica = True
        Periodo.objects.create(periodicidad=self.periodicidad,
                               factor=self.factor,
                               multiplica=self.multiplica)

    def test_str(self):
        """ Test for the periodo __str__ method.

        This tests that it returns the peridicidad of the oficio.
        """
        periodo = Periodo.objects.get(periodicidad=self.periodicidad)
        self.assertEqual(str(periodo), self.periodicidad)


class TestTransacciones(TestCase):
    """ Unit test suite for testing the Transaccione Model.

    """
    def setUp(self):
        """ Setup required for all tests in this suite

        This setup creates a famila to which all the transactions
        will be linked, and mock periods to add to the transactions,
        as well as the transaction itself.
        """
        familia = Familia.objects.create(estado_civil='soltero', localidad='Nabo')
        self.factor_anual = decimal.Decimal('12')
        periodo_anual = Periodo.objects.create(periodicidad='Anual',
                                               factor=self.factor_anual,
                                               multiplica=False)
        Transaccion.objects.create(familia=familia,
                                   activo=True,
                                   monto=1200,
                                   periodicidad=periodo_anual,
                                   es_ingreso=True)

    def test_obtener_valor_de_transaccion(self):
        """ Test that the obtener_valor_de_transaccion method works.

        This test, checks that the correct value is returned for the three
        cases of the function
        """
        transaccion = Transaccion.objects.get(monto=1200)
        self.assertEqual(transaccion.obtener_valor_de_transaccion(), decimal.Decimal('1200.0'))
        transaccion.es_ingreso = False
        self.assertEqual(transaccion.obtener_valor_de_transaccion(), decimal.Decimal('-1200.0'))
        transaccion.activo = False
        self.assertEqual(transaccion.obtener_valor_de_transaccion(), decimal.Decimal('0.0'))

    def test_obtener_valor_mensual(self):
        """ Test that the funcitn obtener_valor_mensual method works.

        This test, checks that the correct value is returned for the six cases the function
        might be in.
        """

        # Casos when multiplica is False
        transaccion = Transaccion.objects.get(monto=decimal.Decimal('1200'))
        self.assertEqual(transaccion.obtener_valor_mensual(), decimal.Decimal('100.0'))
        transaccion.es_ingreso = False
        self.assertEqual(transaccion.obtener_valor_mensual(), decimal.Decimal('-100.0'))
        transaccion.activo = False
        self.assertEqual(transaccion.obtener_valor_mensual(), decimal.Decimal('0.0'))

        # Casos when multiplica is True
        periodo = Periodo.objects.get(periodicidad='Anual')
        periodo.factor = decimal.Decimal('10.0')
        periodo.multiplica = True
        periodo.save()
        periodo = Periodo.objects.get(periodicidad='Anual')
        transaccion = Transaccion.objects.get(monto=1200)
        self.assertEqual(transaccion.obtener_valor_mensual(), decimal.Decimal('12000.0'))
        transaccion.es_ingreso = False
        self.assertEqual(transaccion.obtener_valor_mensual(), decimal.Decimal('-12000.0'))
        transaccion.activo = False
        self.assertEqual(transaccion.obtener_valor_mensual(), decimal.Decimal('0.0'))

    def test_str(self):
        transaccion = Transaccion.objects.get(monto=1200)
        self.assertEqual(str(transaccion), '$100.00 mensuales')
        transaccion.es_ingreso = False
        self.assertEqual(str(transaccion), '-$100.00 mensuales')
        transaccion.activo = False
        self.assertEqual(str(transaccion), '$0.00 mensuales')


class TestIngreso(TestCase):
    """ Unit test suite for testing the Ingreso Model.

    """

    def setUp(self):
        """ Setup required for all tests in this suite.

        This setup creates a famila to which all the transactions
        will be linked, and mock periods to add to the ingreso, a transaction, and
        the ingreso as well.
        """
        familia = Familia.objects.create(estado_civil='soltero', localidad='Nabo')
        periodo_anual = Periodo.objects.create(periodicidad='Anual',
                                               factor=decimal.Decimal('12'),
                                               multiplica=False)
        transaccion = Transaccion.objects.create(familia=familia,
                                                 activo=True,
                                                 monto=1200,
                                                 periodicidad=periodo_anual,
                                                 es_ingreso=True)
        Ingreso.objects.create(transaccion=transaccion,
                               fecha='2017-07-01',
                               tipo='no comprobable')

    def test_str(self):
        """ Test for the Ingreso __str__ method.

        This tests that it returns the __str__ of the related transaccion.
        """
        ingreso = Ingreso.objects.get(tipo='no comprobable')
        self.assertEqual(str(ingreso), '$100.00 mensuales')
