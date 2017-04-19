from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from perfiles_usuario.models import Capturista
from perfiles_usuario.utils import ADMINISTRADOR_GROUP
from administracion.models import Escuela
from estudios_socioeconomicos.models import Estudio
from familias.models import Familia, Integrante, Alumno


class TestViewsBecas(TestCase):
    """Unit test suite for testing the views in the app: administracion.

    Test that the views for 'administracion' are correctly received as a response and that
    they use the correct template.
    """

    def setUp(self):
        """ This generates the family with its integrantes and
            a estudio that will be later queried in the focus mode.
        """
        thelma = User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero',
            first_name='Thelma', last_name='Amlet')
        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(thelma)
        self.client.login(username='thelma', password='junipero')

        elerik = User.objects.create_user(
            username='erikiano',
            email='latelma@junipero.sas',
            password='eugenio420',
            first_name='telma',
            last_name='suapellido')

        self.capturista = Capturista.objects.create(user=elerik)
        self.capturista.save()

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

    def test_template_asignar_beca(self):
        """ Test that we can access the url and
        the template is the expected one.
        """
        response = self.client.get(reverse('becas:asignar_beca',
                                           kwargs={'id_estudio': self.estudio.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'becas/asignar_beca.html')

    def test_asignar_becas_invalid_study(self):
        """ Test that we get a 404 if the id of the study is invalid
        in the url.
        """
        response = self.client.get(reverse('becas:asignar_beca',
                                           kwargs={'id_estudio': 101010}))
        self.assertEqual(404, response.status_code)
