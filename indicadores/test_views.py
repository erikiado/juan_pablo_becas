from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from splinter import Browser


class TestViewsIndicadores(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: indicadores.

    Test the urls for 'indicadores' which make up the directivo dashboard.

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

    def test_all_indicadores(self):
        """ Test for the view that shows all the indicators.

        """
        test_url_name = 'indicadores:all'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

    def test_indicador_detail(self):
        """ Test for the view that shows the detail of a indicator.

        """
        test_url_name = 'indicadores:detail'
        self.browser.visit(self.live_server_url + reverse(test_url_name))
