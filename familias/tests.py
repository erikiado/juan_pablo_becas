from django.test import TestCase
from django.forms import ValidationError
from administracion.models import Escuela
from .models import Familia, Integrante, Alumno
from .forms import IntegranteModelForm, DeleteIntegranteForm


class TestIntegranteForm(TestCase):
    """ Unit tests for the form to edit and create Integrantes.

    """

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


class TestIntegranteDeleteForm(TestCase):
    """ Unit tests for the form to delete Integrantes.

    """

    def setUp(self):
        """Setup data for tests.

        """

        escuela = Escuela.objects.create(nombre='Juan Pablo')
        familia = Familia.objects.create(numero_hijos_diferentes_papas=2,
                                         estado_civil='soltero',
                                         localidad='Nabo')
        self.integrante1 = Integrante.objects.create(
                                familia=familia,
                                nombres='Elver',
                                apellidos='Ga',
                                telefono='4424356788',
                                nivel_estudios=Integrante.OPCION_ESTUDIOS_UNIVERSIDAD,
                                fecha_de_nacimiento='1943-03-19')

        self.integrante2 = Integrante.objects.create(
                                familia=familia,
                                nombres='Elm',
                                apellidos='Otelo',
                                telefono='4424356788',
                                nivel_estudios=Integrante.OPCION_ESTUDIOS_4,
                                fecha_de_nacimiento='1999-03-19')
        self.alumno = Alumno.objects.create(
                                integrante=self.integrante2,
                                numero_sae='12345',
                                escuela=escuela)

    def test_integrante(self):
        """ Test the save method validating that the integrante changes to inactive.

        """
        form = DeleteIntegranteForm({'integrante_id': self.integrante1.pk})
        self.assertTrue(self.integrante1.activo)
        self.assertTrue(form.is_valid())
        form.save()
        integrante = Integrante.objects.get(pk=self.integrante1.pk)
        self.assertFalse(integrante.activo)

    def test_invalid_integrante(self):
        """ Test that the form is invalid if provided an invalid id.

        """
        form = DeleteIntegranteForm({'integrante_id': -1})
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError):
            form.clean()

    def test_student(self):
        """ Test the soft delete for a student.

        """
        form = DeleteIntegranteForm({'integrante_id': self.integrante2.pk})
        self.assertTrue(self.integrante2.activo)
        self.assertTrue(form.is_valid())
        form.save()
        integrante = Integrante.objects.get(pk=self.integrante2.pk)
        self.assertFalse(integrante.activo)
        self.assertFalse(integrante.alumno_integrante.activo)
