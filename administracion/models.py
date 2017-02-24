from django.db import models


class Escuela(models.Model):
    """ Model for Escuelas that are part of JPII organization.
    """
    nombre = models.CharField(max_length=80, null=False)

    def __str__(self):
        return self.nombre
