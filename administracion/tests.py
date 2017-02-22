from django.test import TestCase
from django.core.urlresolvers import reverse


class TestAdministracion(TestCase):
    """
    Suite unitario para probar las rutas administracion.

    Probar que los views de administracion regresen de manera correcta y que se utilice
    el template correcto.
    """

    def test_view_panel_principal(self):
        '''
        Unit Test: administracion.views.admin_panel_principal
        '''
        # self.client.login(username='user', password='test')
        test_url_name = 'administracion:administracion_principal'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'administracion/dashboard_main.html')

    def test_view_panel_usuarios(self):
        '''
        Unit Test: administracion.views.admin_panel_usuarios
        '''
        test_url_name = 'administracion:administracion_usuarios'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'administracion/dashboard_users.html')
