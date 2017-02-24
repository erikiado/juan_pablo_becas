from django.test import TestCase
from django.core.urlresolvers import reverse


class TestAdministracion(TestCase):
    """Unit test suite for testing the views in the app: administracion.

    Test that the views for 'administracion' are correctly received as a response and that
    they use the correct template.
    """

    def test_view_main_dashboard(self):
        """Unit Test: administracion.views.admin_main_dashboard.
        """
        # self.client.login(username='user', password='test')
        test_url_name = 'administracion:main'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'administracion/dashboard_main.html')

    def test_view_users_dashboard(self):
        """Unit Test: administracion.views.admin_users_dashboard.
        """
        test_url_name = 'administracion:users'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'administracion/dashboard_users.html')
