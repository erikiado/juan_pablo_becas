from django.test import TestCase
from django.contrib.auth.models import User, Group
from perfiles_usuario.utils import CAPTURISTA_GROUP
from familias.models import Familia, Integrante, Alumno
from administracion.models import Escuela
from perfiles_usuario.models import Capturista
from .forms import DeleteEstudioForm
from .models import Estudio


class AppFormTests(TestCase):
    """
    Attributes
    ----------
    elerik : User
        User that will be used as a capturista in order to fill all everything
        related with familia.
    familia1 : Familia
        Used in tests that depend on creating an object related to a familia.
    estudio1 : Estudio
        Used in test for changing it's status, to eliminado.
    integrante1 : Integrante
        Used in tests to check it becomes inactive.
    integrante2 : Integrante
        Used in tests to check it becomes inactive.
    alumno1 : Alumno
        Used in tests to check if it becomes inactive.
    escuela : Used in tests that depend on creating an object related to an escuela
    capturista : Capturista
        Asociated with the User, as this object is required for permissions and
        creation.
    """

    def setUp(self):
        test_username = 'erikiano'
        test_password = 'vacalalo'

        elerik = User.objects.create_user(
            username=test_username,
            email='latelma@junipero.sas',
            password=test_password,
            first_name='telma',
            last_name='suapellido')
        capturista_group = Group.objects.get_or_create(name=CAPTURISTA_GROUP)[0]
        capturista_group.user_set.add(elerik)

        self.escuela = Escuela.objects.create(nombre='Juan Pablo')

        self.capturista = Capturista.objects.create(user=elerik)

        numero_hijos_inicial = 3
        estado_civil_inicial = 'soltero'
        localidad_inicial = 'salitre'
        self.familia1 = Familia.objects.create(numero_hijos_diferentes_papas=numero_hijos_inicial,
                                               estado_civil=estado_civil_inicial,
                                               localidad=localidad_inicial)

        self.estudio1 = Estudio.objects.create(capturista=self.capturista,
                                               familia=self.familia1)

        self.integrante1 = Integrante.objects.create(familia=self.familia1,
                                                     nombres='Rick',
                                                     apellidos='Astley',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.integrante2 = Integrante.objects.create(familia=self.familia1,
                                                     nombres='Rick',
                                                     apellidos='Astley',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.alumno1 = Alumno.objects.create(integrante=self.integrante2,
                                             numero_sae='5876',
                                             escuela=self.escuela)

    def test_form_soft_deletes(self):
        form_data = {'id_estudio': self.estudio1.id}
        form = DeleteEstudioForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        estudio = Estudio.objects.get(pk=self.estudio1.pk)
        self.assertEqual(estudio.status, Estudio.ELIMINADO)
        integrante = Integrante.objects.get(pk=self.integrante1.pk)
        self.assertEqual(integrante.activo, False)
        integrante = Integrante.objects.get(pk=self.integrante2.pk)
        self.assertEqual(integrante.activo, False)
        alumno = Alumno.objects.get(pk=self.alumno1.pk)
        self.assertEqual(alumno.activo, False)
