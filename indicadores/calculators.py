from collections import OrderedDict
from familias.models import Familia, Alumno, Integrante

def estado_civil_counter():
    """ Prepare the dataset necessary to present
    a bar chart for the civil status of all the active
    families.

    """
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
    return all_ordered_results

def numero_de_alumnos():
    """ Prepare the dataset necessary to present
    a bar chart for the civil status of all the active
    families.

    """
    all_results = {}
    for localidad_option in Familia.OPCIONES_LOCALIDAD:
        results_localidad = {}
        for option in Integrante.OPCIONES_NIVEL_ESTUDIOS:
            if option[0] < '7' and option[1] == '_':
                results_localidad[option[1]] = Alumno.objects.filter(integrante__nivel_estudios__contains=option[0],
                                                           estudio__status__contains='aprobado',
                                                           localidad=localidad_option[0],
                                                           activo=True).count()
            ordered_results = OrderedDict(sorted(results_localidad.items(), key=lambda t: t[0]))
        all_results[localidad_option[1]] = ordered_results
        all_ordered_results = OrderedDict(sorted(all_results.items(), key=lambda t: t[0]))
    return all_ordered_results