from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from splinter import Browser


class TestBaseViews(StaticLiveServerTestCase):
    """Suite de integracion para probar las rutas base.

    Probar los urls de home, y los accesos a los archivos de robots y humans.

    Attributes
    ----------
    browser : Browser
        Driver para navegar por paginas web y para correr pruebas de integracion.
    """

    def setUp(self):
        """Inicializar el navegador, antes de correr las pruebas.
        """
        self.browser = Browser('chrome')

    def tearDown(self):
        """Al terminar, cerrar el navegador.
        """
        self.browser.quit()

    def test_home(self):
        """Prueba sobre url 'base:home'.

        Visitar el url de nombre 'home' y comprobar que cargue el contenido.
        """
        self.browser.visit(self.live_server_url + reverse('home'))
        self.assertTrue(self.browser.is_text_present('Hello, world!'))

    def test_robots(self):
        """Prueba sobre url 'base:base_files'(robots.txt).

        Visitar el url de robots.txt y comprobar que cargue el archivo.
        """
        self.browser.visit(self.live_server_url + '/robots.txt')
        self.assertTrue(self.browser.is_text_present('robotstxt'))

    def test_humans(self):
        """Prueba sobre url 'base:base_files'(humans.txt).

        Visitar el url de humans.txt y comprobar que cargue el archivo.
        """
        self.browser.visit(self.live_server_url + '/humans.txt')
        self.assertTrue(self.browser.is_text_present('humanstxt'))
