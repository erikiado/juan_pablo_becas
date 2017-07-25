from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .calculators import estado_civil_counter, numero_de_alumnos


def f(x):
    return {
        'estado_civil': estado_civil_counter(),
        'numero_de_alumnos': numero_de_alumnos(),
    }.get(x, 'Indicador Inválido')

@login_required
def all_indicadores(request):
    """ DUMMY VIEW.

    This functions is currently just being used to test the redirect
    from base.

    TODO: name properly and implement everything
    """

    data_estado_civil = estado_civil_counter()
    context = {'data': data_estado_civil}
    return render(request, 'indicadores/charts.html', context)

@login_required
def specific_indicador(request, indicador):
    """ View for presenting a specific indicador, specified in the
    url.

    """
    context = {'data': f(indicador),
               'titulo': indicador}
    return render(request, 'indicadores/charts.html', context)

@login_required
def numero_alumnos(request):
    pass:

@login_required
def estado_civil(request):
