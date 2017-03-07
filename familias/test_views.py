from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from splinter import Browser


class TestViewsFamilias(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: familias.

    Test the urls for 'familias' which make up the administration dashboard.

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

    def test_all_families(self):
        """ Test for the view that shows all the families.

        """
        test_url_name = 'familias:all'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

    def test_family_member(self):
        """ Test for the view that shows a member of a family.

        """
        test_url_name = 'familias:member'
        self.browser.visit(self.live_server_url + reverse(test_url_name))
