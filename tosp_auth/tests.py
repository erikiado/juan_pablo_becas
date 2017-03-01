from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from django.contrib.auth.models import User


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
        User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero')

    def tearDown(self):
        """At the end of tests, close the browser.
        """
        self.browser.quit()

    def test_option_does_not_appear(self):
        """Test: if the option log out appear for log users
        """
        self.client.login(username='thelma', password='junipero')
        self.browser.visit(self.live_server_url)
        self.assertTrue(self.browser.is_text_present('Log Out'))

    def test_option_appear_to_no_logged_client(self):
        """Test: if the option log out appear for not log users
        """
        self.browser.visit(self.live_server_url)
        self.assertFalse(self.browser.is_text_present('Log Out'))
