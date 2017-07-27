from django.test import TestCase
from django.contrib.auth.models import Group
from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, \
                                   DIRECTIVO_GROUP, SERVICIOS_ESCOLARES_GROUP


class TestLoadGroups(TestCase):
    """ Unit test suite for testing that initial data of
    Groups are created
    """

    def test_groups_created(self):
        """ Checks that the appropriate groups for the application have
        been created.
        
        """
        self.assertTrue(Group.objects.get(name=ADMINISTRADOR_GROUP))
        self.assertTrue(Group.objects.get(name=CAPTURISTA_GROUP))
        self.assertTrue(Group.objects.get(name=DIRECTIVO_GROUP))
        self.assertTrue(Group.objects.get(name=SERVICIOS_ESCOLARES_GROUP))
