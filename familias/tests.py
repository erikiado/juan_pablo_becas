from django.test import TestCase
from administracion.models import Escuela
from familias.models import Familia
from .forms import IntegranteModelForm


class TestIntegranteForm(TestCase):

    def setUp(self):
        """Setup the dictionary with data for feeding the form.

        """

        self.escuela = Escuela.objects.create(nombre='Juan Pablo')
        self.familia = Familia.objects.create(numero_hijos_diferentes_papas=2,
                                              estado_civil='soltero',
                                              localidad='Nabo')

        self.valid_data = {
            'familia': self.familia.id,
            'nombres': 'Elver',
            'apellidos': 'Gudo',
            'fecha_de_nacimiento': '1943-03-19',
            'nivel_estudios': 'doctorado',
        }

    def test_valid_data_basic(self):
        """ Test form with a integrante that does not have a role.

        """
        data_form = self.valid_data.copy()
        data_form['rol'] = 'ninguno'
        form = IntegranteModelForm(data_form)
        self.assertTrue(form.is_valid())

    def test_invalid_data_basic(self):
        """ Test that a form without role is invalid

        """
        data_form = self.valid_data.copy()
        form = IntegranteModelForm(data_form)
        self.assertFalse(form.is_valid())

    def test_invalid_data_mixed(self):
        """ Test that a form with role and fields that don't correspond
        to that role is invalid.

        """
        data_form = self.valid_data.copy()
        data_form['rol'] = 'tutor'
        data_form['numero_sae'] = '1234'
        form = IntegranteModelForm(data_form)
        self.assertFalse(form.is_valid())

    def test_valid_data_tutor(self):
        """ Test form with a father.

        """
        data_form = self.valid_data.copy()
        data_form['rol'] = 'tutor'
        data_form['relacion'] = 'padre'
        form = IntegranteModelForm(data_form)
        self.assertTrue(form.is_valid())

    def test_invalid_data_tutor(self):
        """ Test form with an invalid tutor.

        """
        data_form = self.valid_data.copy()
        data_form['rol'] = 'tutor'
        form = IntegranteModelForm(data_form)
        self.assertFalse(form.is_valid())

    def test_valid_student(self):
        """ Test form with the valid data of a student.

        """
        data_form = self.valid_data.copy()
        data_form['rol'] = 'alumno'
        data_form['numero_sae'] = '123456'
        data_form['escuela'] = self.escuela.id
        form = IntegranteModelForm(data_form)
        self.assertTrue(form.is_valid())

    def test_invalid_student(self):
        """ Test form with invalid data of a student.

        """
        data_form = self.valid_data.copy()
        data_form['rol'] = 'alumno'
        data_form['escuela'] = self.escuela.id
        form = IntegranteModelForm(data_form)
        self.assertFalse(form.is_valid())

    def test_invalid_student2(self):
        """ Test form with invalid data of a student.

        """
        data_form = self.valid_data.copy()
        data_form['rol'] = 'alumno'
        data_form['escuela'] = self.escuela.id
        data_form['numero_sae'] = '123456'
        data_form['relacion'] = 'padre'
        form = IntegranteModelForm(data_form)
        self.assertFalse(form.is_valid())

    def test_edit_integrante(self):
        """ Test that the form works correctly to edit a user.

        """
        data_form = self.valid_data.copy()
        data_form['rol'] = 'ninguno'
        form = IntegranteModelForm(data_form)
        self.assertTrue(form.is_valid())
        integrante = form.save()
        self.assertEqual(integrante.nombres, 'Elver')
        data_form['nombres'] = 'Ja'  # change nombres
        form = IntegranteModelForm(data_form, instance=integrante)
        self.assertTrue(form.is_valid())
        integrante = form.save()
        self.assertEqual(integrante.nombres, 'Ja')

    def test_edit_tutor(self):
        """ Test that the form works correctly to edit a tutor.

        """
        data_form = self.valid_data.copy()
        data_form['rol'] = 'tutor'
        data_form['relacion'] = 'padre'
        form = IntegranteModelForm(data_form)
        self.assertTrue(form.is_valid())
        integrante = form.save()
        self.assertEqual(integrante.tutor_integrante.relacion, 'padre')
        data_form['relacion'] = 'madre'  # change relacion
        data_form['nombres'] = 'Fernando'
        form = IntegranteModelForm(data_form, instance=integrante)
        self.assertTrue(form.is_valid())
        integrante = form.save()
        self.assertEqual(integrante.nombres, 'Fernando')
        self.assertEqual(integrante.tutor_integrante.relacion, 'madre')

    def test_edit_student(self):
        """ Test that the form works correctly when editing a student.

        """
        data_form = self.valid_data.copy()
        data_form['rol'] = 'alumno'
        data_form['numero_sae'] = '123456'
        data_form['escuela'] = self.escuela.id
        form = IntegranteModelForm(data_form)
        self.assertTrue(form.is_valid())
        integrante = form.save()
        self.assertEqual(integrante.alumno_integrante.numero_sae, '123456')
        self.assertEqual(integrante.alumno_integrante.escuela, self.escuela)
        data_form['numero_sae'] = '987'
        form = IntegranteModelForm(data_form, instance=integrante)
        self.assertTrue(form.is_valid())
        integrante = form.save()
        self.assertEqual(integrante.alumno_integrante.numero_sae, '987')
