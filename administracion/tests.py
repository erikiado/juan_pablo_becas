from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP
from perfiles_usuario.models import Capturista
from .forms import UserForm, DeleteUserForm


class TestAdministracionUrls(TestCase):
    """Unit test suite for testing the views in the app: administracion.

    Test that the views for 'administracion' are correctly received as a response and that
    they use the correct template.
    """

    def setUp(self):
        thelma = User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero',
            first_name='Thelma', last_name='Amlet')
        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(thelma)
        self.client.login(username='thelma', password='junipero')

    def test_view_main_dashboard(self):
        """Unit Test: administracion.views.admin_main_dashboard.

        """
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


class TestUserForm(TestCase):
    """Basic Suite for testing UserForm.

    Test the basic purpose of the UserForm: that the user is actually created and
    that it has the proper group assigned to it.

    Attributes
    ----------
    valid_data_form : dict
        A dictionary containing the data necessary for the form, which is used in all the
        individual tests.
    """

    def setUp(self):
        """Setup the dictionary with data for feeding the form.

        """
        self.valid_data_form = {
            'username': 'raul',
            'first_name': 'raul',
            'last_name': 'arce',
            'email': 'elver@abc.com',
            'password': 'elver12312310'
        }
        self.thelma = User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero',
            first_name='Thelma', last_name='Thelmapellido')

    def test_valid_data_basic(self):
        """Test if the form assigns the proper group to a user.

        Test if the overriden save method inside UserForm correctly assigns
        the administrador group to the user we are creating.
        """
        data_form = self.valid_data_form.copy()
        data_form['rol_usuario'] = ADMINISTRADOR_GROUP
        form = UserForm(data_form)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.groups.filter(name=ADMINISTRADOR_GROUP).exists())

    def test_valid_data_capturista(self):
        """Test if the form creates the Capturista.

        Test if the overriden save method inside UserForm correctly creates the
        Capturista object when that role is selected.
        """
        data_form = self.valid_data_form.copy()
        data_form['rol_usuario'] = CAPTURISTA_GROUP
        form = UserForm(data_form)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.groups.filter(name=CAPTURISTA_GROUP).exists())
        self.assertTrue(Capturista.objects.filter(user=user).exists())

    def test_invalid_data(self):
        """Test if the form validates invalid data.

        Test if the Form is not valid if the role is missing.
        """
        data_form = self.valid_data_form.copy()
        form = UserForm(data_form)
        self.assertFalse(form.is_valid())


class TestDeleteUserForm(TestCase):
    """Basic Suite for testing DeleteUserForm.

    Test the basic purpose of the DeleteUserForm: that the user is actually deleted from database.

    Attributes
    ----------
    valid_data_form : dict
        A dictionary containing the data necessary for the form, which is used in all the
        individual tests.
    """

    def setUp(self):
        """Setup the dictionary with data for feeding the form.

        """
        self.thelma = User.objects.create_user(
            username='thelma', email='juan@pablo.com', password='junipero',
            first_name='Thelma', last_name='Thelmapellido')
        self.valid_data_form = {
            'user_id': str(self.thelma.pk)
        }

    def test_valid_data_basic(self):
        """Test if the form effectively deletes the user instance

        """
        data_form = self.valid_data_form.copy()
        form = DeleteUserForm(data_form)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(User.objects.count(), 0)
        try:
            test_user = User.objects.get(pk=self.valid_data_form['user_id'])
        except User.DoesNotExist:
            test_user = None
        self.assertEqual(test_user, None)

    def test_invalid_data(self):
        """Test if the form validates invalid data.

        """
        data_form = self.valid_data_form.copy()
        data_form['user_id'] = 'id falso'
        form = DeleteUserForm(data_form)
        self.assertFalse(form.is_valid())
