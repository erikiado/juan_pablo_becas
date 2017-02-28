from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from familias.models import Familia
from perfiles_usuario.models import Capturista
from estudios_socioeconomicos.models import Estudio
from .models import Retroalimentacion
from django.core.urlresolvers import reverse


class TestViewsCaptura(StaticLiveServerTestCase):

    def setUp(self):
        """ Setup attributes.

        """
        self.browser = Browser('chrome')
        self.user = get_user_model().objects.create_user(
                                    username='some_user',
                                    email='temporary@gmail.com',
                                    password='some_pass')
        capturista = Capturista.objects.create(user=self.user)
        familia = Familia.objects.create(
                                explicacion_solvencia='aaa',
                                estado_civil='soltero',
                                localidad='otro')
        self.estudio = Estudio.objects.create(
                                capturista=capturista,
                                familia=familia,
                                status=Estudio.REVISION)
        self.retroalimentacion = Retroalimentacion(
                                estudio=self.estudio,
                                usuario=self.user,
                                descripcion='No esta claro el campo de ingresos.')
        Retroalimentacion.objects.create(
                                estudio=self.estudio,
                                usuario=self.user,
                                descripcion='No esta claro el campo de ingresos.')

    def test_crear_retroalimentacion(self):
        """ Test for the url 'administracion:crear_retroalimentacion'.

        Visit te url and check it loads the content of the dashboard panel.
        """
        test_url_name = 'administracion:crear_retroalimentacion'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Retroalimentación'))

        # Check that the form is sent
        self.assertEqual(Retroalimentacion.objects.count(), 1)
        self.assertTrue(self.browser.is_text_present('Retroalimentacion'))
