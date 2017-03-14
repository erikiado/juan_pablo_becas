from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from splinter import Browser

from perfiles_usuario.utils import CAPTURISTA_GROUP
from estudios_socioeconomicos.models import Estudio
from familias.models import Familia
from perfiles_usuario.models import Capturista


class TestViewsAdministracion(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: captura.

    Test the urls for 'captura' which make up the capturista dashboard.
    A user is created in order to test they are displayed.

    Attributes
    ----------
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """Initialize the browser and create a user, before running the tests.
        """
        self.browser = Browser('chrome')
        test_username = 'estebes'
        test_password = 'junipero'
        estebes = User.objects.create_user(
            username=test_username, email='juan@example.com', password=test_password,
            first_name='Estebes', last_name='Thelmapellido')
        capturista = Group.objects.get_or_create(name=CAPTURISTA_GROUP)[0]
        capturista.user_set.add(estebes)
        capturista.save()

        self.capturista = Capturista.objects.create(user=estebes)
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()

    def tearDown(self):
        """At the end of tests, close the browser.
        """
        self.browser.quit()

    def test_capturista_dashboard_if_this_is_empty(self):
        """Test for url 'captura:estudios'.

        Visit the url of name 'captura:estudios' and check it loads the
        content of the captura dashboard panel.
        """
        test_url_name = 'captura:estudios'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        self.assertEqual(Estudio.objects.count(), 0)
        # Check that the folling texts are present in the dashboard
        self.assertTrue(self.browser.is_text_present('Mis estudios socioeconómicos'))
        self.assertTrue(self.browser.is_text_present('Agregar estudio'))
        # Check that the following text is present if not exists socio-economic studies
        self.assertTrue(self.browser.is_text_present(
                                'No hay registro de estudios socioeconómicos'))
        # Check that the following texts aren't present if not exists any socio-economic study
        self.assertFalse(self.browser.is_text_present('Ver retroalimentación'))
        self.assertFalse(self.browser.is_text_present('Editar'))

    def test_list_studies(self):
        """Test for url 'captura:estudios'.

        Creates two socio-economic studies (f1 and f2) the first as rejected
        (rechazado) and the second as pending (revision) and visit the url
        'captura:estudios' to check it loads both socio-economic studies created
        previously.
        """
        user = User.objects.get(username='estebes')
        user_id = user.id
        capturist = Capturista.objects.get(user=user_id)

        solvencia = 'No tienen dinero'
        estado = Familia.OPCION_ESTADO_SOLTERO
        estado2 = Familia.OPCION_ESTADO_CASADO_CIVIL
        localidad = Familia.OPCION_LOCALIDAD_JURICA
        localidad2 = Familia.OPCION_LOCALIDAD_CAMPANA

        f1 = Familia(numero_hijos_diferentes_papas=1, explicacion_solvencia=solvencia,
                     estado_civil=estado, localidad=localidad)
        f1.save()
        f2 = Familia(numero_hijos_diferentes_papas=2, explicacion_solvencia=solvencia,
                     estado_civil=estado2, localidad=localidad2)
        f2.save()

        e1 = Estudio(capturista_id=capturist.id, familia_id=f1.id,
                     status=Estudio.RECHAZADO, numero_sae=1)
        e1.save()
        e2 = Estudio(capturista_id=capturist.id, familia_id=f2.id,
                     status=Estudio.REVISION, numero_sae=2)
        e2.save()

        test_url_name = 'captura:estudios'
        self.browser.visit(self.live_server_url + reverse(test_url_name))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        self.assertEqual(Estudio.objects.count(), 2)
        # Check that the following texts are present in the dashboard
        self.assertTrue(self.browser.is_text_present('Mis estudios socioeconómicos'))
        self.assertTrue(self.browser.is_text_present('Agregar estudio'))
        # Check that the following text isn't present if exists any socio-economic study
        self.assertFalse(self.browser.is_text_present('No hay registro'))
        # Check that the following texts are present if exists any socio-economic study
        self.assertTrue(self.browser.is_text_present('Estudios en revisión'))
        self.assertTrue(self.browser.is_text_present('Estudios pendientes a revisar'))
        self.assertTrue(self.browser.is_text_present('Editar'))
        self.assertTrue(self.browser.is_text_present('Ver retroalimentación'))
