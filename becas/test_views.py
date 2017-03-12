from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from splinter import Browser


class TestViewsBecas(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: becas.

    Test the urls for 'becas' which make up the servicios escolares dashboard.

    Attributes
    ----------
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """Initialize the browser and create a user, before running the tests.

        """
        self.browser = Browser('chrome')

    def tearDown(self):
        """At the end of tests, close the browser.

        """
        self.browser.quit()

    def test_reinscription_studies(self):
        """ Test for the view that shows the studies left to mark as a reinscription.

        """
        test_url_name = 'becas:services'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
