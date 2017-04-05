import time
import string
import random
import json

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.test import Client
from splinter import Browser

from administracion.models import Escuela
from estudios_socioeconomicos.models import Estudio, Seccion, Pregunta, Respuesta
from estudios_socioeconomicos.models import Subseccion, OpcionRespuesta
from familias.models import Familia, Integrante
from perfiles_usuario.models import Capturista
from estudios_socioeconomicos.load import load_data
from perfiles_usuario.utils import CAPTURISTA_GROUP


class TestViewsCapturaEstudio(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: capturista.

    Test the urls for 'capturista' which allow the user to fill out a study.

    Attributes
    ----------
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """ Initialize the browser, create a user, a family and a study.
            Perform login.
        """
        self.browser = Browser('chrome')
        test_username = 'erikiano'
        test_password = 'vacalalo'

        elerik = User.objects.create_user(
            username=test_username,
            email='latelma@junipero.sas',
            password=test_password,
            first_name='telma',
            last_name='suapellido')

        self.capturista = Capturista.objects.create(user=elerik)
        self.capturista.save()

        load_data()

        self.familia = Familia.objects.create(
            numero_hijos_diferentes_papas=3,
            explicacion_solvencia='narco',
            estado_civil='secreto',
            localidad='otro')

        self.estudio = Estudio.objects.create(
            capturista=self.capturista,
            familia=self.familia,
            status=Estudio.APROBADO)

        self.estudio.save()
        self.familia.save()

        self.assertEqual(Respuesta.objects.all().count(), Pregunta.objects.all().count())
        self.test_url_name = 'captura:contestar_estudio'
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()

    def tearDown(self):
        self.browser.driver.close()
        self.browser.quit()

    def test_displaying_question_and_answers(self):
        """ Tests that when a user loads the URL for filling a study,
            the html elements for all the questions in that section
            are rendered.
        """
        secciones = Seccion.objects.all().order_by('numero')

        self.browser.visit(
            self.live_server_url + reverse(
                self.test_url_name,
                kwargs={'id_estudio': self.estudio.id, 'numero_seccion': secciones[0].numero}))

        subsecciones = Subseccion.objects.filter(seccion=secciones[0])

        for subseccion in subsecciones:
            self.assertTrue(self.browser.is_text_present(subseccion.nombre))

        preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)

        for pregunta in preguntas:
            respuesta = Respuesta.objects.filter(pregunta=pregunta)[0]
            num_opciones = OpcionRespuesta.objects.filter(pregunta=pregunta).count()

            if num_opciones > 0:
                for i in range(num_opciones):
                    answer_input = self.browser.find_by_id(
                        'id_respuesta-' + str(respuesta.id) + '-eleccion_' + str(i))

                    self.assertNotEqual(answer_input, [])
                    self.assertTrue(self.browser.is_text_present(pregunta.texto))
            else:
                answer_input = self.browser.find_by_id(
                    'id_respuesta-' + str(respuesta.id) + '-respuesta')
                self.assertNotEqual(answer_input, [])
                self.assertTrue(self.browser.is_text_present(pregunta.texto))

    def test_incorrect_url_parameters(self):
        """ Test that a user can't query inexistent studies or sections.
        """
        secciones = Seccion.objects.all().order_by('numero')

        self.browser.visit(
            self.live_server_url + reverse(
                self.test_url_name,
                kwargs={'id_estudio': 0, 'numero_seccion': secciones[0].numero}))

        self.assertTrue(self.browser.is_text_present('Lo sentimos'))

    def test_adding_more_answers(self):
        """ Test that a user can dynamically add more questions to a
            study.
        """
        secciones = Seccion.objects.all().order_by('numero')
        subsecciones = Subseccion.objects.filter(seccion=secciones[0])
        preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)
        opciones = OpcionRespuesta.objects.filter(pregunta__in=preguntas)

        preguntas_texto = preguntas.exclude(pk__in=opciones.values_list('pregunta', flat=True))

        self.browser.visit(
            self.live_server_url + reverse(
                self.test_url_name,
                kwargs={'id_estudio': self.estudio.id, 'numero_seccion': secciones[0].numero}))

        number_answers = Respuesta.objects.all().count()

        self.browser.find_by_id('answer-for-' + str(preguntas_texto[0].id)).first.click()
        time.sleep(.1)
        self.assertEqual(number_answers + 1, Respuesta.objects.all().count())

        nueva_respuesta = Respuesta.objects.all().order_by('-id')[0]
        answer_input = self.browser.find_by_id(
            'id_respuesta-' + str(nueva_respuesta.id) + '-respuesta')
        self.assertNotEqual(answer_input, [])

    def test_removing_ansers(self):
        """ Test that a user can dynamically remove questions from a study.
        """
        secciones = Seccion.objects.all().order_by('numero')
        subsecciones = Subseccion.objects.filter(seccion=secciones[0])
        preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)
        opciones = OpcionRespuesta.objects.filter(pregunta__in=preguntas)

        preguntas_texto = preguntas.exclude(pk__in=opciones.values_list('pregunta', flat=True))

        self.browser.visit(
            self.live_server_url + reverse(
                self.test_url_name,
                kwargs={'id_estudio': self.estudio.id, 'numero_seccion': secciones[0].numero}))

        self.browser.find_by_id('answer-for-' + str(preguntas_texto[0].id)).first.click()
        number_answers = Respuesta.objects.all().count()

        self.browser.find_by_css('.delete-answer').first.click()
        self.assertNotEqual(number_answers, Respuesta.objects.all().count())

    def test_submitting_answers(self):
        """ Test that when a user submits his answers and moves on to the
        next section the answers are saved.
        """
        secciones = Seccion.objects.all().order_by('numero')
        subsecciones = Subseccion.objects.filter(seccion=secciones[0])
        preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)
        respuestas = Respuesta.objects.filter(pregunta__in=preguntas)

        self.browser.visit(
            self.live_server_url + reverse(
                self.test_url_name,
                kwargs={'id_estudio': self.estudio.id, 'numero_seccion': secciones[0].numero}))

        random_texts = {}

        for pregunta in preguntas:
            respuestas = Respuesta.objects.filter(pregunta=pregunta)

            for respuesta in respuestas:
                num_opciones = OpcionRespuesta.objects.filter(pregunta=pregunta).count()

                if num_opciones > 0:

                    answer_input = self.browser.find_by_id(
                        'id_respuesta-' + str(respuesta.id) + '-eleccion_' + str(num_opciones-1))

                    answer_input.check()
                else:
                    new_text = ''.join(random.choice(string.ascii_uppercase) for _ in range(12))
                    answer_input = self.browser.find_by_id(
                        'id_respuesta-' + str(respuesta.id) + '-respuesta').first
                    answer_input.fill(new_text)
                    random_texts[respuesta.id] = new_text

        self.browser.find_by_id('next_section_button').first.click()
        time.sleep(.1)
        self.browser.find_by_id('previous_section_button').first.click()
        time.sleep(.1)

        for pregunta in preguntas:
            respuestas = Respuesta.objects.filter(pregunta=pregunta)

            for respuesta in respuestas:
                num_opciones = OpcionRespuesta.objects.filter(pregunta=pregunta).count()

                if num_opciones > 0:
                    answer_input = self.browser.find_by_id(
                        'id_respuesta-' + str(respuesta.id) + '-eleccion_' + str(num_opciones-1))

                    self.assertTrue(answer_input.checked)
                else:
                    answer_input = self.browser.find_by_id(
                        'id_respuesta-' + str(respuesta.id) + '-respuesta').first
                    self.assertEqual(answer_input.value, random_texts[respuesta.id])

    def test_submitting_answer_with_dynamic_answers(self):
        """ Test that answers generated dynamically are being saved after submission.
        """
        secciones = Seccion.objects.all().order_by('numero')
        subsecciones = Subseccion.objects.filter(seccion=secciones[0])
        preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)
        opciones = OpcionRespuesta.objects.filter(pregunta__in=preguntas)

        preguntas_texto = preguntas.exclude(pk__in=opciones.values_list('pregunta', flat=True))

        self.browser.visit(
            self.live_server_url + reverse(
                self.test_url_name,
                kwargs={'id_estudio': self.estudio.id, 'numero_seccion': secciones[0].numero}))

        number_answers = Respuesta.objects.all().count()

        self.browser.find_by_id('answer-for-' + str(preguntas_texto[0].id)).first.click()
        time.sleep(.1)
        self.assertEqual(number_answers + 1, Respuesta.objects.all().count())

        nueva_respuesta = Respuesta.objects.all().order_by('-id')[0]
        new_text = ''.join(random.choice(string.ascii_uppercase) for _ in range(12))
        answer_input = self.browser.find_by_id(
            'id_respuesta-' + str(nueva_respuesta.id) + '-respuesta').first
        answer_input.fill(new_text)

        self.browser.find_by_id('next_section_button').first.click()
        time.sleep(.1)
        self.browser.find_by_id('previous_section_button').first.click()
        time.sleep(.1)

        answer_input = self.browser.find_by_id(
            'id_respuesta-' + str(nueva_respuesta.id) + '-respuesta').first

        self.assertEqual(answer_input.value, new_text)

    def test_passing_all_sections(self):
        """ Test going through all possible sections.
        """
        secciones = Seccion.objects.all().order_by('numero')

        self.browser.visit(
            self.live_server_url + reverse(
                self.test_url_name,
                kwargs={'id_estudio': self.estudio.id, 'numero_seccion': secciones[0].numero}))

        for seccion in secciones:
            time.sleep(.1)
            self.assertTrue(self.browser.is_text_present(seccion.nombre))
            self.browser.find_by_id('next_section_button').first.click()


class TestViewsFamilia(TestCase):
    """ Integration test suite for testing the views in the app captura,
    that surround the creation of editing of the familia model.

    Attributes
    ----------
    client : Client
        Django Client for the testing of all the views related to the creation
        and edition of a family.
    elerik : User
        User that will be used as a capturista in order to fill all everything
        related with familia.
    capturista : Capturista
        Asociated with the User, as this object is required for permissions and
        creation.
    escuela : Used in tests that depend on creating an object related to an escuela.
    familia1 : Familia
        Used in tests that depend on creating or editing an object related to a familia.
    estudio1 : Estudio
        Used in tests that depend on creating or editing an existent estudio.
    integrante1 : Integrante
        Used in tests that depend on creating or editing an object related to an integrante.
    integrante_contructor_dictionary : dictrionary
        Used in order to prevent repetitive code, when creating very similar integrantes
        in different tests.
    alumno_contructor_dictionary : dictionary
        Used in order to prevent repetitive code, when creating very similar alumnos in
        different tests.
    tutor_constructor_dictionary : dictionary
        Used in order to prevent repetivie code, when creating very similar tutores in
        different tests.
    """

    def setUp(self):
        """ Creates all the initial necessary objects for the tests
        """
        self.client = Client()
        test_username = 'erikiano'
        test_password = 'vacalalo'

        elerik = User.objects.create_user(
            username=test_username,
            email='latelma@junipero.sas',
            password=test_password,
            first_name='telma',
            last_name='suapellido')

        self.capturista = Capturista.objects.create(user=elerik)

        self.escuela = Escuela.objects.create(nombre='Juan Pablo')

        numero_hijos_inicial = 3
        estado_civil_inicial = 'soltero'
        localidad_inicial = 'salitre'
        self.familia1 = Familia.objects.create(numero_hijos_diferentes_papas=numero_hijos_inicial,
                                               estado_civil=estado_civil_inicial,
                                               localidad=localidad_inicial)

        self.estudio1 = Estudio.objects.create(capturista=self.capturista,
                                               familia=self.familia1)

        self.integrante1 = Integrante.objects.create(familia=self.familia1,
                                                     nombres='Rick',
                                                     apellidos='Astley',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.integrante_constructor_dictionary = {'familia': self.familia1.id,
                                                  'nombres': 'Arturo',
                                                  'apellidos': 'Herrera Rosas',
                                                  'telefono': '',
                                                  'correo': '',
                                                  'nivel_estudios': 'ninguno',
                                                  'fecha_de_nacimiento': '2017-03-22',
                                                  'rol': 'ninguno'}

        self.alumno_constructor_dictionary = {'integrante': self.integrante1.id,
                                              'numero_sae': 5876,
                                              'escuela': self.escuela.id}
        self.tutor_constructor_dictionary = {'integrante': self.integrante1.id,
                                             'relacion': 'madre'}

        self.client.login(username=test_username, password=test_password)

    def test_create_estudio(self):
        """ Tests the creation of a studio through the create_estudio page.
        """
        response = self.client.post(reverse('captura:create_estudio'),
                                    {'numero_hijos_diferentes_papas': 2,
                                     'estado_civil': 'soltero',
                                     'localidad': 'salitre'})
        id_familia = Familia.objects.latest('id').id
        self.assertRedirects(response, reverse('captura:list_integrantes',
                                               kwargs={'id_familia': id_familia}))

    def test_create_estudio_incomplete(self):
        """ Tests that the create estudio form fails gracefully when sending invalid data
        to the create_estudio view.
        """
        response = self.client.post(reverse('captura:create_estudio'),
                                    {'estado_civil': 'soltero',
                                     'localidad': 'salitre'})
        self.assertFormError(response,
                             'form',
                             'numero_hijos_diferentes_papas',
                             'This field is required.')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'captura/captura_base.html')

    def test_edit_familia(self):
        """ Tests that a familia can be edited through the edit_familia view.
        """
        numero_hijos_inicial = 3
        estado_civil_inicial = 'soltero'
        localidad_inicial = 'salitre'

        numero_hijos_final = 2
        estado_civil_final = 'viudo'
        localidad_final = 'nabo'

        familia = Familia.objects.create(numero_hijos_diferentes_papas=numero_hijos_inicial,
                                         estado_civil=estado_civil_inicial,
                                         localidad=localidad_inicial)
        response = self.client.post(reverse('captura:familia', kwargs={'id_familia': familia.id}),
                                    {'numero_hijos_diferentes_papas': numero_hijos_final,
                                     'estado_civil': estado_civil_final,
                                     'localidad': localidad_final})
        familia = Familia.objects.latest('id')
        self.assertEqual(familia.numero_hijos_diferentes_papas, numero_hijos_final)
        self.assertEqual(familia.estado_civil, estado_civil_final)
        self.assertEqual(familia.localidad, localidad_final)
        self.assertRedirects(response, reverse('captura:list_integrantes',
                                               kwargs={'id_familia': familia.id}))

    def test_edit_familia_incomplete(self):
        """ Tests that the familia edit view and form fail gracefully when provided with
        invalid data.
        """
        numero_hijos_final = 2
        estado_civil_final = 'viudo'

        response = self.client.post(reverse('captura:familia',
                                            kwargs={'id_familia': self.familia1.id}),
                                    {'numero_hijos_diferentes_papas': numero_hijos_final,
                                     'estado_civil': estado_civil_final})

        self.assertFormError(response, 'form', 'localidad', 'This field is required.')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'captura/captura_base.html')

    def test_create_integrante(self):
        """ Tests that an integrante can be created if the data
        is valid.
        """
        self.integrante_constructor_dictionary['id_integrante'] = ''
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # ajax request
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['msg'], 'Integrante Creado')
        self.assertEqual(r.status_code, 200)

    def test_create_integrante_incomplete(self):
        """ Tests that the form and view for create_integrante fail gracefully when provided
        with invalid data.
        """
        self.integrante_constructor_dictionary['id_integrante'] = ''
        self.integrante_constructor_dictionary['apellidos'] = ''
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # ajax request
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['apellidos'][0]['message'], 'This field is required.')

    def test_create_integrante_with_rol_alumno(self):
        """ Test that an alumno can be created if we provide
        the correct data: numero_sae and escuela.
        """

        self.integrante_constructor_dictionary['id_integrante'] = ''
        self.integrante_constructor_dictionary['rol'] = 'alumno'
        self.integrante_constructor_dictionary['numero_sae'] = '123'
        self.integrante_constructor_dictionary['escuela'] = self.escuela.id
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # ajax request
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['msg'], 'Integrante Creado')
        self.assertEqual(r.status_code, 200)

    def test_create_integrante_with_rol_alumno_incomplete(self):
        """ Test that an alumno can't be created if we don't provide
        numero_sae.
        """

        self.integrante_constructor_dictionary['id_integrante'] = ''
        self.integrante_constructor_dictionary['rol'] = 'alumno'
        self.integrante_constructor_dictionary['escuela'] = self.escuela.id
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # ajax request
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['__all__'][0]['message'],
                         'El estudiante necesita el número sae y la escuela')
        self.assertEqual(r.status_code, 400)

    def test_create_integrante_with_rol_alumno_incomplete2(self):
        """ Test that an alumno can't be created if we don't provide
        escuela.
        """
        self.integrante_constructor_dictionary['id_integrante'] = ''
        self.integrante_constructor_dictionary['rol'] = 'alumno'
        self.integrante_constructor_dictionary['numero_sae'] = '123'
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # ajax request
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['__all__'][0]['message'],
                         'El estudiante necesita el número sae y la escuela')
        self.assertEqual(r.status_code, 400)

    def test_create_integrante_with_rol_alumno_incomplete3(self):
        """ Test that an alumno can't be created if we provide
        a relation.
        """
        self.integrante_constructor_dictionary['id_integrante'] = ''
        self.integrante_constructor_dictionary['rol'] = 'alumno'
        self.integrante_constructor_dictionary['numero_sae'] = '123'
        self.integrante_constructor_dictionary['relacion'] = 'padre'
        self.integrante_constructor_dictionary['escuela'] = self.escuela.id
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # ajax request
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['__all__'][0]['message'],
                         'El estudiante no tiene relación')
        self.assertEqual(r.status_code, 400)

    def test_create_integrante_with_rol_tutor(self):
        """ Test that an integrante can be created if we provide
        the correct relation.
        """
        self.integrante_constructor_dictionary['id_integrante'] = ''
        self.integrante_constructor_dictionary['rol'] = 'tutor'
        self.integrante_constructor_dictionary['relacion'] = 'padre'
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['msg'], 'Integrante Creado')
        self.assertEqual(r.status_code, 200)

    def test_create_integrante_with_rol_tutor_incomplete(self):
        """ Test that an integrante can't be created if we don't provide
        the relation.
        """
        self.integrante_constructor_dictionary['id_integrante'] = ''
        self.integrante_constructor_dictionary['rol'] = 'tutor'
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['__all__'][0]['message'],
                         'El tutor necesita un tipo de relación')
        self.assertEqual(r.status_code, 400)

    def test_create_integrante_with_rol_tutor_incomplete2(self):
        """ Test that an integrante can't be created if we provide
        número sae.
        """
        self.integrante_constructor_dictionary['id_integrante'] = ''
        self.integrante_constructor_dictionary['rol'] = 'tutor'
        self.integrante_constructor_dictionary['numero_sae'] = '123'
        self.integrante_constructor_dictionary['relacion'] = 'padre'
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['__all__'][0]['message'],
                         'El tutor no tiene número sae ni escuela')
        self.assertEqual(r.status_code, 400)

    def test_edit_integrante(self):
        """ Test that an already existing integrante can be edited, through the
        edit_integrante view and form.
        """
        new_name = 'Never'
        self.integrante_constructor_dictionary['id_integrante'] = self.integrante1.pk
        self.integrante_constructor_dictionary['nombres'] = new_name
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['msg'], 'Integrante Editado')
        self.assertEqual(r.status_code, 200)
        integrante = Integrante.objects.get(id=self.integrante1.id)
        self.assertEqual(new_name, integrante.nombres)

    def test_estudio_delete(self):
        """ Test that submitting a form for delition of a estudio will be handeled correctly.
        """
        id_estudio = self.estudio1.id
        response = self.client.post(reverse('captura:estudio_delete'),
                                    {'id_estudio': id_estudio})
        self.assertEqual(302, response.status_code)

    def test_estudio_delete_modal_bad_requests(self):
        """ This test checks that the view 'captura:estudio_delete_modal'
        raises a HttpResponseBadRequest when accessed via a non AJAX method
        """
        url = reverse('captura:estudio_delete_modal',
                      kwargs={'id_estudio': self.estudio1.id})
        response = self.client.post(url, {'prueba': 'dato_cualquiera'})
        self.assertEqual(400, response.status_code)
        response = self.client.get(url)
        self.assertEqual(400, response.status_code)

    def test_estudio_delete_bad_request(self):
        """ This test checks that the view 'captura:estudio_delete'
        raises a HttpResponseBadRequest when accessed via a non POST method
        """
        url = reverse('captura:estudio_delete')
        response = self.client.get(url)
        self.assertEqual(400, response.status_code)


# class TestViewsFamiliaLive(StaticLiveServerTestCase):
#     """ The purpose of this class is to suplement TestViewsFamilia, as some of the required tests
#     cannot be ran via de django client.

#     Attributes
#     ----------
#     browser : Browser
#         Driver to navigate through websites and to run integration tests.
#     elerik : User
#         User that will be used as a capturista in order to fill all everything
#         related with familia.
#     familia1 : Familia
#         Used in tests that depend on creating an object related to a familia.
#     estudio1 : Estudio
#         Used in tests that depend on creating or editing an existent estudio.
#     integrante1 : Integrante
#         Used in tests that depend on creating an object related to an integrante.
#     integrante2 : Integrante
#         Used in tests that depend on editing an alumno object.
#     integrante3 : Integrante
#         Used in tests that depend on editing a tutor object.
#     alumno1 : Alumno
#         Used in the tests that depend on creating or editing an object related to an alumno.
#     tutor1: Tutor
#         Used in the tests that depend on creating or editing an object related to a tutor.
#     escuela : Used in tests that depend on creating an object related to an escuela
#     capturista : Capturista
#         Asociated with the User, as this object is required for permissions and
#         creation.
#     integrante_contructor_dictionary : dictrionary
#         Used in order to prevent repetitive code, when creating very similar integrantes
#         in different tests.
#     alumno_contructor_dictionary : dictionary
#         Used in order to prevent repetitive code, when creating very similar alumnos in
#         different tests.
#     tutor_constructor_dictionary : dictionary
#         Used in order to prevent repetivie code, when creating very similar tutores in
#         different tests.
#     """

#     def setUp(self):
#         """ Creates all the initial necessary objects for the tests
#         """
#         self.browser = Browser('chrome')
#         test_username = 'erikiano'
#         test_password = 'vacalalo'

#         elerik = User.objects.create_user(
#             username=test_username,
#             email='latelma@junipero.sas',
#             password=test_password,
#             first_name='telma',
#             last_name='suapellido')

#         self.escuela = Escuela.objects.create(nombre='Juan Pablo')

#         self.capturista = Capturista.objects.create(user=elerik)

#         numero_hijos_inicial = 3
#         estado_civil_inicial = 'soltero'
#         localidad_inicial = 'salitre'
# #         self.familia1 = Familia.objects.create(
#                                   numero_hijos_diferentes_papas=numero_hijos_inicial,
#                                   estado_civil=estado_civil_inicial,
#                                   localidad=localidad_inicial)

#         self.estudio1 = Estudio.objects.create(capturista=self.capturista,
#                                                familia=self.familia1)

#         self.integrante1 = Integrante.objects.create(familia=self.familia1,
#                                                      nombres='Rick',
#                                                      apellidos='Astley',
#                                                      nivel_estudios='doctorado',
#                                                      fecha_de_nacimiento='1996-02-26')

#         self.integrante2 = Integrante.objects.create(familia=self.familia1,
#                                                      nombres='Rick',
#                                                      apellidos='Astley',
#                                                      nivel_estudios='doctorado',
#                                                      fecha_de_nacimiento='1996-02-26')

#         self.integrante3 = Integrante.objects.create(familia=self.familia1,
#                                                      nombres='Rick',
#                                                      apellidos='Astley',
#                                                      nivel_estudios='doctorado',
#                                                      fecha_de_nacimiento='1996-02-26')

#         self.alumno1 = Alumno.objects.create(integrante=self.integrante2,
#                                              numero_sae='5876',
#                                              escuela=self.escuela)

#         self.tutor1 = Tutor.objects.create(integrante=self.integrante3,
#                                            relacion='padre')

#         self.integrante_constructor_dictionary = {'familia': self.familia1.id,
#                                                   'nombres': 'Arturo',
#                                                   'apellidos': 'Herrera Rosas',
#                                                   'telefono': '',
#                                                   'correo': '',
#                                                   'nivel_estudios': 'ninguno',
#                                                   'fecha_de_nacimiento': '2017-03-22',
#                                                   'Rol': 'ninguno'}

#         self.alumno_constructor_dictionary = {'integrante': self.integrante1.id,
#                                               'numero_sae': 5876,
#                                               'escuela': self.escuela.id}
#         self.tutor_constructor_dictionary = {'integrante': self.integrante1.id,
#                                              'relacion': 'madre'}

#         self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
#         self.browser.fill('username', test_username)
#         self.browser.fill('password', test_password)
#         self.browser.find_by_id('login-submit').click()

#     def tearDown(self):
#         """ At the end of tests, close the browser.
#         """
#         self.browser.driver.close()
#         self.browser.quit()

#     def test_edit_integrante_incomplete(self):
#         """ Test that the view and form for edit_integrante fail gracefully when provided
#         with invalid data.
#         """
#         nombres = ''
#         url = self.live_server_url + reverse('captura:integrante',
#                                              kwargs={'id_integrante': self.integrante1.id})
#         self.browser.visit(url)
#         self.browser.fill('nombres', nombres)
#         self.browser.find_by_id('update_integrante').first.click()
#         self.assertEqual(self.browser.url, url)

#     def test_edit_alumno(self):
#         """ Test that an already exisiting alumno can be edited, through the
#         edit_integrante view and form.
#         """
#         numero_sae = '42'

#         url = self.live_server_url + reverse('captura:integrante',
#                                              kwargs={'id_integrante': self.integrante2.id})
#         self.browser.visit(url)

#         self.browser.fill('numero_sae', numero_sae)

#         self.browser.find_by_id('update_integrante').first.click()
#         alumno = Alumno.objects.get(integrante=self.integrante2)
#         self.assertEqual(numero_sae, alumno.numero_sae)

#     def test_edit_alumno_incomplete(self):
#         """ Test that the view and form for edit_integrante fail gracefully when provided
#         with invalid data for an alumno.
#         """
#         numero_sae = ''
#         url = self.live_server_url + reverse('captura:integrante',
#                                              kwargs={'id_integrante': self.integrante2.id})
#         self.browser.visit(url)
#         self.browser.fill('numero_sae', numero_sae)
#         self.browser.find_by_id('update_integrante').first.click()
#         self.assertEqual(self.browser.url, url)

#     def test_edit_tutor(self):
#         """ Test that an already exisiting tutor can be edited, through the
#         edit_integrante view and form.
#         """
#         relacion = 'padre'

#         url = self.live_server_url + reverse('captura:integrante',
#                                              kwargs={'id_integrante': self.integrante3.id})
#         self.browser.visit(url)

#         self.browser.select('relacion', relacion)

#         self.browser.find_by_id('update_integrante').first.click()
#         tutor = Tutor.objects.get(integrante=self.integrante3)
#         self.assertEqual(relacion, tutor.relacion)

#     def test_edit_tutor_incomplete(self):
#         """ Test that the view and form for edit_integrante fail gracefully when provided
#         with invalid data for an alumno.
#         """
#         relacion = ''

#         url = self.live_server_url + reverse('captura:integrante',
#                                              kwargs={'id_integrante': self.integrante3.id})
#         self.browser.visit(url)
#         self.browser.select('relacion', relacion)
#         self.browser.find_by_id('update_integrante').first.click()
#         self.assertEqual(self.browser.url, url)

#     def test_create_alumno_from_existing_integrante(self):
#         """ Tests that modifying the Rol for an existing integrante, from 'ninguno' to
#         'alumno' redirects you to the create page for a new alumno and saves the object.
#         """
#         rol = 'alumno'
#         url = self.live_server_url + reverse('captura:integrante',
#                                              kwargs={'id_integrante': self.integrante1.id})
#         self.browser.visit(url)
#         self.browser.select('Rol', rol)
#         self.browser.find_by_id('update_integrante').first.click()
#         url = self.live_server_url + reverse('captura:create_alumno',
#                                              kwargs={'id_integrante': self.integrante1.id})
#         self.assertEqual(self.browser.url, url)

#         # Fill information
#         numero_sae = '9999'
#         self.browser.fill('numero_sae', numero_sae)
#         self.browser.select('escuela', self.escuela.id)
#         self.browser.find_by_id('create_alumno').first.click()
#         alumno = Alumno.objects.get(integrante=self.integrante1)
#         self.assertEqual(alumno.numero_sae, numero_sae)

#     def test_create_tutor_from_existing_integrante(self):
#         """ Tests that modifying the Rol for an existing integrante, from 'ninguno' to
#         'tutor' redirects you to the create page for a new tutor and saves the object.
#         """
#         rol = 'tutor'
#         url = self.live_server_url + reverse('captura:integrante',
#                                              kwargs={'id_integrante': self.integrante1.id})
#         self.browser.visit(url)
#         self.browser.select('Rol', rol)
#         self.browser.find_by_id('update_integrante').first.click()
#         url = self.live_server_url + reverse('captura:create_tutor',
#                                              kwargs={'id_integrante': self.integrante1.id})
#         self.assertEqual(self.browser.url, url)

#         # Fill information
#         relacion = 'padre'
#         self.browser.select('relacion', relacion)
#         self.browser.find_by_id('create_tutor').first.click()
#         tutor = Tutor.objects.get(integrante=self.integrante1)
#         self.assertEqual(tutor.relacion, relacion)

#     def test_delete_estudio(self):
#         """ Tests that the delete button works for the estudios
#         """
#         url = self.live_server_url + reverse('captura:estudios')
#         self.browser.visit(url)
#         self.browser.find_by_id('delete_estudio_' + str(self.estudio1.id)).first.click()
#         search_query = 'Esta seguro que desea borrar al usuario de correo: ' + str(self.estudio1)
#         self.assertFalse(self.browser.is_text_present(search_query))


class TestViewsAdministracion(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: captura.

    Test the urls for 'captura' which make up the capturista dashboard.
    A user is created in order to test they are displayed.

    Attributes
    ----------
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """Initialize the browser and create a user, before running the tests.
        """
        self.browser = Browser('chrome')
        test_username = 'estebes'
        test_password = 'junipero'
        estebes = User.objects.create_user(
            username=test_username, email='juan@example.com', password=test_password,
            first_name='Estebes', last_name='Thelmapellido')
        capturista = Group.objects.get_or_create(name=CAPTURISTA_GROUP)[0]
        capturista.user_set.add(estebes)
        capturista.save()

        self.capturista = Capturista.objects.create(user=estebes)
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()

    def tearDown(self):
        """At the end of tests, close the browser.
        """
        self.browser.driver.close()
        self.browser.quit()

    def test_capturista_dashboard_if_this_is_empty(self):
        """Test for url 'captura:estudios'.

        Visit the url of name 'captura:estudios' and check it loads the
        content of the captura dashboard panel.
        """
        test_url_name = 'captura:estudios'
        self.browser.visit(self.live_server_url + reverse(test_url_name))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        self.assertEqual(Estudio.objects.count(), 0)
        # Check that the folling texts are present in the dashboard
        self.assertTrue(self.browser.is_text_present('Mis estudios socioeconómicos'))
        self.assertTrue(self.browser.is_text_present('Agregar estudio'))
        # Check that the following text is present if not exists socio-economic studies
        self.assertTrue(self.browser.is_text_present(
                                'No hay registro de estudios socioeconómicos'))
        # Check that the following texts aren't present if not exists any socio-economic study
        self.assertFalse(self.browser.is_text_present('Ver retroalimentación'))
        self.assertFalse(self.browser.is_text_present('Editar'))

    def test_list_studies(self):
        """Test for url 'captura:estudios'.

        Creates two socio-economic studies (f1 and f2) the first as rejected
        (rechazado) and the second as pending (revision) and visit the url
        'captura:estudios' to check it loads both socio-economic studies created
        previously.
        """
        user = User.objects.get(username='estebes')
        user_id = user.id
        capturist = Capturista.objects.get(user=user_id)

        solvencia = 'No tienen dinero'
        estado = Familia.OPCION_ESTADO_SOLTERO
        estado2 = Familia.OPCION_ESTADO_CASADO_CIVIL
        localidad = Familia.OPCION_LOCALIDAD_JURICA
        localidad2 = Familia.OPCION_LOCALIDAD_CAMPANA

        f1 = Familia(numero_hijos_diferentes_papas=1, explicacion_solvencia=solvencia,
                     estado_civil=estado, localidad=localidad)
        f1.save()
        f2 = Familia(numero_hijos_diferentes_papas=2, explicacion_solvencia=solvencia,
                     estado_civil=estado2, localidad=localidad2)
        f2.save()

        e1 = Estudio(capturista_id=capturist.id, familia_id=f1.id,
                     status=Estudio.RECHAZADO)
        e1.save()
        e2 = Estudio(capturista_id=capturist.id, familia_id=f2.id,
                     status=Estudio.REVISION)
        e2.save()
        test_url_name = 'captura:estudios'
        self.browser.visit(self.live_server_url + reverse(test_url_name))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        self.assertEqual(Estudio.objects.count(), 2)
        # Check that the following texts are present in the dashboard
        self.assertTrue(self.browser.is_text_present('Mis estudios socioeconómicos'))
        self.assertTrue(self.browser.is_text_present('Agregar estudio'))
        # Check that the following text isn't present if exists any socio-economic study
        self.assertFalse(self.browser.is_text_present('No hay registro'))
        # Check that the following texts are present if exists any socio-economic study
        self.assertTrue(self.browser.is_text_present('Editar'))
        self.assertTrue(self.browser.is_text_present('Ver Retroalimentación'))
