# from django.test import TestCase
from django.test import TestCase
from django.core.urlresolvers import reverse
from splinter import Browser


# # Create your tests here.
class TestAdministracionViews(TestCase):

    def setUp(self):
        self.browser = Browser('chrome')

    def tearDown(self):
        self.browser.quit()

    def test_panel_principal(self):
        self.browser.visit('http://localhost:8000' +
                           reverse('administracion:administracion_panel'))
        test_string = 'Instituto Juan Pablo'
        self.assertTrue(self.browser.is_text_present(test_string))

    def test_panel_usuarios(self):
        self.browser.visit('http://localhost:8000' +
                           reverse('administracion:administracion_usuarios'))
        test_string = 'Usuarios'
        self.assertTrue(self.browser.is_text_present(test_string))
