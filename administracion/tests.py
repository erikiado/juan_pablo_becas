# from django.test import TestCase
from django.test import TestCase
from django.core.urlresolvers import reverse


# Create your tests here.
class TestAdministracion(TestCase):

    # self.client.login(username='user', password='test')
    # defined in fixture or with factory in setUp()
    def test_view_panel_principal(self):
        response = self.client.get(
                    reverse('administracion:administracion_panel'), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'administracion/dashboard_main.html')
