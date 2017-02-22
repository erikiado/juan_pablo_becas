from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .utils import is_member, is_administrador, is_capturista, is_directivo, is_servicios_escolares
from .utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, \
                DIRECTIVO_GROUP, SERVICIOS_ESCOLARES_GROUP
from .models import Capturista


class PermisosTestCase(TestCase):
    """ Suite to test the validation functions inside utils.py.

    This Suite tests the functions designed to validate permissions of users in order
    to grant them access to views across the project.

    Attributes:
    ----------
    user : django.contrib.auth.models.User
        A mock user to use across all tests.
    directivo_group : django.contrib.auth.models.Group
        The group used to identify users that are directivos.
    administrador_group : django.contrib.auth.models.Group
        The group used to identify users that are administradores.
    servicios_group : : django.contrib.auth.models.Group
        The group used to identify users that are servicios_escolares.
    """

    def setUp(self):
        """ Initialize the attributes.
        """
        self.user = get_user_model().objects.create_user(
                                        username='some_user',
                                        email='temporary@gmail.com',
                                        password='some_pass')
        self.directivo_group = Group.objects.get_or_create(name=DIRECTIVO_GROUP)[0]
        self.administrador_group = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        self.servicios_group = Group.objects.get_or_create(name=SERVICIOS_ESCOLARES_GROUP)[0]

    def test_is_administrador(self):
        """ Test if the is_administrador works for the administrador group.

        Test if the is_administrador function works properly for a user which has
        the administrador group, and also if the same user gets some other group.
        We expect is_administrador to return True in both cases, since the user belongs
        to that group.
        """
        self.user.groups.add(self.administrador_group)
        self.assertTrue(is_administrador(self.user))
        self.user.groups.add(self.directivo_group)
        self.assertTrue(is_administrador(self.user))

    def test_not_admin(self):
        """ Test if the is_administrador fails for a user w/o the group.

        Test if the is_administrador fails for a user which does not have the
        administrador group assigned. We also add a different group and check that
        is_administrador fails again.
        """
        self.assertFalse(is_administrador(self.user))
        self.user.groups.add(self.directivo_group)
        self.assertFalse(is_administrador(self.user))

    def test_is_directivo(self):
        """ Test if the is_directivo works for the directivo group.

        Test if the is_directivo function works properly for a user which has
        the directivo group, and also if the same user gets some other group.
        We expect is_administrador to return True in both cases, since the user belongs
        to that group.
        """
        self.user.groups.add(self.directivo_group)
        self.assertTrue(is_directivo(self.user))
        self.user.groups.add(self.administrador_group)
        self.assertTrue(is_directivo(self.user))

    def test_not_directivo(self):
        """ Test if the is_directivo fails for a user w/o the group.

        Test if the is_directivo fails for a user which does not have the
        directivo group assigned. We also add a different group and check that
        is_administrador fails again.
        """
        self.assertFalse(is_directivo(self.user))
        self.user.groups.add(self.servicios_group)
        self.assertFalse(is_directivo(self.user))

    def test_is_servicios(self):
        """ Test if the is_servicios_escolares works for the servicios_escolares group.

        Test if the is_servicios_escolares function works properly for a user which has
        the servicios_escolares group, and also if the same user gets some other group.
        We expect is_servicios_escolares to return True in both cases, since the user belongs
        to that group.
        """
        self.user.groups.add(self.servicios_group)
        self.assertTrue(is_servicios_escolares(self.user))
        self.user.groups.add(self.administrador_group)
        self.assertTrue(is_servicios_escolares(self.user))

    def test_not_servicios(self):
        """ Test if the is_servicios_escolares fails for a user w/o the group.

        Test if the is_servicios_escolares fails for a user which does not have the
        servicios_escolares group assigned. We also add a different group and check that
        is_servicios_escolares fails again.
        """
        self.assertFalse(is_servicios_escolares(self.user))
        self.user.groups.add(self.directivo_group)
        self.assertFalse(is_servicios_escolares(self.user))

    def test_is_capturista(self):
        """ Test if the is_capturista works for the capturista group.

        Test if the is_capturista function works properly for a Capturista.
        """
        capturista = Capturista.objects.create(user=self.user)
        self.assertTrue(is_capturista(capturista.user))

    def test_not_capturista(self):
        """ Test if the is_capturista fails for a user w/o the group.

        Test if the is_capturista fails for a user which does not have the
        capturista group assigned. We also add a different group and check that
        is_capturista fails again.
        """
        self.assertFalse(is_capturista(self.user))
        self.user.groups.add(self.directivo_group)
        self.assertFalse(is_capturista(self.user))

    def test_is_member_invalid_group(self):
        """ Test if the is_member method fails for a non existing group.

        We validate that the is_member method returns false for a group
        that does not exist and is not assigned to the user.
        """
        self.assertFalse(is_member(self.user, ['blabla']))

    def test_is_member_multiple_groups(self):
        """ Test is_member with more than one group.

        Test that is_member validates correctly the existence of one group among others.
        That is, we check that a user who has two groups: servicio and directivo
        passes the test when we check against a list of more groups among which there is
        servicio and directivo.
        """
        self.user.groups.add(self.servicios_group)
        self.user.groups.add(self.directivo_group)
        self.assertTrue(is_member(self.user, [DIRECTIVO_GROUP, ADMINISTRADOR_GROUP]))
        self.assertTrue(is_member(self.user, [ADMINISTRADOR_GROUP, SERVICIOS_ESCOLARES_GROUP]))

    def test_is_not_member_multiple_groups(self):
        """ Test is_member with more than one group.

        Test that is_member fails when we ask if a user belongs to more than one group,
        when none of them is assigned to the user.
        """
        self.user.groups.add(self.servicios_group)
        self.user.groups.add(self.directivo_group)
        self.assertFalse(is_member(self.user, [ADMINISTRADOR_GROUP, CAPTURISTA_GROUP]))
