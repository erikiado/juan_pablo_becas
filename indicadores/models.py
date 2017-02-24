from django.db import models
from familias.models import Familia

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

    def __str__(self):
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


class Transaccion(models.Model):
    """ This model details the income and expenses of a family has.

    Incomes are very important as they are used to directly
    calculate the scholarship of a student, and are an essential
    part of the calulation of many of the indicators that are going
    to be displayed.

    Attributes:
    -----------
    activo : boolean
        This field indicates whether a certain transaction is currently
        being transacted by the family.
    monto : DecimalField[12,2]
        This field stores the acutal monetary amount that gets exchanged.
        The currency of this amount is MXN.
    periodicidad : ForeignKey
        This field references the value of how often the mone is exchanged
        by the family.
    observacion : Text
        This field stores any additional comments that clarify something
        about the transaction.
    es_ingreso : BooleanField
        This field indicates whether a certain transaction is an income
        or an expense.
    """
    familia = models.ForeignKey(Familia)
    activo = models.BooleanField(default=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    periodicidad = models.ForeignKey(Periodo)
    observacion = models.TextField()
    es_ingreso = models.BooleanField()

    def obtener_valor_de_transaccion(self):
        """ If a transaction is an expense, returns a negative value

        This method gives you the value of a transaction, and is the
        correct way of getting this value.
        """
        valor_transaccion = self.monto
        if self.es_ingreso is not True:
            valor_transaccion = valor_transaccion * -1.0
        return valor_transaccion

    def obtener_valor_mensual(self):
        """ Calculates how much money is exchanged in a month.

        """
        return self.obtener_valor_de_transaccion() * self.periodicidad.multiplicador

    def __str__(self):
        """ Returns the calculated mensual transaction, formatted as money.

        """
        signo_opcional = ''
        valor_mensual_transaccion = self.obtener_valor_mensual()
        if valor_mensual_transaccion < 0.0:
            signo_opcional = '-'
            valor_mensual_transaccion = valor_mensual_transaccion * -1
        argumentos_format = {'signo': signo_opcional,
                             'mensual_transaccion': valor_mensual_transaccion}
        return '{signo}${mensual_transaccion:.2f} mensuales'.format(argumentos_format)


class Ingreso(models.Model):
    """ This model extends de Transaccion model.

    This is a OneToOne relationship with Flujo that capital, that gets used
    whenever the income BooleanField in FlujoDeCapital is True.

    Attributes:
    -----------
    OPCIONES_TIPO : tuple(tuple)
        This touple stores the possible types of income a family can have.
    fecha : DateField
        This field indicates when an income was first received.
    tipo : TextField
        This field indicates the type of an income.
    """
    OPCIONES_TIPO = (('no comprobable', 'No comprobable'),
                     ('comprobable', 'Comprobable'))
    fecha = models.DateTimeField()
    tipo = models.TextField(choices=OPCIONES_TIPO)
