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
from familias.models import Familia, Integrante, Alumno, Tutor
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


class TestViewsFamiliaLive(StaticLiveServerTestCase):
    """ The purpose of this class is to suplement TestViewsFamilia, as some of the required tests
    cannot be ran via de django client.

    Attributes
    ----------
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    elerik : User
        User that will be used as a capturista in order to fill all everything
        related with familia.
    familia1 : Familia
        Used in tests that depend on creating an object related to a familia.
    estudio1 : Estudio
        Used in tests that depend on creating or editing an existent estudio.
    integrante1 : Integrante
        Used in tests that depend on creating an object related to an integrante.
    integrante2 : Integrante
        Used in tests that depend on editing an alumno object.
    alumno1 : Alumno
        Used in the tests that depend on creating or editing an object related to an alumno.
    tutor1: Tutor
        Used in the tests that depend on creating or editing an object related to a tutor.
    escuela : Used in tests that depend on creating an object related to an escuela
    capturista : Capturista
        Asociated with the User, as this object is required for permissions and
        creation.
    """

    def setUp(self):
        """ Creates all the initial necessary objects for the tests
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

        self.escuela = Escuela.objects.create(nombre='Juan Pablo')

        self.capturista = Capturista.objects.create(user=elerik)

        numero_hijos_inicial = 3
        estado_civil_inicial = 'soltero'
        localidad_inicial = 'salitre'
        self.familia1 = Familia.objects.create(
                                  numero_hijos_diferentes_papas=numero_hijos_inicial,
                                  estado_civil=estado_civil_inicial,
                                  localidad=localidad_inicial)

        self.estudio1 = Estudio.objects.create(capturista=self.capturista,
                                               familia=self.familia1)

        self.integrante1 = Integrante.objects.create(familia=self.familia1,
                                                     nombres='Alberto',
                                                     apellidos='Lopez',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.integrante2 = Integrante.objects.create(familia=self.familia1,
                                                     nombres='Pedro',
                                                     apellidos='Perez',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.alumno1 = Alumno.objects.create(integrante=self.integrante1,
                                             numero_sae='5876',
                                             escuela=self.escuela)

        self.tutor1 = Tutor.objects.create(integrante=self.integrante2,
                                           relacion='padre')
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()

    def tearDown(self):
        """ At the end of tests, close the browser.
        """
        self.browser.driver.close()
        self.browser.quit()

    def test_edit_integrantes(self):
        """ Test that we can edit multiple integrantes.

        """
        new_name = 'Alejandro'
        numero_sae = '666'
        url = self.live_server_url + reverse('captura:list_integrantes',
                                             kwargs={'id_familia': self.familia1.id})
        self.browser.visit(url)
        self.browser.find_by_css('.edit-integrante-link').first.click()
        time.sleep(.3)
        #  sin sae
        self.browser.find_by_css('#modal_edit_integrante #id_numero_sae').first.fill('')
        self.browser.find_by_css('#modal_edit_integrante #btn_send_create_user').first.click()
        self.assertTrue(
            self.browser.is_text_present('El estudiante necesita el número sae y la escuela'))
        self.browser.find_by_css('.swal2-confirm').first.click()
        #  con sae
        self.browser.find_by_css('#modal_edit_integrante #id_nombres').first.fill(new_name)
        self.browser.find_by_css('#modal_edit_integrante #id_numero_sae').first.fill(numero_sae)
        self.browser.find_by_css('#modal_edit_integrante #btn_send_create_user').first.click()
        self.assertTrue(self.browser.is_text_present('Integrante Editado'))
        self.browser.find_by_css('.swal2-confirm').first.click()
        integrante = Integrante.objects.get(pk=self.integrante1.pk)
        self.assertEqual(new_name, integrante.nombres)
        alumno = Alumno.objects.get(integrante=self.integrante1.pk)
        self.assertEqual(numero_sae, alumno.numero_sae)
        self.assertTrue(self.browser.is_text_present(new_name))

        # otro usuario
        new_name = 'Peter'
        new_relation = 'tutor'
        self.browser.find_by_css('.edit-integrante-link')[1].click()
        time.sleep(.3)
        self.assertTrue(self.browser.is_text_present('Relacion'))
        self.browser.find_by_css('#modal_edit_integrante #id_nombres').first.fill(new_name)
        search_xpath = '//DIV[@id="modal_edit_integrante"]\
                        //SELECT[@id="id_relacion"]\
                        //OPTION[@value="' + new_relation + '"]'
        self.browser.find_by_xpath(search_xpath).click()

        self.browser.find_by_css('#modal_edit_integrante #btn_send_create_user').first.click()
        self.assertTrue(self.browser.is_text_present('Integrante Editado'))
        self.browser.find_by_css('.swal2-confirm').first.click()
        integrante = Integrante.objects.get(pk=self.integrante2.pk)
        self.assertEqual(new_name, integrante.nombres)
        self.assertEqual(integrante.tutor_integrante.relacion, new_relation)
        self.assertTrue(self.browser.is_text_present(new_name))

    def send_create_integrante_form(self, nombres, apellidos, telefono, correo):
        """Function which fills the user creation form and tries to send it.

        """
        self.browser.find_by_id('btn_modal_create_integrante').click()
        time.sleep(0.3)
        self.browser.find_by_id('id_nombres').first.fill(nombres)
        self.browser.find_by_id('id_apellidos').first.fill(apellidos)
        self.browser.find_by_id('id_telefono').first.fill(telefono)
        self.browser.find_by_id('id_correo').first.fill(correo)
        self.browser.select('nivel_estudios', '1_grado')
        self.browser.find_by_id('id_fecha_de_nacimiento').first.click()
        time.sleep(.2)
        self.browser.find_by_css('.ui-datepicker-today').first.click()
        self.browser.find_by_id('btn_send_create_user').click()

    def test_create_integrantes(self):
        """ Create two integrantes, checking errors and that they appear on the table.

        """
        url = self.live_server_url + reverse('captura:list_integrantes',
                                             kwargs={'id_familia': self.familia1.id})
        self.browser.visit(url)
        self.send_create_integrante_form(nombres='Elver', apellidos='Ga', telefono='4424567899',
                                         correo='abc@abc.com')
        self.assertTrue(self.browser.is_text_present('Integrante Creado'))
        self.browser.find_by_css('.swal2-confirm').first.click()
        time.sleep(.2)
        self.assertTrue(self.browser.is_text_present('Elver'))

        self.send_create_integrante_form(nombres='Eugenio', apellidos='Ga', telefono='-1',
                                         correo='abc@abc.com')
        self.assertTrue(self.browser.is_text_present('El número de telefono'))
        self.browser.find_by_css('.swal2-confirm').first.click()
        self.browser.find_by_id('id_telefono').first.fill('123456789')
        self.browser.find_by_id('btn_send_create_user').click()
        self.assertTrue(self.browser.is_text_present('Integrante Creado'))
        self.browser.find_by_css('.swal2-confirm').first.click()
        time.sleep(.2)
        self.assertTrue(self.browser.is_text_present('Eugenio'))


class TestViewsTransaccionesLive(StaticLiveServerTestCase):
    """ The purpose of this class is to suplement TestViewsFamilia, as some of the required tests
    cannot be ran via de django client.

    Attributes
    ----------
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    elerik : User
        User that will be used as a capturista in order to fill all everything
        related with familia.
    familia1 : Familia
        Used in tests that depend on creating an object related to a familia.
    estudio1 : Estudio
        Used in tests that depend on creating or editing an existent estudio.
    integrante1 : Integrante
        Used in tests that depend on creating an object related to an integrante.
    integrante2 : Integrante
        Used in tests that depend on editing an alumno object.
    alumno1 : Alumno
        Used in the tests that depend on creating or editing an object related to an alumno.
    tutor1: Tutor
        Used in the tests that depend on creating or editing an object related to a tutor.
    escuela : Used in tests that depend on creating an object related to an escuela
    capturista : Capturista
        Asociated with the User, as this object is required for permissions and
        creation.
    """

    def setUp(self):
        """ Creates all the initial necessary objects for the tests
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

        self.escuela = Escuela.objects.create(nombre='Juan Pablo')

        self.capturista = Capturista.objects.create(user=elerik)

        numero_hijos_inicial = 3
        estado_civil_inicial = 'soltero'
        localidad_inicial = 'salitre'
        self.familia1 = Familia.objects.create(
                                  numero_hijos_diferentes_papas=numero_hijos_inicial,
                                  estado_civil=estado_civil_inicial,
                                  localidad=localidad_inicial)

        self.estudio1 = Estudio.objects.create(capturista=self.capturista,
                                               familia=self.familia1)

        self.integrante1 = Integrante.objects.create(familia=self.familia1,
                                                     nombres='Alberto',
                                                     apellidos='Lopez',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.integrante2 = Integrante.objects.create(familia=self.familia1,
                                                     nombres='Pedro',
                                                     apellidos='Perez',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.alumno1 = Alumno.objects.create(integrante=self.integrante1,
                                             numero_sae='5876',
                                             escuela=self.escuela)

        self.tutor1 = Tutor.objects.create(integrante=self.integrante2,
                                           relacion='padre')
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()

    def tearDown(self):
        """ At the end of tests, close the browser.
        """
        self.browser.driver.close()
        self.browser.quit()


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
