from django.test import TestCase
from familias.models import Familia
from .models import Oficio, Periodo, Transaccion, Ingreso


class TestOficio(TestCase):
    """ Unit test suite for testing the Oficio model in .models

    Attributes:
    -----------
    nombre : String
        Stores the name that will be used for the name of the oficio object.
    """

    nombre = 'Electricista'

    def setUp(self):
        """ Setup required for all the tests in this suite.

        This setup creates a new Oficio object.
        """

        Oficio.objects.create(nombre=self.nombre)

    def test_str(self):
        """ Test for the oficio __str__ method.

        This tests that it returns the name of the oficio.
        """
        oficio = Oficio.objects.get(nombre=self.nombre)
        self.assertTrue(str(oficio) == self.nombre)


class TestPeriodo(TestCase):
    """ Unit test suite for testing the Periodo model in .models.

    Attributes:
    -----------
    periodicidad : String
        Denotes the value of the perodicidad field that will be used to
        create objects, and test the methods of said object.
    multiplicador : float
        Denotes the value of the multiplicador field that will be used to crete objects.
    """

    periodicidad = 'Anual'
    multiplicador = 1.0

    def setUp(self):
        """ Setup required for all the test in this suite.

        This setup creates a new Periodo object.
        """
        Periodo.objects.create(periodicidad=self.periodicidad, multiplicador=self.multiplicador)

    def test_str(self):
        """ Test for the periodo __str__ method.

        This tests that it returns the peridicidad of the oficio.
        """
        periodo = Periodo.objects.get(periodicidad=self.periodicidad)
        self.assertTrue(str(periodo) == self.periodicidad)


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
        periodo_anual = Periodo.objects.create(periodicidad='Anual', multiplicador=1/12)
        Transaccion.objects.create(familia=familia,
                                   activo=True,
                                   monto=1200,
                                   periodicidad=periodo_anual,
                                   es_ingreso=True)

    def test_obtener_valor_de_transaccion(self):
        """ Test that the obtener_valor_de_transaccion function

        This test, checks that the correct value is returned for the three
        cases of the function
        """
        transaccion = Transaccion.objects.get(monto=1200)
        self.assertTrue(transaccion.obtener_valor_de_transaccion() == 1200.0)
        transaccion.es_ingreso = False
        self.assertTrue(transaccion.obtener_valor_de_transaccion() == -1200.0)
        transaccion.activo = False
        self.assertTrue(transaccion.obtener_valor_de_transaccion() == 0.0)

#     def test_obtener_valor_mensual(self):
#         transaccion = Transaccion.objects.get(monto=1200)
#         print(transaccion.obtener_valor_mensual())
#         self.assertTrue(transaccion.obtener_valor_mensual() == 1200.0 * 1/12)
#         transaccion.es_ingreso = False
#         self.assertTrue(transaccion.obtener_valor_mensual() == 100.0)
#         transaccion.activo = False
#         self.assertTrue(transaccion.obtener_valor_mensual() == 0.0)

#     def test_str(self):
#         transaccion = Transaccion.objects.get(monto=1200)
#         self.assertTrue(str(transaccion) == '$100.00 mensuales')
#         transaccion.es_ingreso = False
#         self.assertTrue(str(transaccion) == '-$100.00 mensuales')
#         transaccion.activo = False
#         self.assertTrue(str(transaccion) == '$0.00 mensuales')


class TestIngreso(TestCase):
    """ Unit test suite for testing the Ingreso Model.

    """

    def setUp():
        """ Setup required for all tests in this suite.

        This setup creates a famila to which all the transactions
        will be linked, and mock periods to add to the ingreso, a transaction, and
        the ingreso as well.
        """
        familia = Familia.objects.create(estado_civil='soltero', localidad='Nabo')
        periodo_anual = Periodo.objects.create(periodicidad='Anual', multiplicador=1/12)
        transaccion = Transaccion.objects.create(familia=familia,
                                                 activo=True,
                                                 monto=1200,
                                                 periodicidad=periodo_anual,
                                                 es_ingreso=True)
        Ingreso.objects.create(transaccion=transaccion,
                               date='20/07/01',
                               tipo='no comprobable')

    # def test_str(self):
    #     """ Test for the Ingreso __str__ method.

    #     This tests that it returns the __str__ of the related transaccion.
    #     """
    #     ingreso = Ingreso.objects.get(tipo='no comprobable')
    #     self.assertTrue(str(ingreso) == '$100.00 mensuales')
