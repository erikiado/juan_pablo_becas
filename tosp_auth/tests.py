from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, DIRECTIVO_GROUP, \
                                   SERVICIOS_ESCOLARES_GROUP

class WidgetLogoutTest(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: tosp_auth.

        Test if the widget log out are present.

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
        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(thelma)
        administrators.save()

    def tearDown(self):
        """At the end of tests, close the browser.
        """
        self.browser.quit()

    def test_option_does_not_appear(self):
        """Test: if the option log out appear for log users
        """
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', 'thelma')
        self.browser.fill('password', 'junipero')
        self.browser.find_by_id('login-submit').click()
        self.browser.visit(self.live_server_url)
        self.assertTrue(self.browser.is_text_present('Log Out'))

    def test_option_appear_to_no_logged_client(self):
        """Test: if the option log out appear for not log users
        """
        self.browser.visit(self.live_server_url)
        self.assertFalse(self.browser.is_text_present('Log Out'))
