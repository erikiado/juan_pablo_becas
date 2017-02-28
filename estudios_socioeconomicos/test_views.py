from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group
from splinter import Browser

from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, DIRECTIVO_GROUP, \
                                   SERVICIOS_ESCOLARES_GROUP



class PendingStudiosTest(StaticLiveServerTestCase):
    """ Integration test suite for testing the views in the app: estudios_socioeconomicos.
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
        thelma = User.objects.create_user(
              username='thelma', email='juan@pablo.com', password='junipero')
        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(thelma)


    def tearDown(self):
        """ At the end of tests, close the browser.

        """
        self.browser.quit()

    def test_pending_studies_appears_for_user_admin(self):
        """ Test for url 'estudios_socioeconomicos:pendientes'.

            Visit the url of name 'estudios_socioeconomicos:pendientes' and check it loads the
            content of the socio-economic studies dashboard panel.
        """
        test_url_name = 'estudios_socioeconomicos:pendientes'
        self.client.login(username='thelma', password='junipero')

        self.browser.visit(self.live_server_url + reverse(test_url_name))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))

    def test_studies_under_review_appears_for_admin(self):
        """ Test for url 'estudios_socioeconomicos:revision'.

            Visit the url of name 'estudios_socioeconomicos:revision' and check it loads the
            content of the socio-economic studies dashboard panel.
        """
        test_url_name = 'estudios_socioeconomicos:revision'
        self.client.login(username='thelma', password='junipero')
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))

    def test_option_appear_to_no_logged_client(self):
        """ Test: verify if the socio-economic studies appears for user not logged

        """
        self.browser.visit(self.live_server_url)
        self.assertFalse(self.browser.is_text_present('Estudios Socioeconómicos'))
