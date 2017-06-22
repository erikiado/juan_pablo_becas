from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client

from rest_framework import status

from administracion.models import Escuela
from captura.models import Retroalimentacion
from estudios_socioeconomicos.models import Estudio
from familias.models import Familia, Integrante, Alumno
from perfiles_usuario.models import Capturista
from estudios_socioeconomicos.load import load_data
from perfiles_usuario.utils import ADMINISTRADOR_GROUP


class TestRetroalimentacions(TestCase):
    """ Tests that an administrador can leave feedback and aprove or
        reject a study.

        Attributes
        ----------
        client : Client
            Django Client for the testing the focus mode view.
        elerik : User
            User that will be used as a capturista.
        capturista : Capturista
            Asociated with the User, as this object is required for permissions and
            creation.
    """

    def setUp(self):
        """ This generates the family with its integrantes and
            a estudio..
        """
        self.client = Client()
        self.test_username = 'thelma'
        self.test_password = 'vacalalo'

        elerik = User.objects.create_user(
            username='erikiano',
            email='latelma@junipero.sas',
            password=self.test_password,
            first_name='telma',
            last_name='suapellido')

        self.thelma = User.objects.create_user(
            username=self.test_username,
            email='juan@pablo.com',
            password=self.test_password,
            first_name='Thelma',
            last_name='Thelmapellido')

        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(self.thelma)
        administrators.save()

        self.capturista = Capturista.objects.create(user=elerik)
        self.capturista.save()

        load_data()

        self.familia = Familia.objects.create(
            numero_hijos_diferentes_papas=3,
            explicacion_solvencia='narco',
            estado_civil='secreto',
            localidad='otro')

        self.estudio = Estudio.objects.create(
            capturista=self.capturista,
            familia=self.familia,
            status=Estudio.REVISION)

        self.escuela = Escuela.objects.create(nombre='Rolando Calles')

        self.integrante_alumno = Integrante.objects.create(
            familia=self.familia,
            nombres='Rick',
            apellidos='Astley',
            nivel_estudios='doctorado',
            fecha_de_nacimiento='1996-02-26')

        self.alumno = Alumno.objects.create(
            integrante=self.integrante_alumno,
            escuela=self.escuela)

        self.test_url = 'estudios_socioeconomicos:focus_mode'

    def test_can_leave_retroalimentacion(self):
        """ Tests that an administrador has the options in view to
            aprove or reject study.
        """
        self.client.login(username=self.test_username, password=self.test_password)

        response = self.client.get(reverse(self.test_url, kwargs={'id_estudio': self.estudio.id}))
        response_text = response.content.decode('utf-8')

        self.assertIn('Aceptar Estudio', response_text)
        self.assertIn('Rechazar Estudio', response_text)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_study(self):
        """ Tests that an administrador can accept a study.
        """
        self.client.login(username=self.test_username, password=self.test_password)

        url = 'estudios_socioeconomicos:accept_study'
        response = self.client.post(reverse(url, kwargs={'id_estudio': self.estudio.id}))

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Estudio.objects.get(id=self.estudio.id).status, Estudio.APROBADO)

    def test_reject_study_feedback(self):
        """ Tests that a study can be rejected by an administrador an leave feedback
        """
        self.client.login(username=self.test_username, password=self.test_password)

        url = 'estudios_socioeconomicos:reject_study'
        data = {}
        data['estudio'] = self.estudio.id
        data['usuario'] = self.thelma.id
        data['descripcion'] = 'nada bien'

        response = self.client.post(reverse(url), data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Estudio.objects.get(id=self.estudio.id).status, Estudio.RECHAZADO)
        self.assertEqual(Retroalimentacion.objects.all().first().descripcion, 'nada bien')


class TestFocusMode(TestCase):
    """ Tests that a studiy can be viewed on Focus Mode.

        Attributes
        ----------
        client : Client
            Django Client for the testing the focus mode view.
        elerik : User
            User that will be used as a capturista.
        capturista : Capturista
            Asociated with the User, as this object is required for permissions and
            creation.
    """
    def setUp(self):
        """ This generates the family with its integrantes and
            a estudio that will be later queried in the focus mode.
        """
        self.client = Client()
        self.test_username = 'erikiano'
        self.test_password = 'vacalalo'

        elerik = User.objects.create_user(
            username=self.test_username,
            email='latelma@junipero.sas',
            password=self.test_password,
            first_name='telma',
            last_name='suapellido')

        self.capturista = Capturista.objects.create(user=elerik)
        self.capturista.save()

        load_data()

        self.familia = Familia.objects.create(
            numero_hijos_diferentes_papas=3,
            explicacion_solvencia='narco',
            estado_civil='secreto',
            localidad='otro')

        self.estudio = Estudio.objects.create(
            capturista=self.capturista,
            familia=self.familia,
            status=Estudio.APROBADO)

        self.escuela = Escuela.objects.create(nombre='Rolando Calles')

        self.integrante_alumno = Integrante.objects.create(
            familia=self.familia,
            nombres='Rick',
            apellidos='Astley',
            nivel_estudios='doctorado',
            fecha_de_nacimiento='1996-02-26')

        self.alumno = Alumno.objects.create(
            integrante=self.integrante_alumno,
            escuela=self.escuela)

        self.test_url = 'estudios_socioeconomicos:focus_mode'

    def test_view_study(self):
        """ Test that a study can be viewed in focus mode.
        """
        self.client.login(username=self.test_username, password=self.test_password)

        response = self.client.get(reverse(self.test_url, kwargs={'id_estudio': self.estudio.id}))
        response_text = response.content.decode('utf-8')

        self.assertIn(self.integrante_alumno.nombres, response_text)
        self.assertIn(str(self.estudio), response_text)
        self.assertIn(self.familia.get_localidad_display(), response_text)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_access_capturista(self):
        """ Tests that a capturista that did not create the study
            can't access it.
        """
        no_autorizado = User.objects.create_user(
            username='noautorizado',
            email='noautorizado@junipero.sas',
            password='noautorizado',
            first_name='noautorizado',
            last_name='noautorizado')

        Capturista.objects.create(user=no_autorizado)

        self.client.login(username='noautorizado', password='noautorizado')
        response = self.client.get(reverse(self.test_url, kwargs={'id_estudio': self.estudio.id}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTemplateUsed(response, '404.html')

    def test_admin_can_view(self):
        """ tests that an administrator user can view any study.
        """
        test_username = 'thelma'
        test_password = 'junipero'
        thelma = User.objects.create_user(
            username=test_username, email='juan@pablo.com', password=test_password,
            first_name='Thelma', last_name='Thelmapellido')

        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(thelma)
        administrators.save()
        self.client.login(username=test_username, password=test_password)
        response = self.client.get(reverse(self.test_url, kwargs={'id_estudio': self.estudio.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'estudios_socioeconomicos/focus_mode.html')

    def test_non_active_family_members_invisible(self):
        """ Test that an inactive family member can't appear inside the focus mode.
        """

        inactive_member = Integrante.objects.create(
            familia=self.familia,
            nombres='Inactive',
            apellidos='Oddjob',
            nivel_estudios='doctorado',
            fecha_de_nacimiento='1996-02-26',
            activo=False)

        self.client.login(username=self.test_username, password=self.test_password)

        response = self.client.get(reverse(self.test_url, kwargs={'id_estudio': self.estudio.id}))
        response_text = response.content.decode('utf-8')

        self.assertNotIn(inactive_member.nombres, response_text)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
