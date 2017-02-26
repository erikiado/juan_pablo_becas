from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token

from .utils import CAPTURISTA_GROUP, ADMINISTRADOR_GROUP, is_member


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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_authentication_token(sender, instance=None, created=False, **kwargs):
    """ Signal for creating a new Token when after a user is saved.

    To authenticate a user using the desktop application we will be using auth tokens.
    Rest framework provides us with this functionality but we need to create a Token for
    each user.

    Attributes:
    ----------
    instance : django.contrib.auth.models.User
        The instance of the object whose creation triggered the signal. In this case a
        django user.
    created : BooleanField
        A value indicating if this instance is being created for the first time. Or if set
        to false if it is being edited.
    """
    if created and is_member(instance, [CAPTURISTA_GROUP, ADMINISTRADOR_GROUP]):
        Token.objects.create(user=instance)
