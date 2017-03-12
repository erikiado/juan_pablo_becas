from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from splinter import Browser


class TestViewsCaptura(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: captura.

    Test the urls for 'captura' which make up the captura dashboard.

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

    def test_estudio_housing(self):
        """ Test for the view that shows the housing of a family.

        """
        test_url_name = 'captura:housing'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)

    def test_captura_estudios(self):
        """ Test for the view that shows the list of pending studies.

        """
        test_url_name = 'captura:estudios'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)

    def test_captura_family(self):
        """ Test for the view that shows the members of a family.

        """
        test_url_name = 'captura:family'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)

    def test_estudio_income(self):
        """ Test for the view that shows the income of a family.

        """
        test_url_name = 'captura:income'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)

    def test_estudio_sections(self):
        """ Test for the view that shows all sections of a study's focus mode.

        """
        test_url_name = 'captura:sections'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
