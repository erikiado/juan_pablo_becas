from django.db import models
from familias.models import Alumno


class Beca(models.Model):
    """ Model for becas that are going to be awarded to
    students of the institution.

    """
    alumno = models.ForeignKey(Alumno)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_de_asignacion = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return '${:.2f} mensuales'.format(self.monto)
