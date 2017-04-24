import decimal
from django.shortcuts import get_object_or_404
from indicadores.models import Transaccion
from .models import Familia


def total_egresos_familia(id_familia):
    """ Returns the total value of the losses a
    family has per month.

    """
    familia = get_object_or_404(Familia, pk=id_familia)
    transacciones = Transaccion.objects.filter(familia=familia,
                                               activo=True,
                                               es_ingreso=False)
    total = decimal.Decimal('0')
    for transaccion in transacciones:
        total = total + transaccion.obtener_valor_mensual()

    return '{:.2f}'.format(total)


def total_ingresos_familia(id_familia):
    """ Return the total monthly earnings of a family.

    """
    familia = get_object_or_404(Familia, pk=id_familia)
    transacciones = Transaccion.objects.filter(familia=familia,
                                               activo=True,
                                               es_ingreso=True)
    total = decimal.Decimal('0')
    for transaccion in transacciones:
        total = total + transaccion.obtener_valor_mensual()

    return '{:.2f}'.format(total)


def total_neto_familia(id_familia):
    """ Returns the net total income of a family.

    """
    familia = get_object_or_404(Familia, pk=id_familia)
    transacciones = Transaccion.objects.filter(familia=familia,
                                               activo=True)
    total = decimal.Decimal('0')
    for transaccion in transacciones:
        total = total + transaccion.obtener_valor_mensual()

    return '{:.2f}'.format(total)
