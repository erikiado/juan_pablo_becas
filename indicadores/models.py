from django.db import models


class Oficio(models.Model):
    """ This model stores the list of all possible jobs.

    This list of jobs stores the information related to a family
    member, this model is used directly for the presentation and
    creation of the indicators related to the jobs of tutors.

    Attributes:
    -----------
    nombre : TextField
        This field stores the name of a job.
    """

    nombre = models.TextField()

    def __str__ (self):
        return '{}'.format(self.nombre)

class Periodo(models.Model):
    """ This model serves to mark how often an event happens.

    This model allows to store in other models how often
    something happens wich can reduce the amount of work needed
    to acquire data form the socioeconomical study, especially
    incomes and expenses.

    Attributes:
    -----------
    periodicidad : TextField
        This text stores a human readable value for how often a
        specific event happens e.g. Bimensual, Trimestral, etc.
    multiplicador: DecimalField[12,10]
        This is the actual value that is used in calculations. It's
        purpose is to be able to calculate in the case of incomes and
        expenses how much the monto represents per month, by multiplying
        the income by this number.
    """

    periodicidad = models.TextField()
    multiplicador = models.DecimalField(max_digits=12, decimal_places=10)

    def __str__(self):
        """ This returns the value or the periodicidad attribute

        """
        return '{}'.format(self.periodicidad)


class Ingreso(models.Model):
    """ This model details an income a family has.

    Incomes are very important as they are used to directly
    calculate the scholarship of a student, and are an essential 
    part of the calulation of many of the indicators that are going
    to be displayed.

    Attributes:
    -----------
    activo : boolean
        This field indicates whether a certain income is currently
        being received by the family.
    fecha : DateField
        This field indicates when an income was first received.
    monto : DecimalField[12,2]
        This field stores the acutal monetary amount the family receives
        from an income. The currency of this amount is MXN.
    periodicidad : ForeignKey
        This field references the value of how often the income is received
        by the family.
    observacion : Text
        This field stores any additional comments that clarify something
        about the income.

    """

    activo = models.BooleanField(default=True)
    fecha = models.DateTimeField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    periodicidad = models.ForeignKey(Periodo)
    observacion = models.TextField()

    def obtener_valor_mensual(self):
        """ Calculates how is received from an income in a month.

        """
        return self.monto * self.periodicidad.multiplicador

    def __str__(self):
        """ Returns the calculated mensual income, formatted as money.

        """
        return '${mensual_income} mensuales'.format(mensual_income=obtener_valor_mensual())



