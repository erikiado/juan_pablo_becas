from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse


class TestViewsFamilias(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: familias.

    Test the urls for 'familias' which make up the administration dashboard.

    """

    def test_all_families(self):
        """ Test for the view that shows all the families.

        """
        test_url_name = 'familias:all'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)

    def test_family_member(self):
        """ Test for the view that shows a member of a family.

        """
        test_url_name = 'familias:member'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
