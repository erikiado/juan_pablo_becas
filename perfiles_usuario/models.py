from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group

from .utils import CAPTURISTA_GROUP


class Capturista(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """ Override the save method to add the capturista group.
        """
        user_group = Group.objects.get_or_create(name=CAPTURISTA_GROUP)[0]
        self.user.groups.add(user_group)
        return super(Capturista, self).save(*args, **kwargs)
