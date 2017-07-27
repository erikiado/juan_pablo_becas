from collections import OrderedDict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .calculators import estado_civil_counter, numero_de_alumnos
from familias.models import Familia, Oficio, Integrante, Alumno
from familias.utils import total_ingresos_familia


@login_required
def breakdown_alumnos(request):
    total_alumnos = Alumno.objects.filter(integrante__activo=True).count()

    alumnos_grado = {}
    alumnos_grado['1ro de Primaria'] = Alumno.objects.filter(integrante__activo=True,
                                                                 integrante__nivel_estudios='1_grado').count()
    alumnos_grado['2do de Primaria'] = Alumno.objects.filter(integrante__activo=True,
                                                                 integrante__nivel_estudios='2_grado').count()
    alumnos_grado['3ro de Primaria'] = Alumno.objects.filter(integrante__activo=True,
                                                                 integrante__nivel_estudios='3_grado').count()
    alumnos_grado['4to de Primaria'] = Alumno.objects.filter(integrante__activo=True,
                                                                integrante__nivel_estudios='4_grado').count()
    alumnos_grado['5to de Primaria'] = Alumno.objects.filter(integrante__activo=True,
                                                                integrante__nivel_estudios='5_grado').count()
    alumnos_grado['6to de Primaria'] = Alumno.objects.filter(integrante__activo=True,
                                                               integrante__nivel_estudios='6_grado').count()

    alumnos_ordenados = OrderedDict(sorted(alumnos_grado.items(), key=lambda t: t[0]))
    context = {'total_alumnos': total_alumnos,
               'titulo': 'Desgloce de Alumnos',
               'data': alumnos_ordenados}
    return render(request, 'indicadores/breakdown_alumnos.html', context)


@login_required
def estado_civil(request):
    all_results = {}
    for localidad_option in Familia.OPCIONES_LOCALIDAD:
        results_localidad = {}
        for option in Familia.OPCIONES_ESTADO_CIVIL:
            results_localidad[option[1]] = Familia.objects.filter(estado_civil=option[0],
                                                       estudio__status__contains='aprobado',
                                                       localidad=localidad_option[0]).count()
            ordered_results = OrderedDict(sorted(results_localidad.items(), key=lambda t: t[0]))
        all_results[localidad_option[1]] = ordered_results
        all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))

    unified_total = {}
    for option in Familia.OPCIONES_ESTADO_CIVIL:
        unified_total[option[1]] = Familia.objects.filter(estudio__status__contains='aprobado',
                                                          estado_civil=option[0]).count()

    unified_ordered_total = OrderedDict(sorted(unified_total.items(), key=lambda t: t[0]))
    context = {'data': all_ordered_results,
               'titulo': 'Estado Civil',
               'unified_total': unified_ordered_total}
    return render(request, 'indicadores/estado_civil.html', context)

@login_required
def estudios_padres(request):
    pass


def edad_padres(request):
    pass

def ocupaciones(request):
    all_results = {}
    oficios = Oficio.objects.all()
    for localidad_option in Familia.OPCIONES_LOCALIDAD:
        results_localidad = {}
        for oficio in oficios:
            results_localidad[oficio.nombre] = Integrante.objects.filter(oficio=oficio,
                                                                  rol='Tutor',
                                                                  activo=True,
                                                                  familia__estudio__status__contains='aprobado',
                                                                  familia__localidad=localidad_option[0]).count()
            ordered_results = OrderedDict(sorted(results_localidad.items(), key=lambda t: t[0]))
        all_results[localidad_option[1]] = ordered_results
        all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))

    unified_total = {}
    for oficio in oficios:
        unified_total[oficio.nombre] = Integrante.objects.filter(familia__estudio__status__contains='aprobado',
                                                             rol='Tutor',
                                                             oficio=oficio).count()

    unified_ordered_total = OrderedDict(sorted(unified_total.items(), key=lambda t: t[0]))
    context = {'data': all_ordered_results,
               'titulo': 'Ocupaciones',
               'unified_total': unified_ordered_total}
    return render(request, 'indicadores/ocupaciones.html', context)

def ingreso_mensual(request):
    pass
    # unified_total = {}
    # all_results = {}
    # familias = Familia.objects.filter(estudio__status__contains='aprobado')
    # for localidad in Familia.OPCIONES_LOCALIDAD:
    #     all_results[localidad[0]] = {'0': 0,
    #                               '1000': 0,
    #                               '2000': 0,
    #                               '3000': 0,
    #                               '4000': 0,
    #                               '5000': 0,
    #                               '6000': 0,
    #                               '7000': 0,
    #                               '8000': 0,
    #                               '9000': 0,
    #                               '10000': 0,
    #                               '11000': 0,
    #                               '12000': 0,
    #                               '13000': 0,
    #                               '14000': 0,
    #                               '15000': 0,
    #                               '16000': 0,
    #                               '17000': 0,
    #                               '18000': 0}

    # unified_total[localidad] = {'0': 0,
    #                             '1000': 0,
    #                             '2000': 0,
    #                             '3000': 0,
    #                             '4000': 0,
    #                             '5000': 0,
    #                             '6000': 0,
    #                             '7000': 0,
    #                             '8000': 0,
    #                             '9000': 0,
    #                             '10000': 0,
    #                             '11000': 0,
    #                             '12000': 0,
    #                             '13000': 0,
    #                             '14000': 0,
    #                             '15000': 0,
    #                             '16000': 0,
    #                             '17000': 0,
    #                             '18000': 0}
    # for familia in familias:
    #     all_results[familia.localidad[str(int(total_ingresos_familia(familia.pk) / 1000) * 1000)]] = all_results[familia.localidad[str(int(total_ingresos_familia(familia.pk) / 1000) * 1000)]] + 1
    #     unified_total[int(total_ingresos_familia(familia.pk) / 1000) * 1000] = unified_total[int(total_ingresos_familia(familia.pk) / 1000) * 1000] + 1

    # all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))
    # unified_ordered_total = OrderedDict(sorted(unified_total.items(), key=lambda t: t[0]))
    
    # context = {'data': all_ordered_results,
    #            'titulo': 'Ingresos',
    #            'unified_total': unified_ordered_total}
    # return render(request, 'indicadores/ocupaciones.html', context)

def localidad(request):
    all_results = {}
    for localidad in Familia.OPCIONES_LOCALIDAD:
        all_results[localidad[1]] = Familia.objects.filter(estudio__status__contains='aprobado',
                                                           localidad=localidad[0]).count()

    all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))
    context = {'data': all_ordered_results, 'titulo': 'Distribución Familias'}
    return render(request, 'indicadores/localidad.html', context)

def sacramentos(request):
    pass

def becas(request):
    pass
