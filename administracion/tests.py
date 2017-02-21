from django.test import TestCase
from django.core.urlresolvers import reverse


# Tests Unitarios para views.py de la app: administracion
class TestAdministracion(TestCase):

    # Unit Test: administracion.views.admin_dashboard
    def test_view_panel_principal(self):
        # self.client.login(username='user', password='test')
        test_url_name = 'administracion:administracion_principal'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'administracion/dashboard_main.html')

    # Unit Test: administracion.views.admin_dashboard
    def test_view_panel_usuarios(self):
        # self.client.login(username='user', password='test')
        test_url_name = 'administracion:administracion_usuarios'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'administracion/dashboard_users.html')
