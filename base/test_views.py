from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from splinter import Browser


from estudios_socioeconomicos.models import Estudio
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

    # def test_home(self):
    #     """Test for url 'base:home'.

    #     Visit the url of name 'home' and check it loads the content
    #     """
    #     self.browser.visit(self.live_server_url + reverse('home'))
    #     self.assertTrue(self.browser.is_text_present('Hello, world!'))

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
        self.assertRedirects(response, reverse('administracion:main_estudios',
                                               kwargs={'status_study': Estudio.REVISION}))

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
