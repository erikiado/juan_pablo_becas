from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from django.contrib.auth.models import User


test_url = 'http://localhost:8081'


# Tests Integracion para las views de la app: administracion
class TestAdministracionViews(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = Browser('chrome')

        # Se crea usuario para comprobar despliegue de usuarios
        User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero')

    def tearDown(self):
        self.browser.quit()

    def test_panel_principal(self):
        test_url_name = 'administracion:administracion_principal'
        self.browser.visit(test_url + reverse(test_url_name))

        # Se comprueba que la pagina despliegue los textos esperados en el panel principal
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Se prueba si el include de la side_nav
        self.assertTrue(self.browser.is_text_present('Administración'))

    def test_panel_usuarios(self):
        test_url_name = 'administracion:administracion_usuarios'
        self.browser.visit(test_url + reverse(test_url_name))

        # Se comprueba que la pagina despliegue los textos esperados en el panel usuarios
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Se prueba si el include de la side_nav
        self.assertTrue(self.browser.is_text_present('Usuarios'))

        # Se revisa que el usuario se haya creado
        self.assertEqual(User.objects.count(), 1)

        # Se comprueba que se despliegue el usuario
        self.assertTrue(self.browser.is_text_present('thelma'))
