from django.db import models
from django.conf import settings

from estudios_socioeconomicos.models import Estudio

class Retroalimentacion(models.Model):
    estudio = models.ForeignKey(Estudio)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)

    fecha = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return '{usuario} - {fecha}: {descripcion}'.format(
                                                fecha=str(self.fecha),
                                                usuario=str(self.usuario),
                                                descripcion=self.descripcion[:40])

