import os

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status

from jp2_online.settings.base import MEDIA_ROOT
from administracion.models import Escuela
from estudios_socioeconomicos.models import Pregunta, Subseccion, Seccion, Estudio
from estudios_socioeconomicos.models import Respuesta, Foto, OpcionRespuesta
from estudios_socioeconomicos.load import load_data
from familias.models import Familia, Comentario, Integrante
from indicadores.models import Oficio
from perfiles_usuario.models import Capturista
from indicadores.models import Ingreso


from .views import APIQuestionsInformation, APIUploadRetrieveStudy
from .views import APIOficioInformation, APIEscuelaInformation
from .views import APIUploadRetrieveImages


class TestAPIStudyMetaInformationRetrieval(APITestCase):
    """ Test Case for the API endpoint that will list information
        about questions, sections and subsections for the offline
        application.
    """
    def setUp(self):
        """ Setup start values and load data from script
        """
        test_username = 'erikiano'
        test_password = 'vacalalo'

        self.user = User.objects.create_user(
            username=test_username,
            email='latelma@junipero.sas',
            password=test_password,
            first_name='telma',
            last_name='suapellido')

        self.capturista = Capturista.objects.create(user=self.user)
        self.capturista.save()
        self.escuela = Escuela.objects.create(nombre='Juan Pablo')

        self.oficio = Oficio.objects.create(nombre='Maistro')

        load_data()

        self.test_url_name = 'captura:api_obtener_informacion_preguntas'

    def authenticate_request(self, api_view):
        data = {'username': 'erikiano', 'password': 'vacalalo'}

        response = self.client.post(
            reverse('perfiles_usuario:obtain_auth_token'),
            data, format='json')
        token = response.data['token']
        factory = APIRequestFactory()

        view = api_view.as_view()

        request = factory.get(reverse(self.test_url_name))
        force_authenticate(request, user=self.user, token=token)

        return view(request)

    def test_retrieval_study_meta_information(self):
        """ Test that an authenticated user can retrieve information
            through the API.
        """
        response = self.authenticate_request(APIQuestionsInformation)

        num_preguntas = 0
        num_subsecciones = 0
        num_secciones = 0

        for seccion in response.data:
            for subseccion in seccion['subsecciones']:
                for pregunta in subseccion['preguntas']:
                    num_preguntas += 1
                num_subsecciones += 1
            num_secciones += 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(num_preguntas, Pregunta.objects.all().count())
        self.assertEqual(num_subsecciones, Subseccion.objects.all().count())
        self.assertEqual(num_secciones, Seccion.objects.all().count())

    def test_escuelas_retrieval(self):
        """ Test that an authenticated user can recieve information
            about escuelas through an API endpoint.
        """
        response = self.authenticate_request(APIEscuelaInformation)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Escuela.objects.all().count())
        self.assertEqual(response.data[0]['nombre'], 'San Juan Pablo II')

    def test_oficio_retrieval(self):
        """ Test that an authenticated user can recieve information
            about oficios through an API endpoint.
        """
        response = self.authenticate_request(APIOficioInformation)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Oficio.objects.all().count())
        self.assertEqual(response.data[0]['nombre'], 'Maistro')


class TestAPIUploadRetrieveStudy(APITestCase):
    """ Test case for API REST endpoint with CRUD
        operations on a Study.

        Currents Tests:

        Test Creating Study
        Test Updating Study

        Test Updating Family

        Test Remove Integrante
        Test Add Integrante
        Test Update Integrante

        Test Remove Comentario
        Test Add Comentario
        Test Update Comentario

        Test Add Respuesta
        Test Remove Respuesta

        Test Unauthorized Access Listing
        Test Unauthorized Access Study

        Test New Family Generate If Study ID Removed
        Test No Family present In Study
        Test Wrong Data For Family
        Test Wrong Data For Integrante
        Test Wrong Update Integrante

        TEST Add Transaction (No Ingreso)
        TEST Update Transaction (No Ingreso)
            Same as Delete

        TEST Add Transaction (Ingreso)
        TEST Update Transaction (Ingreso)
            Same as Delete

    """
    def setUp(self):
        """ Creates users for testing study.
            Sets that study data that will be used through
            the tests.
        """
        self.factory = APIRequestFactory()
        self.test_url_name = 'captura:estudio'

        test_username = 'erikiano'
        test_password = 'vacalalo'

        self.user = User.objects.create_user(
            username=test_username,
            email='latelma@junipero.sas',
            password=test_password,
            first_name='telma',
            last_name='suapellido')

        self.capturista = Capturista.objects.create(user=self.user)
        self.capturista.save()

        self.unauthorized_user = User.objects.create_user(
            username='elbukok',
            email='elbukok@junipero.sas',
            password=test_password,
            first_name='Charles',
            last_name='Bukowski')

        self.unauthorized_capturista = Capturista.objects.create(user=self.unauthorized_user)
        self.unauthorized_capturista.save()

        self.view = APIUploadRetrieveStudy.as_view({
                'get': 'list',
                'post': 'create',
                'put': 'update',
                })

        load_data()

        self.escuela = Escuela.objects.create(nombre='El ITESM')

        self.study_data = {
            'familia': {
                'numero_hijos_diferentes_papas': 10,
                'explicacion_solvencia': 'Trabajando Duro',
                'estado_civil': 'soltero',
                'localidad': 'poblado_jurica',
                'comentario_familia': [
                    {
                        'fecha': '2017-03-19T19:18:48.158466Z',
                        'texto': 'Trabajan bien'
                    },
                    {
                        'fecha': '2017-03-19T19:18:48.160690Z',
                        'texto': 'Necesitan la beca'
                    }
                ],
                'integrante_familia': [
                    {
                        'nombres': 'Lao',
                        'apellidos': 'Tse',
                        'telefono': '',
                        'correo': '',
                        'nivel_estudios': '5_grado',
                        'fecha_de_nacimiento': '2003-03-19',
                        'alumno_integrante': {
                            'activo': True,
                            'escuela': {
                                'id': self.escuela.id,
                                'nombre': self.escuela.nombre
                            }
                        },
                        'tutor_integrante': None
                    },
                    {
                        'nombres': 'Telma',
                        'apellidos': 'Ibarra',
                        'telefono': '',
                        'correo': '',
                        'nivel_estudios': 'universidad',
                        'fecha_de_nacimiento': '2017-03-19',
                        'alumno_integrante': None,
                        'tutor_integrante': {
                            'relacion': 'madre',
                            'tutor_ingresos': None
                        }
                    },
                    {
                        'nombres': 'Herman',
                        'apellidos': 'Hesse',
                        'telefono': '',
                        'correo': '',
                        'nivel_estudios': 'doctorado',
                        'fecha_de_nacimiento': '2017-03-19',
                        'alumno_integrante': None,
                        'tutor_integrante': {
                            'relacion': 'tutor',
                            'tutor_ingresos': [
                                {
                                    'fecha': '2017-12-12',
                                    'tipo': Ingreso.OPCION_NO_COMPROBABLE,
                                    'transaccion': {
                                        'activo': True,
                                        'monto': 12500,
                                        'periodicidad': {
                                            'periodicidad': 'Mensual',
                                            'factor': 2.1,
                                            'multiplica': True,
                                        },
                                        'observacion': 'sastres',
                                        'es_ingreso': True
                                    }
                                }
                            ]
                        }
                    }
                    ],
                'transacciones': [
                    {
                        'activo': True,
                        'monto': 500,
                        'periodicidad': {
                            'periodicidad': 'Mensual',
                            'factor': 2.1,
                            'multiplica': True,
                        },
                        'observacion': 'sastres',
                        'es_ingreso': False
                    }
                ]
                }, 'respuesta_estudio': [
                    {
                        'pregunta': Pregunta.objects.all()[0].id,
                        'eleccion': None,
                        'respuesta': ''
                    },
                    {
                        'pregunta': Pregunta.objects.all()[1].id,
                        'eleccion': None,
                        'respuesta': ''
                    }
                ], 'status': Estudio.BORRADOR
            }

        self.initial_studies = 0
        data = {'username': test_username, 'password': test_password}

        response = self.client.post(
            reverse('perfiles_usuario:obtain_auth_token'),
            data,
            format='json')

        self.token = response.data['token']

    def create_base_study(self):
        """ This function creates a new study using the REST API
            endpoint. Most cases will need to create a study to
            test editing certain information, this allows us to
            keep it DRY.

            Returns
            ----------
                Response
                    The response object with the data of the
                    newly created object.

            Notes
            ---------
            With this every function that calls this asserts a
            new study is being generated.
        """
        self.assertEqual(Estudio.objects.all().count(), self.initial_studies)
        url = reverse('{}-list'.format(self.test_url_name))
        request = self.factory.post(url, self.study_data)
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        # print(response.data)
        self.assertEqual(Estudio.objects.all().count(), self.initial_studies+1)
        self.initial_studies += 1
        return response

    def update_existing_study(self, data, pk):
        """ This function updates an existing study using the REST API
            endpoint. Most cases will need to update a study to
            test editing certain information, this allows us to
            keep it DRY.

            Parameters
            ----------
            data : dictionary
                Dictionary with study data to modify
            pk : int
                The id of the instance that will be modified.

        """
        url = reverse('{}-detail'.format(self.test_url_name), kwargs={'pk': pk})
        request = self.factory.put(url, data)
        force_authenticate(request, user=self.user, token=self.token)
        return self.view(request, pk)

    def test_upload_study(self):
        """ Test that a study can be uploaded using a REST endpoint
            and that the nested information is being saved to the
            database.
        """
        response = self.create_base_study()

        familia = Familia.objects.get(pk=response.data['familia']['id'])

        self.assertEqual(
            self.study_data['familia']['numero_hijos_diferentes_papas'],
            familia.numero_hijos_diferentes_papas)

        self.assertEqual(
            self.study_data['familia']['explicacion_solvencia'],
            familia.explicacion_solvencia)

        comentarios = Comentario.objects.filter(familia=familia)

        comentarios_request = self.study_data['familia']['comentario_familia']

        for coment_bd, coment_rq in zip(comentarios, comentarios_request):
            self.assertEqual(coment_bd.texto, coment_rq['texto'])

        integrantes = Integrante.objects.filter(familia=familia)

        for integrante in self.study_data['familia']['integrante_familia']:
            int_bd = integrantes.filter(nombres=integrante['nombres'])[0]
            self.assertEqual(int_bd.apellidos, integrante['apellidos'])

    def test_update_study(self):
        """ Tests that the information in existing study can be updated
            using a REST endpoint.
        """
        response = self.create_base_study()

        study_id = response.data['id']

        change_study = response.data
        change_study['familia']['numero_hijos_diferentes_papas'] = 1000

        response = self.update_existing_study(change_study, study_id)

        self.assertEqual(Estudio.objects.all().count(), self.initial_studies+1)
        self.assertEqual(response.data['familia']['numero_hijos_diferentes_papas'], 1000)

    def test_remove_integrante(self):
        """ Tests that an integrante can be removed from a study
            using a REST endpoint.
        """
        response = self.create_base_study()

        study_id = response.data['id']
        change_study = response.data
        change_study['familia']['integrante_familia'][0]['activo'] = False
        id_integrante = change_study['familia']['integrante_familia'][0]['id']

        response = self.update_existing_study(change_study, study_id)

        integrante = Integrante.objects.get(pk=id_integrante)
        self.assertEqual(integrante.activo, False)
        # self.assertEqual(len(response.data['familia']['integrante_familia']), 2)

    def test_add_integrante(self):
        """ Test that an integrante can be added to a study
            using a REST endpoint.
        """
        response = self.create_base_study()

        study_id = response.data['id']
        change_study = response.data

        integrantes_nuevos = [
            {
                'nombres': 'juan',
                'apellidos': 'rulfo',
                'telefono': '',
                'correo': '',
                'nivel_estudios': '4_grado',
                'fecha_de_nacimiento': '2002-03-19',
                'alumno_integrante': {
                    'activo': True,
                    'escuela': str(self.escuela.id)
                },
                'tutor_integrante': None
            },
            {
                'nombres': 'Conchita',
                'apellidos': 'Felix',
                'telefono': '',
                'correo': '',
                'nivel_estudios': 'doctorado',
                'fecha_de_nacimiento': '1950-03-19',
                'alumno_integrante': None,
                'tutor_integrante': {
                    'relacion': 'tutor',
                    'tutor_ingresos': None,
                }
            }
        ]

        for integrante_nuevo in integrantes_nuevos:
            change_study['familia']['integrante_familia'].append(integrante_nuevo)

        response = self.update_existing_study(change_study, study_id)

        self.assertEqual(len(response.data['familia']['integrante_familia']), 5)

    def test_update_integrante(self):
        """ Test updating the information of an integrante.
        """
        response = self.create_base_study()

        study_id = response.data['id']
        change_study = response.data

        integrantes = change_study['familia']['integrante_familia']
        current_num_integrantes = len(integrantes)
        change_name_id = integrantes[0]['id']
        integrantes[0]['nombres'] = 'Chaos Monkey'

        integrante_nuevo = {
            'nombres': 'Juan',
            'apellidos': 'Rulfo',
            'telefono': '',
            'correo': '',
            'nivel_estudios': 'doctorado',
            'fecha_de_nacimiento': '1930-03-19',
            'alumno_integrante': None,
            'tutor_integrante': {
                'relacion': 'tutor',
                'tutor_ingresos': None,
            }
        }

        change_study['familia']['integrante_familia'].append(integrante_nuevo)
        response = self.update_existing_study(change_study, study_id)

        integrantes = response.data['familia']['integrante_familia']
        mono_chaos = Integrante.objects.get(pk=change_name_id)

        self.assertEqual('Chaos Monkey', mono_chaos.nombres)
        self.assertEqual(len(integrantes), current_num_integrantes+1)

        for integrante in integrantes:
            if integrante['id'] == change_name_id:
                self.assertEqual('Chaos Monkey', integrante['nombres'])

    def test_remove_comentario(self):
        """ Test that a Comentario can be removed from a study
            using a REST endpoint.
        """
        response = self.create_base_study()

        study_id = response.data['id']
        change_study = response.data
        del change_study['familia']['comentario_familia'][0]

        response = self.update_existing_study(change_study, study_id)

        self.assertEqual(len(response.data['familia']['comentario_familia']), 1)

    def test_add_comentarios(self):
        response = self.create_base_study()

        study_id = response.data['id']
        change_study = response.data

        comment = {
            'fecha': '2017-03-19T19:18:48.158466Z',
            'texto': 'Memento Mori'}

        change_study['familia']['comentario_familia'].append(comment)

        response = self.update_existing_study(change_study, study_id)

        self.assertEqual(Comentario.objects.filter(texto='Memento Mori').count(), 1)

    def test_update_comentario(self):
        """ Tests that a comentario can be updated through a REST
            endpoint.
        """
        response = self.create_base_study()

        study_id = response.data['id']
        change_study = response.data
        change_study['familia']['comentario_familia'][0]['texto'] = 'Sastres el Desastres'

        response = self.update_existing_study(change_study, study_id)
        self.assertEqual(Comentario.objects.filter(texto='Sastres el Desastres').count(), 1)

    def test_add_respuesta(self):
        """ Tests that an answer can be added to a study using a REST
            endpoint.
        """
        self.assertEqual(Respuesta.objects.all().count(), 0)

        response = self.create_base_study()

        num_answers = Respuesta.objects.all().count()

        self.assertEqual(num_answers, len(response.data['respuesta_estudio']))

        change_study = response.data

        change_study['respuesta_estudio'].append({
                'pregunta': Pregunta.objects.all()[3].id,
                'eleccion': None,
                'respuesta': ''
            })

        study_id = response.data['id']

        response = self.update_existing_study(change_study, study_id)
        self.assertEqual(num_answers + 1, len(response.data['respuesta_estudio']))

    def test_remove_respuesta(self):
        """ Tests that an answer can be removed from a study using a
            REST endpoint.
        """
        response = self.create_base_study()

        num_answers = Respuesta.objects.all().count()
        study_id = response.data['id']
        change_study = response.data
        del change_study['respuesta_estudio']

        response = self.update_existing_study(change_study, study_id)

        self.assertEqual(num_answers - 1, len(response.data['respuesta_estudio']))

    def test_unauthorized_access_listing(self):
        """ Test that a user can not access studies from another user.
        """
        response = self.create_base_study()

        data = {'username': 'elbukok', 'password': 'vacalalo'}

        response = self.client.post(
            reverse('perfiles_usuario:obtain_auth_token'),
            data,
            format='json')

        request = self.factory.get(reverse('{}-list'.format(self.test_url_name)))
        force_authenticate(request, user=self.unauthorized_user, token=response.data['token'])
        response = self.view(request)

        self.assertEqual(response.data['detail'], 'Not found.')

    def test_unauthorized_access_study(self):
        """ Test that a user can not access a specific study from another user.
        """
        response = self.create_base_study()

        study_id = response.data['id']
        self.assertEqual(Estudio.objects.all().count(), self.initial_studies + 1)

        data = {'username': 'elbukok', 'password': 'vacalalo'}
        response = self.client.post(
            reverse('perfiles_usuario:obtain_auth_token'),
            data,
            format='json')

        token = response.data['token']

        url = reverse('{}-detail'.format(self.test_url_name), kwargs={'pk': study_id})
        request = self.factory.get(url)
        force_authenticate(request, user=self.unauthorized_user, token=token)
        response = self.view(request)

        self.assertEqual(response.data['detail'], 'Not found.')

    def test_new_study_generated_with_new_family(self):
        """ Test that if a study without and ID is passed to the API,
            but a family with an ID is passed, a new family is generated.
        """
        response = self.create_base_study()
        del response.data['id']

        url = reverse('{}-list'.format(self.test_url_name))
        request = self.factory.post(url, response.data)
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)

        self.assertEqual(Familia.objects.all().count(), self.initial_studies + 2)

    def test_no_family_present_study(self):
        """ Test that API return correct status code and feedback if no
            family is present.
        """
        del self.study_data['familia']

        url = reverse('{}-list'.format(self.test_url_name))
        request = self.factory.post(url, self.study_data)
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['familia'][0], 'This field is required.')

        self.assertEqual(Estudio.objects.all().count(), 0)

    def test_wrong_data_familia(self):
        """ Test API send correct feedback and status code if information
            is not sent correctly.
        """
        del self.study_data['familia']['integrante_familia'][0]['alumno_integrante']

        url = reverse('{}-list'.format(self.test_url_name))
        request = self.factory.post(url, self.study_data)
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Estudio.objects.all().count(), 0)

    def test_wrong_integrante_name(self):
        """ Test API send correct feedback and status code if information
            is not sent correctly.
        """
        del self.study_data['familia']['integrante_familia'][1]['tutor_integrante']['relacion']

        url = reverse('{}-list'.format(self.test_url_name))
        request = self.factory.post(url, self.study_data)
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Estudio.objects.all().count(), 0)

    def test_wrong_update_integrante(self):
        """ Test API send correct feedback and status code if information
            is not sent correctly.
        """
        response = self.create_base_study()

        del response.data['familia']['integrante_familia'][1]['tutor_integrante']['relacion']

        url = reverse('{}-list'.format(self.test_url_name))
        request = self.factory.post(url, response.data)
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Estudio.objects.all().count(), 1)

    def test_add_transaction(self):
        """ Tests that a transaction can be added to study.
        """
        response = self.create_base_study()
        initial_transactions = len(response.data['familia']['transacciones'])
        change_study = response.data
        study_id = response.data['id']

        new_transaccion = {
            'activo': True,
            'monto': 1000,
            'periodicidad': {
                'periodicidad': 'Semanal',
                'factor': 1.1,
                'multiplica': False,
            },
            'observacion': 'no lo sieastres',
            'es_ingreso': False
        }

        change_study['familia']['transacciones'].append(new_transaccion)
        response = self.update_existing_study(change_study, study_id)

        self.assertEqual(
            len(response.data['familia']['transacciones']),
            initial_transactions + 1)

    def test_update_transaction(self):
        """ Test that a transaction can be updated inside a study.
        """
        response = self.create_base_study()
        study_id = response.data['id']
        change_study = response.data
        change_study['familia']['transacciones'][0]['monto'] = 200
        change_study['familia']['transacciones'][0]['periodicidad']['factor'] = 1

        response = self.update_existing_study(change_study, study_id)

        transaccion = response.data['familia']['transacciones'][0]
        self.assertEqual((transaccion['monto']), '200.00')
        self.assertEqual(int(float(transaccion['periodicidad']['factor'])), 1)

    def test_add_transacion_ingreso(self):
        """ Test adding a transaction that has ingreso to an integrante.
        """
        response = self.create_base_study()
        study_id = response.data['id']
        change_study = response.data
        initial_transactions = len(response.data['familia']['transacciones'])

        ingreso = {
            'fecha': '2017-12-12',
            'tipo': Ingreso.OPCION_NO_COMPROBABLE,
            'transaccion': {
                'activo': True,
                'monto': 55000,
                'periodicidad': {
                    'periodicidad': 'Mensual',
                    'factor': 2.1,
                    'multiplica': True,
                },
                'observacion': 'sastres el desastres',
                'es_ingreso': True
            }
        }

        integrante = change_study['familia']['integrante_familia'][1]
        id_integrante = integrante['id']
        self.assertEqual(len(integrante['tutor_integrante']['tutor_ingresos']), 0)
        integrante['tutor_integrante']['tutor_ingresos'].append(ingreso)

        response = self.update_existing_study(change_study, study_id)

        for integrante in response.data['familia']['integrante_familia']:
            if integrante['id'] == id_integrante:
                ingreso = integrante['tutor_integrante']['tutor_ingresos'][0]
                self.assertEqual(int(float(ingreso['transaccion']['monto'])), 55000)
                self.assertEqual(ingreso['fecha'], '2017-12-12')

        self.assertEqual(
            len(response.data['familia']['transacciones']),
            initial_transactions + 1)

    def test_update_transaccion_ingreso(self):
        response = self.create_base_study()
        study_id = response.data['id']
        change_study = response.data
        id_integrante = -1

        for integrante in change_study['familia']['integrante_familia']:
            if integrante['tutor_integrante']:
                if integrante['tutor_integrante']['tutor_ingresos']:
                    ingresos = integrante['tutor_integrante']['tutor_ingresos'][0]
                    ingresos['fecha'] = '1917-10-17'
                    id_integrante = integrante['id']

        response = self.update_existing_study(change_study, study_id)

        for integrante in response.data['familia']['integrante_familia']:
            if integrante['id'] == id_integrante:
                ingresos = integrante['tutor_integrante']['tutor_ingresos'][0]
                self.assertEqual(ingresos['fecha'], '1917-10-17')

    def test_upload_images_for_estudio(self):
        """ Test that an image can be uploaded to a study
            through a REST endpoint.
        """
        request = self.create_base_study()
        id_study = request.data['id']

        image = SimpleUploadedFile('prueba.png', b'file_content')

        data = {
            'estudio': id_study,
            'file_name': 'imagen1',
            'upload': image
        }

        view = APIUploadRetrieveImages.as_view({
                'get': 'list',
                'post': 'create',
            })

        url = reverse('captura:imagenes-list', kwargs={'id_estudio': id_study})
        request = self.factory.post(url, data, format='multipart')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, id_study)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        file_name = os.path.basename(response.data['upload'])
        path = os.path.join(os.path.dirname(MEDIA_ROOT), 'media', file_name)
        file_exists = os.path.isfile(path)

        self.assertTrue(file_exists)

        image = Foto.objects.get(pk=response.data['id'])
        self.assertEqual(image.file_name, response.data['file_name'])

    def test_listing_images(self):
        """ Test images for a study can be queried through API endpoint
        """
        request = self.create_base_study()
        id_study = request.data['id']

        image = SimpleUploadedFile('prueba.png', b'file_content')

        data = {
            'estudio': Estudio.objects.get(pk=id_study),
            'file_name': 'imagen1',
            'upload': image
        }

        Foto.objects.create(**data)
        self.assertEqual(Foto.objects.all().count(), 1)

        view = APIUploadRetrieveImages.as_view({
                'get': 'list',
                'post': 'create',
            })

        url = reverse('captura:imagenes-list', kwargs={'id_estudio': id_study})
        request = self.factory.get(url)
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, id_study)
        self.assertEqual(len(response.data), 1)
        image = response.data[0]
        self.assertEqual(image['file_name'], data['file_name'])

    def test_uploading_uploading_non_authorized(self):
        """ Test a user can't upload file to a study that
            does not belong to him.
        """
        study_data = self.create_base_study().data
        id_study = study_data['id']

        data = {'username': 'elbukok', 'password': 'vacalalo'}

        response = self.client.post(
            reverse('perfiles_usuario:obtain_auth_token'),
            data,
            format='json')

        image = SimpleUploadedFile('prueba.png', b'file_content')

        data = {
            'estudio': id_study,
            'file_name': 'imagen1',
            'upload': image
        }

        user = User.objects.get(username='elbukok')
        token = response.data['token']

        view = APIUploadRetrieveImages.as_view({
                'get': 'list',
                'post': 'create',
            })

        url = reverse('captura:imagenes-list', kwargs={'id_estudio': id_study})
        request = self.factory.post(url, data, format='multipart')
        force_authenticate(request, user=user, token=token)
        response = view(request, id_study)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_two_studies_with_opcion(self):
        """ test answering two different studies filling all questions that
            have options.
        """
        study = self.create_base_study().data
        opciones = OpcionRespuesta.objects.all()
        preguntas_nuevas = []
        preguntas_respondidas = []

        for opcion in opciones:
            preguntas_nuevas.append({
                'pregunta': opcion.pregunta.id,
                'eleccion': opcion.id,
                'respuesta': ''})
            preguntas_respondidas.append(opcion.pregunta.id)

        preguntas_por_responder = Pregunta.objects.exclude(id__in=preguntas_respondidas)

        for pregunta in preguntas_por_responder:
            preguntas_nuevas.append({
                'pregunta': pregunta.id,
                'eleccion': None,
                'respuesta': 'sastreseldesastres'})

        study['respuesta_estudio'] = preguntas_nuevas
        response = self.update_existing_study(study, study['id'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['respuesta_estudio']), Respuesta.objects.all().count())

        new_study = self.create_base_study().data
        preguntas_nuevas = []

        for opcion in opciones:
            preguntas_nuevas.append({
                'pregunta': opcion.pregunta.id,
                'eleccion': opcion.id,
                'respuesta': ''})

        new_study['respuesta_estudio'] = preguntas_nuevas
        response = self.update_existing_study(new_study, new_study['id'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['respuesta_estudio']),
            OpcionRespuesta.objects.all().count())
