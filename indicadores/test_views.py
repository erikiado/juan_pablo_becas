from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse


class TestViewsIndicadores(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: indicadores.

    Test the urls for 'indicadores' which make up the directivo dashboard.

    Attributes
    ----------
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def test_all_indicadores(self):
        """ Test for the view that shows all the indicators.

        """
        test_url_name = 'indicadores:all'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)

    def test_indicador_detail(self):
        """ Test for the view that shows the detail of a indicator.

        """
        test_url_name = 'indicadores:detail'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
