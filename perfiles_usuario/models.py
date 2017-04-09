from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group

from .utils import CAPTURISTA_GROUP


class Capturista(models.Model):
    """ Extension of Django's User Model for Capturistas.

    We extend the Django User Model to identify Capturistas since they have relations with
    other models and close interaction with the API.

    Attributes:
    ----------
    user : django.contrib.auth.models.User
        The django User related to Capturista (i.e. contains the actual user information).
    activo : BooleanField
        Indicates whether the profile is active or not.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """ Override the save method to add the capturista group.
        """
        user_group = Group.objects.get_or_create(name=CAPTURISTA_GROUP)[0]
        self.user.groups.add(user_group)
        return super(Capturista, self).save(*args, **kwargs)

    def __str__(self):
        """ Return the string representation of the user
        related to this capturista.
        """
        return str(self.user)
