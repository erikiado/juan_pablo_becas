import pickle


def parse(name):
    preguntas = {}
    while True:
        seccion = input('Ingrese el nombre de la seccion: ')
        if seccion == 'n': break
        if seccion not in preguntas:
            preguntas[seccion] = {}
        while True:
            subseccion = input('Ingrese el nombre de la subseccion dentro de %s: ' % seccion)
            if subseccion == 'n': break
            curr = 1
            if subseccion not in preguntas[seccion]:
                preguntas[seccion][subseccion] = []
            while True:
                p = input('Ingrese el nombre de la pregunta: ')
                if p == 'n': break
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


def fix_description(name):
    preguntas = pickle.load(open(name, 'rb'))
    for sec in preguntas.keys():
        for sub in preguntas[sec].keys():
            for p in preguntas[sec][sub]:
                val = p.pop('description', '')
                p['descripcion'] = val.strip()
    pickle.dump(preguntas, open(name, 'wb'))

if __name__ == '__main__':
    fix_description('preguntas.pkl')