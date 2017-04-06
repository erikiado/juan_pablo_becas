import decimal
from django.db import models
from familias.models import Familia, Tutor

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
        """ This returns the name of the Oficio

        """
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
    factor: DecimalField[12,10]
        This is the actual value that is used in calculations. It's
        purpose is to be able to calculate in the case of incomes and
        expenses how much the monto represents per month, by multiplying
        the income by this number.
    multiplica : BooleanField
        This dictates how the factor should be used in arithmetic
        operations. True for multiplication, false for division.
        This mitigates precision problems, in some operations.
    """

    periodicidad = models.TextField()
    factor = models.DecimalField(max_digits=12, decimal_places=10)
    multiplica = models.BooleanField()

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
    familia : ForeignKey
        This field matches a transaction with a family.
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
    familia = models.ForeignKey(Familia, related_name='transacciones')
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
        if not self.es_ingreso:
            valor_transaccion = valor_transaccion * decimal.Decimal('-1.0')
        if self.activo:
            return valor_transaccion
        else:
            return decimal.Decimal('0.0')

    def obtener_valor_mensual(self):
        """ Calculates how much money is exchanged in a month.

        """
        if self.periodicidad.multiplica:
            return self.obtener_valor_de_transaccion() * self.periodicidad.factor
        else:
            return self.obtener_valor_de_transaccion() / self.periodicidad.factor


    def __str__(self):
        """ Returns the calculated mensual transaction, formatted as money.

        """
        signo_opcional = ''
        valor_mensual_transaccion = self.obtener_valor_mensual()
        if valor_mensual_transaccion < decimal.Decimal('0.0'):
            signo_opcional = '-'
            valor_mensual_transaccion = valor_mensual_transaccion * decimal.Decimal('-1.0')
        return '{}${:.2f} mensuales'.format(signo_opcional, valor_mensual_transaccion)


class Ingreso(models.Model):
    """ This model extends de Transaccion model.

    This is a OneToOne relationship with Flujo that capital, that gets used
    whenever the income BooleanField in FlujoDeCapital is True.

    Attributes:
    -----------
    OPCIONES_TIPO : tuple(tuple)
        This touple stores the possible types of income a family can have.
    transaccion : OneToOneField
        This field indicates the transaction an instance of this model is extending.
    fecha : DateField
        This field indicates when an income was first received.
    tipo : TextField
        This field indicates the type of an income.
    tutor : ForeignKey
        This field indicates the parent to which an income can be attributed. It can
        be null in case no parent, is related to the income.
    """
    OPCION_NO_COMPROBABLE = 'no comprobable'
    OPCION_COMPROBABLE = 'comprobable'
    OPCIONES_TIPO = ((OPCION_NO_COMPROBABLE, 'No comprobable'),
                     (OPCION_COMPROBABLE, 'Comprobable'))
    transaccion = models.OneToOneField(Transaccion)
    fecha = models.DateField()
    tipo = models.CharField(max_length=100, choices=OPCIONES_TIPO)
    tutor = models.ForeignKey(Tutor, null=True)

    def __str__(self):
        """ This function returns the __str__ method of the parent transaction.

        """
        return '{}'.format(self.transaccion)
