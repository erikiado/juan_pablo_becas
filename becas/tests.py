from django.test import TestCase
from django.core.urlresolvers import reverse


class TestUrlsBecas(TestCase):
    """Integration test suite for testing the URLs in the app: becas.

    Test the urls for 'becas' which make up the servicios escolares dashboard.

    """

    def test_reinscription_studies(self):
        """ Test for the view that shows the studies left to mark as a reinscription.

        """
        test_url_name = 'becas:services'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
