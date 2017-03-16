from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from splinter import Browser
from perfiles_usuario.models import Capturista
from perfiles_usuario.utils import CAPTURISTA_GROUP
from estudios_socioeconomicos.models import Estudio
from django.test import TestCase


class TestCapturaEstudio(StaticLiveServerTestCase):
    """ Integration test suite for the creation fo estudios

    Attributes:
    -----------
    username : String
        Stores the username of the user that is created for the effect of
        these tests.
    password : String
        Stores the password of the user that is created for the effect of
        these tests.
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """ Create a new capturista that can fill a estudio, and opens
        a browser.

        """
        self.username = 'Eugenio420'
        self.password = 'pugnotpug'
        self.user = get_user_model().objects.create_user(
                                            username=self.username,
                                            password=self.password)
        Capturista.objects.create(user=self.user)
        self.browser = Browser('chrome')

    def tearDown(self):
        """ At the end of each test it closes the browser.

        """
        self.browser.quit()

    def create_group(self, group_name):
        """ Utility function to create a group and add the user to it.

        We receive the name of the group, create it, and bound it to the
        user.

        Parameters:
        -----------
        group_name : str
            The name of the group.
        """
        group = Group.objects.get_or_create(name=group_name)[0]
        group.user_set.add(self.user)
        group.save()

    def test_creation_of_new_study(self):
        """ Creates a new estudio and checks that it was actually created
        with a borrador status.
        """
        self.create_group(CAPTURISTA_GROUP)
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', self.username)
        self.browser.fill('password', self.password)
        self.browser.find_by_id('login-submit').click()
        starting_estudios_count = Estudio.objects.filter(status='borrador').count()
        self.browser.visit(self.live_server_url + reverse('captura:estudios'))
        self.browser.find_by_id('create_estudio').click()
        new_estudios_count = Estudio.objects.filter(status='borrador').count()
        self.assertEqual(new_estudios_count, starting_estudios_count + 1)
        
class TestViewsCaptura(TestCase):
    """Integration test suite for testing the views in the app: captura.

    Test the urls for 'captura' which make up the captura dashboard.

    """

    def test_estudio_housing(self):
        """ Test for the view that shows the housing of a family.

        """
        test_url_name = 'captura:housing'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)

    def test_captura_estudios(self):
        """ Test for the view that shows the list of pending studies.

        """
        test_url_name = 'captura:estudios'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)

    def test_captura_family(self):
        """ Test for the view that shows the members of a family.

        """
        test_url_name = 'captura:family'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)

    def test_estudio_income(self):
        """ Test for the view that shows the income of a family.

        """
        test_url_name = 'captura:income'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)

    def test_estudio_sections(self):
        """ Test for the view that shows all sections of a study's focus mode.

        """
        test_url_name = 'captura:sections'
        response = self.client.get(reverse(test_url_name), follow=True)
        self.assertEqual(200, response.status_code)
