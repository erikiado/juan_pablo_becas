from django.test import TestCase
from familias.models import Familia, Integrante, Tutor
from .forms import IngresoForm


class TestFormsTransacciones(TestCase):
    """ Integration test suite for testing the forms in the app indicadores,
    that surround the creation and editing of the transaccion and ingreso model.

    Attributes
    ----------
    familia1 : Familia
        Used in tests that depend on creating or editing an object related to a familia.
    familia2: Familia
        Used to make sure tutores don't leak when selecting one for an ingreso.
    integrante1 : Integrante
        Used in tests that depend on creating or editing an object related to an integrante.
    integrante2 : Integrante
        Used to create a different queryset, for the forms
    tutor1 : Tutor
        Tutor for the first familia
    tutor2 : Tutor
        Tutor for the second familia, this one is checked for not being in the queryset for the
        ingreso form of familia 1.
    """

    def setUp(self):
        """ Creates all the initial necessary objects for the tests
        """
        numero_hijos_inicial = 3
        estado_civil_inicial = 'soltero'
        localidad_inicial = 'salitre'
        self.familia1 = Familia.objects.create(numero_hijos_diferentes_papas=numero_hijos_inicial,
                                               estado_civil=estado_civil_inicial,
                                               localidad=localidad_inicial)

        self.familia2 = Familia.objects.create(numero_hijos_diferentes_papas=numero_hijos_inicial,
                                               estado_civil=estado_civil_inicial,
                                               localidad=localidad_inicial)

        self.integrante1 = Integrante.objects.create(familia=self.familia1,
                                                     nombres='Rick',
                                                     apellidos='Astley',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.integrante2 = Integrante.objects.create(familia=self.familia2,
                                                     nombres='Bruce',
                                                     apellidos='Lee',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.tutor1 = Tutor.objects.create(integrante=self.integrante1,
                                           relacion='padre')

        self.tutor2 = Tutor.objects.create(integrante=self.integrante2,
                                           relacion='padre')

    def test_ingreso_tutor_queryset(self):
        """ Test that the select tutor option only includes tutores that are
        part of the family an ingreso is going to be added to.

        """
        id_familia = self.familia1.id
        form = IngresoForm(id_familia)
        tutores_form_queryset = form.fields['tutor'].queryset
        integrantes = Integrante.objects.filter(familia=id_familia).values_list('id', flat=True)
        tutores_familia = Tutor.objects.filter(integrante__in=integrantes)
        all_tutores = Tutor.objects.all()
        self.assertEqual(list(tutores_familia), list(tutores_form_queryset))
        self.assertNotEqual(list(all_tutores), list(tutores_familia))
