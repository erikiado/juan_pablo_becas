from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from django.contrib.auth.models import User
from perfiles_usuario.utils import CAPTURISTA_GROUP
from django.contrib.auth.models import Group
from estudios_socioeconomicos.models import Estudio


class TestViewsAdministracion(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: administracion.

    Test the urls for 'administracion' which make up the administration dashboard.
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
        test_username = 'thelma'
        test_password = 'junipero'
        thelma = User.objects.create_user(
            username=test_username, email='juan@pablo.com', password=test_password,
            first_name='Thelma', last_name='Thelmapellido')
        capturista = Group.objects.get_or_create(name=CAPTURISTA_GROUP)[0]
        capturista.user_set.add(thelma)
        capturista.save()
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()

    def tearDown(self):
        """At the end of tests, close the browser.

        """
        self.browser.quit()

    def test_main_dashboard(self):
        """Test for url 'captura:capturista_dashboard'.

        Visit the url of name 'captura:capturista_dashboard' and check it loads the
        content of the captura dashboard panel.
        """
        test_url_name = 'captura:capturista_dashboard'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        self.assertEqual(Estudio.objects.count(), 0)
        # Check that the folling texts are present in the dashboard
        self.assertTrue(self.browser.is_text_present('Mis estudios socioeconómicos'))
        self.assertTrue(self.browser.is_text_present('Agregar estudio'))
