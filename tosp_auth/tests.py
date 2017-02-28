from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class ControlerLogoutTest(TestCase):
    
    """Unit test suite for testing the controler of 
        Logout in the app: tosp_auth.

        Test that if the functionality of logout is correct.
    """
    
    def setUp(self):
        """Initialize the browser and create a user, before running the tests.
        """
        User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero')
            
    def test_logout_does_not_do_that(self):
        
        """Verify if the Logout works.
        """
        
        self.client.login(username='thelma', password='junipero')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log Out")
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "login")
        
        
    def test_expected_url(self):
        """Verify if redirect to the right url.
        """
        self.client.login(username='thelma', password='junipero')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        