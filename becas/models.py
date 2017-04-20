from django.db import models
from familias.models import Alumno


class Beca(models.Model):
    """ Model for becas that are going to be awarded to
    students of the institution.

    """
    OPCIONES_PORCENTAJE = [
        (x, x + '%') for x in map(lambda x: str(x), range(1, 101))
    ]
    alumno = models.ForeignKey(Alumno)
    porcentaje = models.CharField(max_length=5,
                                  choices=OPCIONES_PORCENTAJE,
                                  default='0')
    fecha_de_asignacion = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return '{}%'.format(self.porcentaje)
