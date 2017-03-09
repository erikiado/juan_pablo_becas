from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group

from splinter import Browser

from perfiles_usuario.utils import ADMINISTRADOR_GROUP
from estudios_socioeconomicos.models import Estudio
from familias.models import Familia
from perfiles_usuario.models import Capturista


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
        User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero')

    def tearDown(self):
        """At the end of tests, close the browser.
        """
        self.browser.quit()

    def test_main_dashboard(self):
        """Test for url 'administracion:main'.

        Visit the url of name 'administracion:main' and check it loads the
        content of the main dashboard panel.
        """
        test_url_name = 'administracion:main'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Administración'))

    def test_users_dashboard(self):
        """Test for url 'administracion:users'.

        Visit the url of name 'administracion:users' and check it loads the
        content of the user dashboard panel.
        """
        test_url_name = 'administracion:users'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Usuarios'))

        # Check that the only user is displayed
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(self.browser.is_text_present('thelma'))


class Studies_dashboard_administrator_Test(StaticLiveServerTestCase):
    """ Integration test suite for testing the views in the app: administracion.
        Test if the socio-economic studies are present.

        Attributes
        ----------
        browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """ Initialize the browser and create a user,
            before running the tests.
        """
        self.browser = Browser('chrome')
        test_username = 'thelma'
        test_password = 'junipero'
        thelma = User.objects.create_user(
            username=test_username, email='juan@pablo.com', password=test_password,
            first_name='Thelma', last_name='Thelmapellido')
        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(thelma)
        administrators.save()
        # self.capturista = Capturista.objects.create(user=thelma)
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()


    def tearDown(self):
        """ At the end of tests, close the browser.
        """
        self.browser.quit()

    def test_pending_studies_appears_for_user_admin(self):
        """ Test for url 'administracion:main_estudios'.

            Visit the url of name 'administracion:main_estudios' and check it loads the
            content of the socio-economic studies dashboard panel.
        """
        # self.client.login(username='thelma', password='junipero')
        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))

    def test_studies_under_review_appears_for_admin(self):
        """ Test for url 'administracion:main_estudios'.

            Visit the url of name 'administracion:main_estudios' and check it loads the
            content of the socio-economic studies dashboard panel.
        """
        # self.client.login(username='thelma', password='junipero')
        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
