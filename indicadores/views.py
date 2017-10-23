from collections import OrderedDict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .calculators import estado_civil_counter, numero_de_alumnos
from becas.models import Beca
from familias.models import Familia, Oficio, Integrante, Alumno
from familias.utils import unformatted_total_ingresos_familia, education


@login_required
def breakdown_alumnos(request):
    total_alumnos = Alumno.objects.filter(integrante__activo=True).count()

    alumnos_grado = {}
    alumnos_grado['1ro de Kinder'] = Alumno.objects.filter(integrante__activo=True,
                                                            integrante__nivel_estudios='kinder_1').count()
    alumnos_grado['2do de Kinder'] = Alumno.objects.filter(integrante__activo=True,
                                                            integrante__nivel_estudios='kinder_2').count()
    alumnos_grado['3ro de Kinder'] = Alumno.objects.filter(integrante__activo=True,
                                                            integrante__nivel_estudios='kinder_3').count()
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
    unified_total = {}
    all_results = {}
    familias = Familia.objects.filter(estudio__status__contains='aprobado')
    for localidad in Familia.OPCIONES_LOCALIDAD:
        all_results[localidad[1]] = {'No Tiene': 0,
                                     'Kinder': 0,
                                     'Primaria': 0,
                                     'Secundaria': 0,
                                     'Preparatoria': 0,
                                     'Universidad': 0,
                                     'Post-universitario': 0}


    unified_total = {'No Tiene': 0,
                     'Kinder': 0,
                     'Primaria': 0,
                     'Secundaria': 0,
                     'Preparatoria': 0,
                     'Universidad': 0,
                     'Post-universitario': 0}
    

    for localidad in Familia.OPCIONES_LOCALIDAD:
        familias = Familia.objects.filter(estudio__status__contains='aprobado',
                                          localidad=localidad[0])
        for familia in familias:
            integrantes = Integrante.objects.filter(familia=familia,
                                                    activo=True)

            for integrante in integrantes:
                if hasattr(integrante, 'tutor_integrante'):
                    if education(integrante.pk) is 'none':
                        all_results[localidad[1]]['No Tiene'] = all_results[localidad[1]]['No Tiene'] + 1
                    elif education(integrante.pk) is 'kinder':
                        all_results[localidad[1]]['Kinder'] = all_results[localidad[1]]['Kinder'] + 1
                    elif education(integrante.pk) is 'primaria':
                        all_results[localidad[1]]['Primaria'] = all_results[localidad[1]]['Primaria'] + 1
                    elif education(integrante.pk) is 'secundaria':
                        all_results[localidad[1]]['Secundaria'] = all_results[localidad[1]]['Secundaria'] + 1
                    elif education(integrante.pk) is 'preparatoria':
                        all_results[localidad[1]]['Preparatoria'] = all_results[localidad[1]]['Preparatoria'] + 1
                    elif education(integrante.pk) is 'unversidad':
                        all_results[localidad[1]]['Universidad'] = all_results[localidad[1]]['Universidad'] + 1
                    elif education(integrante.pk) is 'post-universitario':
                        all_results[localidad[1]]['Post-universitario'] = all_results[localidad[1]]['Post-universitario'] + 1

        all_results[localidad[1]] = OrderedDict(sorted(all_results[localidad[1]].items(), key=lambda t: t[0]))

    familias = Familia.objects.filter(estudio__status__contains='aprobado')

    for familia in familias:
        integrantes = Integrante.objects.filter(familia=familia,
                                                activo=True)
        for integrante in integrantes:
            if hasattr(integrante, 'tutor_integrante'):
                if education(integrante.pk) is 'none':
                    unified_total['No Tiene'] = unified_total['No Tiene'] + 1
                elif education(integrante.pk) is 'kinder':
                    unified_total['Kinder'] = unified_total['Kinder'] + 1
                elif education(integrante.pk) is 'primaria':
                    unified_total['Primaria'] = unified_total['Primaria'] + 1
                elif education(integrante.pk) is 'secundaria':
                    unified_total['Secundaria'] = unified_total['Secundaria'] + 1
                elif education(integrante.pk) is 'preparatoria':
                    unified_total['Preparatoria'] = unified_total['Preparatoria'] + 1
                elif education(integrante.pk) is 'unversidad':
                    unified_total['Universidad'] = unified_total['Universidad'] + 1
                elif education(integrante.pk) is 'post-universitario':
                    unified_total['Post-universitario'] = unified_total['Post-universitario'] + 1

    all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))
    unified_ordered_total = OrderedDict(sorted(unified_total.items(), key=lambda t: t[0]))

    context = {'data': all_ordered_results,
               'titulo': 'Educación Padres',
               'unified_total': unified_ordered_total}
    return render(request, 'indicadores/ocupaciones.html', context)


def edad_padres(request):
    unified_total = {}
    all_results = {}
    familias = Familia.objects.filter(estudio__status__contains='aprobado')
    for localidad in Familia.OPCIONES_LOCALIDAD:
        all_results[localidad[1]] = {'10 - 15 años': 0,
                                     '15 - 20 años': 0,
                                     '20 - 25 años': 0,
                                     '25 - 30 años': 0,
                                     '30 - 35 años': 0,
                                     '35 - 40 años': 0,
                                     '40 - 45 años': 0,
                                     '45 - 50 años': 0,
                                     '50 - 55 años': 0,
                                     '55 - 60 años': 0,
                                     '+60 años': 0}


    unified_total = {'10 - 15 años': 0,
                     '15 - 20 años': 0,
                     '20 - 25 años': 0,
                     '25 - 30 años': 0,
                     '30 - 35 años': 0,
                     '35 - 40 años': 0,
                     '40 - 45 años': 0,
                     '45 - 50 años': 0,
                     '50 - 55 años': 0,
                     '55 - 60 años': 0,
                     '+60 años': 0}
    

    for localidad in Familia.OPCIONES_LOCALIDAD:
        familias = Familia.objects.filter(estudio__status__contains='aprobado',
                                          localidad=localidad[0])
        for familia in familias:
            integrantes = Integrante.objects.filter(familia=familia,
                                                    activo=True)

            for integrante in integrantes:
                if hasattr(integrante, 'tutor_integrante'):
                    if integrante.age() >= 10 and integrante.age() < 15:
                        all_results[localidad[1]]['10 - 15 años'] = all_results[localidad[1]]['10 - 15 años'] + 1
                    elif integrante.age() >= 15 and integrante.age() < 20:
                        all_results[localidad[1]]['15 - 20 años'] = all_results[localidad[1]]['15 - 20 años'] + 1
                    elif integrante.age() >= 20 and integrante.age() < 25:
                        all_results[localidad[1]]['20 - 25 años'] = all_results[localidad[1]]['20 - 25 años'] + 1
                    elif integrante.age() >= 25 and integrante.age() < 30:
                        all_results[localidad[1]]['25 - 30 años'] = all_results[localidad[1]]['25 - 30 años'] + 1
                    elif integrante.age() >= 30 and integrante.age() < 35:
                        all_results[localidad[1]]['30 - 35 años'] = all_results[localidad[1]]['30 - 35 años'] + 1
                    elif integrante.age() >= 35 and integrante.age() < 40:
                        all_results[localidad[1]]['35 - 40 años'] = all_results[localidad[1]]['35 - 40 años'] + 1
                    elif integrante.age() >= 40 and integrante.age() < 45:
                        all_results[localidad[1]]['40 - 45 años'] = all_results[localidad[1]]['40 - 45 años'] + 1
                    elif integrante.age() >= 45 and integrante.age() < 50:
                        all_results[localidad[1]]['45 - 50 años'] = all_results[localidad[1]]['45 - 50 años'] + 1
                    elif integrante.age() >= 50 and integrante.age() < 55:
                        all_results[localidad[1]]['50 - 55 años'] = all_results[localidad[1]]['50 - 55 años'] + 1
                    elif integrante.age() >= 55 and integrante.age() < 60:
                        all_results[localidad[1]]['55 - 60 años'] = all_results[localidad[1]]['55 - 60 años'] + 1
                    else:
                        all_results[localidad[1]]['+60 años'] = all_results[localidad[1]]['+60 años'] + 1

        all_results[localidad[1]] = OrderedDict(sorted(all_results[localidad[1]].items(), key=lambda t: t[0]))

    familias = Familia.objects.filter(estudio__status__contains='aprobado')

    for familia in familias:
        integrantes = Integrante.objects.filter(familia=familia,
                                                activo=True)

        for integrante in integrantes:
            if hasattr(integrante, 'tutor_integrante'):
                if integrante.age() >= 10 and integrante.age() < 15:
                    unified_total['10 - 15 años'] = unified_total['10 - 15 años'] + 1
                elif integrante.age() >= 15 and integrante.age() < 20:
                    unified_total['15 - 20 años'] = unified_total['15 - 20 años'] + 1
                elif integrante.age() >= 20 and integrante.age() < 25:
                    unified_total['20 - 25 años'] = unified_total['20 - 25 años'] + 1
                elif integrante.age() >= 25 and integrante.age() < 30:
                    unified_total['25 - 30 años'] = unified_total['25 - 30 años'] + 1
                elif integrante.age() >= 30 and integrante.age() < 35:
                    unified_total['30 - 35 años'] = unified_total['30 - 35 años'] + 1
                elif integrante.age() >= 35 and integrante.age() < 40:
                    unified_total['35 - 40 años'] = unified_total['35 - 40 años'] + 1
                elif integrante.age() >= 40 and integrante.age() < 45:
                    unified_total['40 - 45 años'] = unified_total['40 - 45 años'] + 1
                elif integrante.age() >= 45 and integrante.age() < 50:
                    unified_total['45 - 50 años'] = unified_total['45 - 50 años'] + 1
                elif integrante.age() >= 50 and integrante.age() < 55:
                    unified_total['50 - 55 años'] = unified_total['50 - 55 años'] + 1
                elif integrante.age() >= 55 and integrante.age() < 60:
                    unified_total['55 - 60 años'] = unified_total['55 - 60 años'] + 1
                else:
                    unified_total['+60 años'] = unified_total['+60 años'] + 1


    all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))
    unified_ordered_total = OrderedDict(sorted(unified_total.items(), key=lambda t: t[0]))
    
    context = {'data': all_ordered_results,
               'titulo': 'Edad Padres',
               'unified_total': unified_ordered_total}
    return render(request, 'indicadores/ocupaciones.html', context)

def ocupaciones(request):
    all_results = {}
    oficios = Oficio.objects.all()
    for localidad_option in Familia.OPCIONES_LOCALIDAD:
        results_localidad = {}
        for oficio in oficios:
            results_localidad[oficio.nombre] = Integrante.objects.filter(oficio=oficio,
                                                                  rol='tutor',
                                                                  activo=True,
                                                                  familia__estudio__status__contains='aprobado',
                                                                  familia__localidad=localidad_option[0]).count()
            ordered_results = OrderedDict(sorted(results_localidad.items(), key=lambda t: t[0]))
        all_results[localidad_option[1]] = ordered_results
        all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))

    unified_total = {}
    for oficio in oficios:
        unified_total[oficio.nombre] = Integrante.objects.filter(familia__estudio__status__contains='aprobado',
                                                                 rol='tutor',
                                                                 oficio=oficio).count()

    unified_ordered_total = OrderedDict(sorted(unified_total.items(), key=lambda t: t[0]))
    context = {'data': all_ordered_results,
               'titulo': 'Ocupaciones',
               'unified_total': unified_ordered_total}
    return render(request, 'indicadores/ocupaciones.html', context)

def ingreso_mensual(request):
    unified_total = {}
    all_results = {}
    familias = Familia.objects.filter(estudio__status__contains='aprobado')
    for localidad in Familia.OPCIONES_LOCALIDAD:
        all_results[localidad[1]] = {'$0 - $1999': 0,
                                     '$2000 - $3999': 0,
                                     '$4000 - $5999': 0,
                                     '$6000 - $7999': 0,
                                     '$8000 - $9999': 0,
                                     '$10000 - $11999': 0,
                                     '$12000 - $13999': 0,
                                     '$14000 - $15999': 0,
                                     '$16000 - $17999': 0,
                                     '$18000 - $19999': 0,
                                     '+20000': 0}


    unified_total = {'$0 - $1999': 0,
                     '$2000 - $3999': 0,
                     '$4000 - $5999': 0,
                     '$6000 - $7999': 0,
                     '$8000 - $9999': 0,
                     '$10000 - $11999': 0,
                     '$12000 - $13999': 0,
                     '$14000 - $15999': 0,
                     '$16000 - $17999': 0,
                     '$18000 - $19999': 0,
                     '+20000': 0}
    

    for localidad in Familia.OPCIONES_LOCALIDAD:
        familias = Familia.objects.filter(estudio__status__contains='aprobado',
                                          localidad=localidad[0])
        for familia in familias:
            if unformatted_total_ingresos_familia(familia.pk) < 2000:
                all_results[localidad[1]]['$0 - $1999'] = all_results[localidad[1]]['$0 - $1999'] + 1
            elif unformatted_total_ingresos_familia(familia.pk) < 4000:
                all_results[localidad[1]]['$2000 - $3999'] = all_results[localidad[1]]['$2000 - $3999'] + 1
            elif unformatted_total_ingresos_familia(familia.pk) < 6000:
                all_results[localidad[1]]['$4000 - $5999'] = all_results[localidad[1]]['$4000 - $59999'] + 1
            elif unformatted_total_ingresos_familia(familia.pk) < 8000:
                all_results[localidad[1]]['$6000 - $7999'] = all_results[localidad[1]]['$6000 - $7999'] + 1
            elif unformatted_total_ingresos_familia(familia.pk) < 10000:
                all_results[localidad[1]]['$8000 - $9999'] = all_results[localidad[1]]['$8000 - $9999'] + 1
            elif unformatted_total_ingresos_familia(familia.pk) < 12000:
                all_results[localidad[1]]['$10000 - $11999'] = all_results[localidad[1]]['$10000 - $11999'] + 1
            elif unformatted_total_ingresos_familia(familia.pk) < 14000:
                all_results[localidad[1]]['$12000 - $139999'] = all_results[localidad[1]]['$12000 - $13999'] + 1
            elif unformatted_total_ingresos_familia(familia.pk) < 16000:
                all_results[localidad[1]]['$14000 - $15999'] = all_results[localidad[1]]['$14000 - $15999'] + 1
            elif unformatted_total_ingresos_familia(familia.pk) < 18000:
                all_results[localidad[1]]['$16000 - $17999'] = all_results[localidad[1]]['$16000 - $17999'] + 1
            elif unformatted_total_ingresos_familia(familia.pk) < 20000:
                all_results[localidad[1]]['$18000 - $19999'] = all_results[localidad[1]]['$18000 - $19999'] + 1
            else:
                all_results[localidad[1]]['+20000'] = all_results[localidad[1]]['+20000'] + 1

            all_results[localidad[1]] = OrderedDict(sorted(all_results[localidad[1]].items(), key=lambda t: t[0]))

    familias = Familia.objects.filter(estudio__status__contains='aprobado')

    for familia in familias:
        if unformatted_total_ingresos_familia(familia.pk) < 2000:
            unified_total['$0 - $1999'] = unified_total['$0 - $1999'] + 1
        elif unformatted_total_ingresos_familia(familia.pk) < 4000:
            unified_total['$2000 - $3999'] = unified_total['$2000 - $3999'] + 1
        elif unformatted_total_ingresos_familia(familia.pk) < 6000:
            unified_total['$4000 - $5999'] = unified_total['$4000 - $59999'] + 1
        elif unformatted_total_ingresos_familia(familia.pk) < 8000:
            unified_total['$6000 - $7999'] = unified_total['$6000 - $7999'] + 1
        elif unformatted_total_ingresos_familia(familia.pk) < 10000:
            unified_total['$8000 - $9999'] = unified_total['$8000 - $9999'] + 1
        elif unformatted_total_ingresos_familia(familia.pk) < 12000:
            unified_total['$10000 - $11999'] = unified_total['$10000 - $11999'] + 1
        elif unformatted_total_ingresos_familia(familia.pk) < 14000:
            unified_total['$12000 - $139999'] = unified_total['$12000 - $13999'] + 1
        elif unformatted_total_ingresos_familia(familia.pk) < 16000:
            unified_total['$14000 - $15999'] = unified_total['$14000 - $15999'] + 1
        elif unformatted_total_ingresos_familia(familia.pk) < 18000:
            unified_total['$16000 - $17999'] = unified_total['$16000 - $17999'] + 1
        elif unformatted_total_ingresos_familia(familia.pk) < 20000:
            unified_total['$18000 - $19999'] = unified_total['$18000 - $19999'] + 1
        else:
            unified_total['+20000'] = unified_total['+20000'] + 1


    all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))
    unified_ordered_total = OrderedDict(sorted(unified_total.items(), key=lambda t: t[0]))
    
    context = {'data': all_ordered_results,
               'titulo': 'Ingresos',
               'unified_total': unified_ordered_total}
    return render(request, 'indicadores/ocupaciones.html', context)

def localidad(request):
    all_results = {}
    for localidad in Familia.OPCIONES_LOCALIDAD:
        all_results[localidad[1]] = Familia.objects.filter(estudio__status__contains='aprobado',
                                                           localidad=localidad[0]).count()

    all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))
    context = {'data': all_ordered_results, 'titulo': 'Distribución Familias'}
    return render(request, 'indicadores/localidad.html', context)

def sacramentos(request):
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
               'titulo': 'Sacramentos',
               'unified_total': unified_ordered_total}
    return render(request, 'indicadores/estado_civil.html', context)

def becas(request):
    unified_total = {}
    all_results = {}
    familias = Familia.objects.filter(estudio__status__contains='aprobado')
    for localidad in Familia.OPCIONES_LOCALIDAD:
        all_results[localidad[1]] = {'0%': 0,
                                     '1% - 9%': 0,
                                     '9% - 19%': 0,
                                     '%20 - %29': 0,
                                     '%30 - %39': 0,
                                     '%40 - %49': 0,
                                     '%50 - %59': 0,
                                     '%60 - %69': 0,
                                     '%70 - %79': 0,
                                     '%80 - %89': 0,
                                     '%90 - %100': 0}


    unified_total = {'0%': 0,
                     '1% - 9%': 0,
                     '9% - 19%': 0,
                     '%20 - %29': 0,
                     '%30 - %39': 0,
                     '%40 - %49': 0,
                     '%50 - %59': 0,
                     '%60 - %69': 0,
                     '%70 - %79': 0,
                     '%80 - %89': 0,
                     '%90 - %100': 0}
    

    for localidad in Familia.OPCIONES_LOCALIDAD:
        familias = Familia.objects.filter(estudio__status__contains='aprobado',
                                          localidad=localidad[0])
        for familia in familias:
            integrantes = Integrante.objects.filter(familia=familia,
                                                    activo=True)

            for integrante in integrantes:
                if hasattr(integrante, 'alumno_integrante'):
                    if Beca.objects.filter(alumno=integrante.alumno_integrante).count():
                        scholarship = Beca.objects.filter(alumno=integrante.alumno_integrante).latest('fecha_de_asignacion')
                        if scholarship.number_percentage() == 0:
                            all_results[localidad[1]]['0%'] = all_results[localidad[1]]['0%'] + 1
                        elif scholarship.number_percentage() < 10:
                            all_results[localidad[1]]['1% - 9%'] = all_results[localidad[1]]['1% - 9%'] + 1
                        elif scholarship.number_percentage() < 20:
                            all_results[localidad[1]]['10% - 19%'] = all_results[localidad[1]]['10% - 19%'] + 1
                        elif scholarship.number_percentage() < 30:
                            all_results[localidad[1]]['%20 - %29'] = all_results[localidad[1]]['%20 - %29'] + 1
                        elif scholarship.number_percentage() < 40:
                            all_results[localidad[1]]['%30 - %39'] = all_results[localidad[1]]['%30 - %39'] + 1
                        elif scholarship.number_percentage() < 50:
                            all_results[localidad[1]]['%40 - %49'] = all_results[localidad[1]]['%40 - %49'] + 1
                        elif scholarship.number_percentage() < 60:
                            all_results[localidad[1]]['%50 - %59'] = all_results[localidad[1]]['%50 - %59'] + 1
                        elif scholarship.number_percentage() < 70:
                            all_results[localidad[1]]['%60 - %69'] = all_results[localidad[1]]['%60 - %69'] + 1
                        elif scholarship.number_percentage() < 80:
                            all_results[localidad[1]]['%70 - %79'] = all_results[localidad[1]]['%70 - %79'] + 1
                        elif scholarship.number_percentage() < 90:
                            all_results[localidad[1]]['%80 - %89'] = all_results[localidad[1]]['%80 - %89'] + 1
                        elif scholarship.number_percentage() < 101:
                            all_results[localidad[1]]['%90 - %100'] = all_results[localidad[1]]['%90 - %100'] + 1

        all_results[localidad[1]] = OrderedDict(sorted(all_results[localidad[1]].items(), key=lambda t: t[0]))

    familias = Familia.objects.filter(estudio__status__contains='aprobado')

    for familia in familias:
        integrantes = Integrante.objects.filter(familia=familia,
                                                activo=True)

        for integrante in integrantes:
            if hasattr(integrante, 'alumno_integrante'):
                if Beca.objects.filter(alumno=integrante.alumno_integrante).count():
                    scholarship = Beca.objects.filter(alumno=integrante.alumno_integrante).latest('fecha_de_asignacion')
                    if scholarship.number_percentage() == 0:
                        unified_total['0%'] = unified_total['0%'] + 1
                    elif scholarship.number_percentage() < 10:
                        unified_total['1% - 9%'] = unified_total['1% - 9%'] + 1
                    elif scholarship.number_percentage() < 20:
                        unified_total['10% - 19%'] = unified_total['10% - 19%'] + 1
                    elif scholarship.number_percentage() < 30:
                        unified_total['%20 - %29'] = unified_total['%20 - %29'] + 1
                    elif scholarship.number_percentage() < 40:
                        unified_total['%30 - %39'] = unified_total['%30 - %39'] + 1
                    elif scholarship.number_percentage() < 50:
                        unified_total['%40 - %49'] = unified_total['%40 - %49'] + 1
                    elif scholarship.number_percentage() < 60:
                        unified_total['%50 - %59'] = unified_total['%50 - %59'] + 1
                    elif scholarship.number_percentage() < 70:
                        unified_total['%60 - %69'] = unified_total['%60 - %69'] + 1
                    elif scholarship.number_percentage() < 80:
                        unified_total['%70 - %79'] = unified_total['%70 - %79'] + 1
                    elif scholarship.number_percentage() < 90:
                        unified_total['%80 - %89'] = unified_total['%80 - %89'] + 1
                    elif scholarship.number_percentage() < 101:
                        unified_total['%90 - %100'] = unified_total['%90 - %100'] + 1

    all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))
    unified_ordered_total = OrderedDict(sorted(unified_total.items(), key=lambda t: t[0]))
    
    context = {'data': all_ordered_results,
               'titulo': 'Distribución Becas',
               'unified_total': unified_ordered_total}
    return render(request, 'indicadores/ocupaciones.html', context)
