import pickle

from estudios_socioeconomicos.models import Seccion, Subseccion, Pregunta, OpcionRespuesta


def parse(name):
    """ utility script to parse the study.
    """
    preguntas = {}
    while True:
        seccion = input('Ingrese el nombre de la seccion: ')
        if seccion == 'n':
            break
        if seccion not in preguntas:
            preguntas[seccion] = {}
        while True:
            subseccion = input('Ingrese el nombre de la subseccion dentro de %s: ' % seccion)
            if subseccion == 'n':
                break
            curr = 1
            if subseccion not in preguntas[seccion]:
                preguntas[seccion][subseccion] = []
            while True:
                p = input('Ingrese el nombre de la pregunta: ')
                if p == 'n':
                    break
                opt = input('Respuestas: ')
                opt = opt.split(',')
                rel_integrante = input('related? (y/n): ')
                preguntas[seccion][subseccion].append({
                    'texto': p,
                    'numero': curr,
                    'opciones': list(map(lambda x: x.strip(), opt)) if len(opt) > 1 else [],
                    'relacionado_a_integrante': rel_integrante == 'y'
                    })
                curr += 1
    print(preguntas)
    pickle.dump(preguntas, open(name, 'wb'))


def load_data(name='estudios_socioeconomicos.pkl'):
    """ Load the questions and sections for the study.

    To execute: import this function after running
    python manage.py shell
    and just call it.
    """
    preguntas = pickle.load(open(name, 'rb'))
    nums = {
        'Generales del Solicitante': 1,
        'Datos y Relación Familiar de Todos los Integrantes de la Vivienda': 2,
        'Situación Económica': 3,
        'Vivienda y Entorno Social': 4,
        'Investigación Laboral': 6,
        'Personalidad': 7,
        'Otros Aspectos': 8
    }
    for sec in preguntas.keys():
        seccion = Seccion.objects.create(nombre=sec, numero=nums[sec])
        for i, sub in enumerate(preguntas[sec].keys()):
            subseccion = Subseccion.objects.create(
                                seccion=seccion,
                                nombre=sub,
                                numero=i)
            for p in preguntas[sec][sub]:
                pregunta = Pregunta.objects.create(
                                subseccion=subseccion,
                                texto=p['texto'],
                                description=p['descripcion'],
                                orden=p['numero'],
                                )
                map(lambda o: OpcionRespuesta.objects.create(
                        pregunta=pregunta, texto=o), p['opciones'])
