from django.test import TestCase
from django.contrib.auth.models import Group
from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, \
                                   DIRECTIVO_GROUP, SERVICIOS_ESCOLARES_GROUP


class TestLoadPeriodos(TestCase):
    """ Unit test suite for testing that initial data of
    Groups is created
    """

    def test_escuelas_created(self):
        """ Checks that this method __str__ method returns the name
        of the object.
        """
        self.assertTrue(Group.objects.get(name=ADMINISTRADOR_GROUP))
        self.assertTrue(Group.objects.get(name=CAPTURISTA_GROUP))
        self.assertTrue(Group.objects.get(name=DIRECTIVO_GROUP))
        self.assertTrue(Group.objects.get(name=SERVICIOS_ESCOLARES_GROUP))
