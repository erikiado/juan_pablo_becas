from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from django.contrib.auth.models import User


class TestAdministracionViews(StaticLiveServerTestCase):
    """Suite de integracion para probar las rutas administracion.

    Probar los urls de administracion que componen el panel administrativo en sus distintas
    vistas. Se crea un usuario para comprobar su despliegue en el panel de usuarios.

    Attributes
    ----------
    browser : Browser
        Driver para navegar por paginas web y para correr pruebas de integracion.
    """

    def setUp(self):
        """Inicializar el navegador, antes de correr las pruebas y crear un usuario.
        """
        self.browser = Browser('chrome')
        # Se crea usuario para comprobar despliegue de usuarios
        User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero')

    def tearDown(self):
        """Al terminar, cerrar el navegador.
        """
        self.browser.quit()

    def test_panel_principal(self):
        """Prueba sobre url 'administracion:administracion_principal'.

        Visitar el url de 'administracion:administracion_principal' y comprobar que cargue el
        contenido del panel principal.
        """
        test_url_name = 'administracion:administracion_principal'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Se comprueba que la pagina despliegue los textos esperados en el panel principal
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Se prueba si el include de la side_nav
        self.assertTrue(self.browser.is_text_present('Administración'))

    def test_panel_usuarios(self):
        """Prueba sobre url 'administracion:administracion_usuarios'.

        Visitar el url de 'administracion:administracion_usuarios' y comprobar que cargue el
        contenido del panel de usuarios.
        """
        test_url_name = 'administracion:administracion_usuarios'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Se comprueba que la pagina despliegue los textos esperados en el panel usuarios
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Se prueba si el include de la side_nav
        self.assertTrue(self.browser.is_text_present('Usuarios'))

        # Se revisa que el usuario se haya creado
        self.assertEqual(User.objects.count(), 1)

        # Se comprueba que se despliegue el usuario
        self.assertTrue(self.browser.is_text_present('thelma'))
