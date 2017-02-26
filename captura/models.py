from django.db import models
from django.conf import settings

from estudios_socioeconomicos.models import Estudio


class Retroalimentacion(models.Model):
    """ The model that represents the feedback on a study.

    This model contains the feedback left either by the admin or
    by a capturista on a study during the review process.

    Attributes:
    -----------
    usuario : User
        The user who writes the feedback. It may be either the admin or
        the capturista.
    fecha : DateTimeField
        The time at which the feedback is filled.
    descripcion : TextField
        The actual feedback text.
    activo : BooleanField
        Boolean indicating whether this feedback should be shown or not.
    """
    estudio = models.ForeignKey(Estudio)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)

    fecha = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return '{usuario} - {fecha}: {descripcion}'.format(
                                                fecha=str(self.fecha),
                                                usuario=str(self.usuario),
                                                descripcion=self.descripcion[:40])
