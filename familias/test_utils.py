from django.test import TestCase
from indicadores.models import Transaccion, Ingreso, Periodo
from .models import Familia, Integrante, Tutor
from .utils import total_egresos_familia, total_ingresos_familia, total_neto_familia


class TestFormsTransacciones(TestCase):
    def setUp(self):
        """ Creates all the initial necessary objects for the tests
        """

        numero_hijos_inicial = 3
        estado_civil_inicial = 'soltero'
        localidad_inicial = 'salitre'
        self.familia1 = Familia.objects.create(nombre_familiar='Molina',
                                               numero_hijos_diferentes_papas=numero_hijos_inicial,
                                               estado_civil=estado_civil_inicial,
                                               localidad=localidad_inicial)

        self.integrante1 = Integrante.objects.create(familia=self.familia1,
                                                     nombres='Rick',
                                                     apellidos='Astley',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.tutor1 = Tutor.objects.create(integrante=self.integrante1,
                                           relacion='padre')

        self.integrante_constructor_dictionary = {'familia': self.familia1.id,
                                                  'nombres': 'Arturo',
                                                  'apellidos': 'Herrera Rosas',
                                                  'telefono': '',
                                                  'correo': '',
                                                  'nivel_estudios': 'ninguno',
                                                  'fecha_de_nacimiento': '2017-03-22',
                                                  'rol': 'ninguno'}

        self.periodo = Periodo.objects.create(periodicidad='Semanal',
                                              factor=4,
                                              multiplica=True)
        self.transaccion1 = Transaccion.objects.create(familia=self.familia1,
                                                       monto=30,
                                                       periodicidad=self.periodo,
                                                       observacion='Egreso Familia',
                                                       es_ingreso=False)
        self.transaccion2 = Transaccion.objects.create(familia=self.familia1,
                                                       monto=40,
                                                       periodicidad=self.periodo,
                                                       observacion='Ingreso Familia',
                                                       es_ingreso=True)
        self.ingreso1 = Ingreso.objects.create(transaccion=self.transaccion2,
                                               fecha='2016-02-02',
                                               tipo='comprobable')

    def test_total_ingresos(self):
        """ Test that the total of ingresos of the family is accurate, and
        displayed properly
        """
        total_ingresos = total_ingresos_familia(self.familia1.id)
        self.assertEqual('160.00', total_ingresos)

    def test_total_egresos(self):
        """ Test that the total of egresos of the family is accurate, and
        displayed properly
        """
        total_ingresos = total_egresos_familia(self.familia1.id)
        self.assertEqual('-120.00', total_ingresos)

    def test_total_neto(self):
        """ Test that the total neto of the family income is accurate, and displayed
        properly
        """
        total_ingresos = total_neto_familia(self.familia1.id)
        self.assertEqual('40.00', total_ingresos)
