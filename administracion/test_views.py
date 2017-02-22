from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from django.contrib.auth.models import User


class TestAdministracionViews(StaticLiveServerTestCase):
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
        """At the end of tests, close the browser
        """
        self.browser.quit()

    def test_panel_principal(self):
        """Test for url 'administracion:administracion_principal'.

        Visit the url of name 'administracion:administracion_principal' and check it loads the
        content of the main dashboard panel.
        """
        test_url_name = 'administracion:administracion_principal'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Administración'))

    def test_panel_usuarios(self):
        """Test for url 'administracion:administracion_usuarios'.

        Visit the url of name 'administracion:administracion_usuarios' and check it loads the
        content of the user dashboard panel.
        """
        test_url_name = 'administracion:administracion_usuarios'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Usuarios'))

        # Check that the only user is displayed
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(self.browser.is_text_present('thelma'))
