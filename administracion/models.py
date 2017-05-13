from django.db import models


class Escuela(models.Model):
    """ Model for Escuelas that are part of JPII organization.
    """
    nombre = models.CharField(max_length=80, null=False)

    def __str__(self):
        return self.nombre


class Colegiatura(models.Model):
    """ Model that will store the amount of money that is paid monthly
    in the institution.

    """
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        """ Print monto

        """
        return '${:.2f}'.format(self.monto)
