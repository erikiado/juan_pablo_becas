import decimal
from django.shortcuts import get_object_or_404
from indicadores.models import Transaccion
from .models import Familia, Integrante


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

def unformatted_total_ingresos_familia(id_familia):
    """ Return the total monthly earnings of a family.

    """
    familia = get_object_or_404(Familia, pk=id_familia)
    transacciones = Transaccion.objects.filter(familia=familia,
                                               activo=True,
                                               es_ingreso=True)
    total = decimal.Decimal('0')
    for transaccion in transacciones:
        total = total + transaccion.obtener_valor_mensual()

    return total

def education(id_integrante):
    """ Returns the simplified education of a family member

    """
    integrante = get_object_or_404(Integrante, pk=id_integrante)
    if integrante.nivel_estudios == 'ninguno':
        return 'none'
    elif (integrante.nivel_estudios == 'kinder_1' or 
          integrante.nivel_estudios == 'kinder_2' or
          integrante.nivel_estudios == 'kinder_3'):
        return 'kinder'
    elif (integrante.nivel_estudios == '1_grado' or
          integrante.nivel_estudios == '2_grado' or
          integrante.nivel_estudios == '3_grado' or
          integrante.nivel_estudios == '4_grado' or
          integrante.nivel_estudios == '5_grado' or
          integrante.nivel_estudios == '6_grado'):
        return 'primaria'
    elif (integrante.nivel_estudios == '7_grado' or
          integrante.nivel_estudios == '8_grado' or
          integrante.nivel_estudios == '9_grado'):
        return 'secundaria'
    elif (integrante.nivel_estudios == '10_grado' or
          integrante.nivel_estudios == '11_grado' or
          integrante.nivel_estudios == '12_grado'):
        return 'preparatoria'
    elif integrante.nivel_estudios == 'universidad':
        return 'universidad'
    elif (integrante.nivel_estudios == 'maestria' or
          integrante.nivel_estudios == 'doctorado'):
        return 'post-universitario'
    else:
        return 'unmatched'
