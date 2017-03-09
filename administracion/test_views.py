import time
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group
from splinter import Browser
from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, DIRECTIVO_GROUP, \
                                   SERVICIOS_ESCOLARES_GROUP
from perfiles_usuario.models import Capturista


class TestViewsAdministracion(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: administracion.

    Test the urls for 'administracion' which make up the administration dashboard.
    A user is created in order to test they are displayed.

    Attributes
    ----------
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """Initialize the browser and create a user, before running the tests.

        """
        self.browser = Browser('chrome')
        test_username = 'thelma'
        test_password = 'junipero'
        thelma = User.objects.create_user(
            username=test_username, email='juan@pablo.com', password=test_password,
            first_name='Thelma', last_name='Thelmapellido')
        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(thelma)
        administrators.save()
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()

    def tearDown(self):
        """At the end of tests, close the browser.

        """
        self.browser.quit()

    def test_main_dashboard(self):
        """Test for url 'administracion:main'.

        Visit the url of name 'administracion:main' and check it loads the
        content of the main dashboard panel.
        """
        test_url_name = 'administracion:main'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Administración'))

    def test_users_dashboard(self):
        """Test for url 'administracion:users'.

        Visit the url of name 'administracion:users' and check it loads the
        content of the user dashboard panel.
        """
        test_url_name = 'administracion:users'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Usuarios'))

        # Check that the only user is displayed
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(self.browser.is_text_present('thelma'))
        self.assertTrue(self.browser.is_text_present(ADMINISTRADOR_GROUP))

    def test_create_user_dashboard(self):
        """Test for create user from dashboard form.

        Visit the url of name 'administracion:users' and create some users with different
        roles and check they are created.
        """
        test_url_name = 'administracion:users'
        self.browser.visit(self.live_server_url + reverse(test_url_name))
        self.send_create_user_form('Eugenio420', 'Eugenio', 'Mar', 'eugenio@sjp.com',
                                   DIRECTIVO_GROUP)
        self.send_create_user_form('SimonETA', 'Simoneta', 'Mar', 'simoneta@sjp.com',
                                   SERVICIOS_ESCOLARES_GROUP)
        self.send_create_user_form('Pug03', 'Muffin', 'Mer', 'muffin@sjp.com', CAPTURISTA_GROUP)

        # Check user creation.
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(Capturista.objects.count(), 1)

        # Check that all users are displayed.
        self.assertTrue(self.browser.is_text_present('Eugenio'))
        self.assertTrue(self.browser.is_text_present('Simoneta'))
        self.assertTrue(self.browser.is_text_present('Muffin'))

        # Check all roles are displayed correctly.
        self.assertTrue(self.browser.is_text_present(ADMINISTRADOR_GROUP))
        self.assertTrue(self.browser.is_text_present(DIRECTIVO_GROUP))
        self.assertTrue(self.browser.is_text_present(CAPTURISTA_GROUP))
        self.assertTrue(self.browser.is_text_present(SERVICIOS_ESCOLARES_GROUP))

    def test_invalid_create_user_dashboard(self):
        """Test for create user from dashboard form.

        Visit the url of name 'administracion:users' and try to create some invalid users
        and check they are not created. The validation tested are: valid email, valid username
        and valid password.
        """
        test_url_name = 'administracion:users'
        self.browser.visit(self.live_server_url + reverse(test_url_name))
        # Send invalid email.
        self.send_create_user_form('Eugenio420', 'Eugenio', 'Mar', 'eugeniosjp.com',
                                   DIRECTIVO_GROUP)
        # Revisit the url since it should not be sent.
        self.browser.visit(self.live_server_url + reverse(test_url_name))
        # Send invalid username.
        self.send_create_user_form('', 'Simoneta', 'Mar', 'simoneta@sjp.com',
                                   SERVICIOS_ESCOLARES_GROUP)
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check no user created.
        self.browser.visit(self.live_server_url + reverse(test_url_name))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Capturista.objects.count(), 0)

        # Check that all users are displayed.
        self.assertFalse(self.browser.is_text_present('Eugenio'))
        self.assertFalse(self.browser.is_text_present('Simoneta'))
        self.assertFalse(self.browser.is_text_present('Muffin'))

        # Check all roles are displayed correctly
        self.assertFalse(self.browser.is_text_present(DIRECTIVO_GROUP))
        self.assertFalse(self.browser.is_text_present(CAPTURISTA_GROUP))
        self.assertFalse(self.browser.is_text_present(SERVICIOS_ESCOLARES_GROUP))

    def send_create_user_form(self, username, first_name, last_name, email, role):
        """Function which fills the user creation form and tries to send it.

        """
        self.browser.find_by_id('btn_modal_create_user').click()
        time.sleep(0.5)
        self.browser.find_by_id('id_username').first.fill(username)
        self.browser.find_by_id('id_first_name').first.fill(first_name)
        self.browser.find_by_id('id_last_name').first.fill(last_name)
        self.browser.find_by_id('id_email').first.fill(email)
        self.browser.find_by_id('id_rol_usuario').select(role)
        self.browser.find_by_id('btn_send_create_user').click()
        time.sleep(0.1)

    def test_edit_user_dashboard(self):
        """Test for create user from dashboard form.

        Visit the url of name 'administracion:users', create a user and update it with different
        roles and check it is correctly displayed.
        """
        test_url_name = 'administracion:users'
        self.browser.visit(self.live_server_url + reverse(test_url_name))
        self.send_create_user_form('Eugenio420', 'Eugenio', 'Mar', 'eugenio@sjp.com',
                                   DIRECTIVO_GROUP)

        # Check user creation.
        self.assertEqual(User.objects.count(), 2)
        test_user = User.objects.get(email='eugenio@sjp.com')

        self.browser.reload()
        # Check the new user is displayed
        self.assertTrue(self.browser.is_text_present('Eugenio420'))
        self.assertTrue(self.browser.is_text_present('Eugenio'))
        self.assertTrue(self.browser.is_text_present('Mar'))
        self.assertTrue(self.browser.is_text_present('eugenio@sjp.com'))
        self.assertTrue(self.browser.is_text_present(DIRECTIVO_GROUP))

        # Update the user role and username and check they are correctly displayed
        self.send_update_user_form(test_user.pk, username='Eugenio421', role=CAPTURISTA_GROUP)
        self.assertFalse(self.browser.is_text_present(DIRECTIVO_GROUP))
        self.assertTrue(self.browser.is_text_present(CAPTURISTA_GROUP))
        self.assertTrue(self.browser.is_text_present('Eugenio421'))
        self.assertEqual(Capturista.objects.count(), 1)

        # Update the user and check the roles are updated and the Capturista role deleted.
        self.send_update_user_form(test_user.pk, first_name='Marcos',
                                   role=SERVICIOS_ESCOLARES_GROUP)
        self.assertFalse(self.browser.is_text_present(CAPTURISTA_GROUP))
        self.assertTrue(self.browser.is_text_present(SERVICIOS_ESCOLARES_GROUP))
        self.assertTrue(self.browser.is_text_present('Marcos'))
        self.assertEqual(Capturista.objects.count(), 0)

    def send_update_user_form(self, pk, username=False, first_name=False, last_name=False,
                              email=False, role=False):
        """Function which fills the user update form and tries to send it.

        This function initializes everything as False so each field is updated only if it is
        given as a parameter.
        """
        self.browser.find_by_id('update_user_'+str(pk)).click()
        time.sleep(0.5)
        if username:
            search_xpath = '//DIV[@id="modal_edit_user"]//INPUT[@id="id_username"]'
            self.browser.find_by_xpath(search_xpath).fill(username)
        if first_name:
            search_xpath = '//DIV[@id="modal_edit_user"]//INPUT[@id="id_first_name"]'
            self.browser.find_by_xpath(search_xpath).fill(first_name)
        if last_name:
            search_xpath = '//DIV[@id="modal_edit_user"]//INPUT[@id="id_last_name"]'
            self.browser.find_by_xpath(search_xpath).fill(last_name)
        if email:
            search_xpath = '//DIV[@id="modal_edit_user"]//INPUT[@id="id_email"]'
            self.browser.find_by_xpath(search_xpath).fill(email)
        if role:
            search_xpath = '//DIV[@id="modal_edit_user"]\
                            //SELECT[@id="id_rol_usuario"]\
                            //OPTION[@value="' + role + '"]'
            self.browser.find_by_xpath(search_xpath).click()
        self.browser.find_by_id('btn_send_edit_user').click()

    def test_login_created_user(self):
        """Test for creating user from dashboard and then login with it.

        Visit the url of name 'administracion:users', create a user, logout and then attempt to
        login with the created user.
        """
        test_url_name = 'administracion:users'
        self.browser.visit(self.live_server_url + reverse(test_url_name))
        self.send_create_user_form('Eugenio420', 'Eugenio', 'Mar', 'eugenio@sjp.com',
                                   DIRECTIVO_GROUP)

        # Check user creation.
        self.assertEqual(User.objects.count(), 2)
        test_user = User.objects.get(email='eugenio@sjp.com')

        self.browser.visit(self.live_server_url + reverse('tosp_auth:logout'))
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_user.username)
        # Fill the password with the generated password
        # This should be updated when the new password generation takes place
        self.browser.fill('password', test_user.first_name + '_' + test_user.last_name)
        self.browser.find_by_id('login-submit').click()

        # Check the user effectively logged in.
        self.assertTrue(self.browser.is_text_present('Hello, Eugenio Mar!'))
