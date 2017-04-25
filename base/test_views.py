from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from splinter import Browser

from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, DIRECTIVO_GROUP, \
                                   SERVICIOS_ESCOLARES_GROUP
from perfiles_usuario.models import Capturista


class TestBaseViews(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: base.

    Test the url for home and the basefiles like robots.txt and humans.txt

    Attributes
    ----------
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """Initialize the browser, before running the tests.
        """
        self.browser = Browser('chrome')

    def tearDown(self):
        """At the end of tests, close the browser
        """
        self.browser.driver.close()
        self.browser.quit()

    def test_robots(self):
        """Test for url 'base:base_files(robots.txt)'.

        Visit the url of robots.txt and check it loads the file
        """
        self.browser.visit(self.live_server_url + reverse('base_files',
                           kwargs={'filename': 'robots.txt'}))
        self.assertTrue(self.browser.is_text_present('robotstxt'))

    def test_humans(self):
        """Test for url 'base:base_files(humans.txt)'.

        Visit the url of humans.txt and check it loads the file
        """
        self.browser.visit(self.live_server_url + reverse('base_files',
                           kwargs={'filename': 'humans.txt'}))
        self.assertTrue(self.browser.is_text_present('humanstxt'))

    def test_access_to_help(self):
        """ Test that help is accesible via de help button
        """
        test_username = 'thelma'
        test_password = 'junipero'
        self.thelma = get_user_model().objects.create_user(
            username=test_username, email='juan@pablo.com', password=test_password,
            first_name='Thelma', last_name='Thelmapellido')
        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(self.thelma)
        administrators.save()
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()
        self.browser.find_by_id('my-account-btn').click()
        self.browser.find_by_id('help_button').click()
        self.assertTrue(self.browser.is_text_present('Página de ayuda'))


class TestHelp(TestCase):
    """ Suite to test that the help page can be accessed.
    """

    def setUp(self):
        """ Create the necessary elements
        """
        self.username = 'Eugenio420'
        self.password = 'pugnotpug'
        self.user = get_user_model().objects.create_user(
                                            username=self.username,
                                            password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_help(self):
        """ Test for url 'base:ayuda'.

        Visits the url of help.html and checks if it loads the correct template.
        """
        response = self.client.get(reverse('ayuda'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'base/help.html')


class TestRedirects(TestCase):
    """ Suite to test the redirection from base to the corresponding dashboards.


    """

    def setUp(self):
        self.username = 'Eugenio420'
        self.password = 'pugnotpug'
        self.user = get_user_model().objects.create_user(
                                            username=self.username,
                                            password=self.password)

    def test_redirect_to_login(self):
        """ Test that an unauthenticated user gets redirected to login.

        We check that the login_url in settings works properly by redirecting
        to the login url.
        """
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('tosp_auth:login') + '?next=/')

    def create_group(self, group_name):
        """ Utility function to create a group and add the user to it.

        We receive the name of the group, create it, and bound it to the
        user.

        Parameters:
        -----------
        group_name : str
            The name of the group.
        """
        group = Group.objects.get_or_create(name=group_name)[0]
        group.user_set.add(self.user)
        group.save()

    def test_redirect_admin(self):
        """ Test that the admin is redirected to its dashboard.

        We test that a user who has the admin group is redirected to its dashboard.
        """
        self.create_group(ADMINISTRADOR_GROUP)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('administracion:main'))

    def test_redirect_capturista(self):
        """ Test that the capturista is redirected to its dashboard.

        """
        self.capturista = Capturista.objects.create(user=self.user)
        self.create_group(CAPTURISTA_GROUP)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('captura:estudios'))

    def test_redirect_directivo(self):
        """ Test that a directivo is redirected to its dashboard.

        """
        self.create_group(DIRECTIVO_GROUP)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('indicadores:all'))

    def test_redirect_servicios_escolares(self):
        """ Test that servicios escolares is redirected to its dashboard.

        """
        self.create_group(SERVICIOS_ESCOLARES_GROUP)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('becas:services'))

    def test_redirect_login(self):
        """ Test that a logged user gets redirected to home.

        """
        self.create_group(CAPTURISTA_GROUP)
        self.capturista = Capturista.objects.create(user=self.user)
        self.create_group(CAPTURISTA_GROUP)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('captura:estudios'))
        response = self.client.get(reverse('tosp_auth:login'))
        self.assertRedirects(response, reverse('home'), target_status_code=302)
