from django.test import TestCase

from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP
from perfiles_usuario.models import Capturista
from .forms import FormaCreacionUsuario


class TestFormaCreacionUsuario(TestCase):
    """ Basic Suite for testing FormaCreacionUsuario.

    Test the basic purpose of the FormaCreacionUsuario: that the user is actually created and
    that it has the proper group assigned to it.

    Attributes
    ----------
    valid_data_form : dict
        A dictionary containing the data necessary for the form, which is used in all the
        individual tests.
    """

    def setUp(self):
        """ Setup the dictionary with data for feeding the form.
        """
        self.valid_data_form = {
            'username': 'raul',
            'first_name': 'raul',
            'last_name': 'arce',
            'email': 'elver@abc.com',
            'password': 'elver12312310'
        }

    def test_valid_data_basic(self):
        """ Test if the form assigns the proper group to a user.

        Test if the overriden save method inside FormaCreacionUsuario correctly assigns
        the administrador group to the user we are creating.
        """
        data_form = self.valid_data_form.copy()
        data_form['rol_usuario'] = ADMINISTRADOR_GROUP
        form = FormaCreacionUsuario(data_form)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.groups.filter(name=ADMINISTRADOR_GROUP).exists())

    def test_valid_data_capturista(self):
        """ Test if the form creates the Capturista.

        Test if the overriden save method inside FormaCreacionUsuario correctly creates the
        Capturista object when that role is selected.
        """
        data_form = self.valid_data_form.copy()
        data_form['rol_usuario'] = CAPTURISTA_GROUP
        form = FormaCreacionUsuario(data_form)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.groups.filter(name=CAPTURISTA_GROUP).exists())
        self.assertTrue(Capturista.objects.filter(user=user).exists())

    def test_invalid_data(self):
        """ Test if the form validates invalid data.

        Test if the Form is not valid if the role is missing.
        """
        data_form = self.valid_data_form.copy()
        form = FormaCreacionUsuario(data_form)
        self.assertFalse(form.is_valid())
