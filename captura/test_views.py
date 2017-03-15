import time
import string
import random

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group
from splinter import Browser

from estudios_socioeconomicos.models import Estudio, Seccion, Pregunta, Respuesta
from estudios_socioeconomicos.models import Subseccion, OpcionRespuesta
from familias.models import Familia
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

        self.assertTrue(self.browser.is_text_present('Not Found'))

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
                     status=Estudio.RECHAZADO, numero_sae=1)
        e1.save()
        e2 = Estudio(capturista_id=capturist.id, familia_id=f2.id,
                     status=Estudio.REVISION, numero_sae=2)
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
        self.assertTrue(self.browser.is_text_present('Ver retroalimentación'))
