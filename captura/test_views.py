import time 

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from django.contrib.auth.models import User

from estudios_socioeconomicos.models import Estudio, Seccion, Pregunta, Respuesta, Subseccion
from familias.models import Familia
from perfiles_usuario.models import Capturista
from estudios_socioeconomicos.load import load_data

class TestViewsCapturaEstudio(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: capturista.

    Test the urls for 'capturista' which allow the user to fill out a study.

    Attributes
    ----------
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """
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
        self.assertEqual(Pregunta.objects.all().count(), 142)

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

        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()

    def tearDown(self):
        self.browser.quit()

    def test_displaying_question_and_answers(self):
        test_url_name = 'captura:contestar_estudio'
        secciones = Seccion.objects.all().order_by('numero')

        self.browser.visit(
            self.live_server_url + reverse(
                test_url_name, 
                kwargs={'id_estudio': self.estudio.id, 'numero_seccion': secciones[0].numero}))
        
        subsecciones = Subseccion.objects.filter(seccion=secciones[0])

        for subseccion in subsecciones:
            self.assertTrue(self.browser.is_text_present(subseccion.nombre))

        preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)

        for pregunta in preguntas:
            respuesta = Respuesta.objects.filter(pregunta=pregunta)[0]
            
            answer_input = self.browser.find_by_id('id_respuesta-' + str(respuesta.id) + '-respuesta')
            self.assertNotEqual(answer_input, [])
            self.assertTrue(self.browser.is_text_present(pregunta.texto))



    def test_incorrect_url_parameters(self):
        test_url_name = 'captura:contestar_estudio'
        secciones = Seccion.objects.all().order_by('numero')

        self.browser.visit(
            self.live_server_url + reverse(
                test_url_name, 
                kwargs={'id_estudio': 0, 'numero_seccion': secciones[0].numero}))

        self.assertTrue(self.browser.is_text_present("Not Found"))

    def test_adding_more_answers(self):
        test_url_name = 'captura:contestar_estudio'
        secciones = Seccion.objects.all().order_by('numero')
        subsecciones = Subseccion.objects.filter(seccion=secciones[0])
        preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)
        respuestas = Respuesta.objects.filter(pregunta__in=preguntas)

        self.browser.visit(
            self.live_server_url + reverse(
                test_url_name, 
                kwargs={'id_estudio': self.estudio.id, 'numero_seccion': secciones[0].numero}))

        number_answers = Respuesta.objects.all().count()
        self.browser.find_by_id('answer-for-' + str(preguntas[0].id)).first.click()
        time.sleep(1)
        self.assertEqual(number_answers + 1, Respuesta.objects.all().count())

        nueva_respuesta = Respuesta.objects.all()[number_answers]
        answer_input = self.browser.find_by_id('id_respuesta-' + str(nueva_respuesta.id) + '-respuesta')
        self.assertNotEqual(answer_input, [])


    def test_removing_ansers(self):
        test_url_name = 'captura:contestar_estudio'
        secciones = Seccion.objects.all().order_by('numero')
        subsecciones = Subseccion.objects.filter(seccion=secciones[0])
        preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)
        respuestas = Respuesta.objects.filter(pregunta__in=preguntas)

        self.browser.visit(
            self.live_server_url + reverse(
                test_url_name, 
                kwargs={'id_estudio': self.estudio.id, 'numero_seccion': secciones[0].numero}))

        self.browser.find_by_id('answer-for-' + str(preguntas[0].id)).first.click()
        number_answers = Respuesta.objects.all().count()

        self.browser.find_by_id('delete-for-' + str(respuestas[0].id)).first.click()
        self.assertNotEqual(number_answers, Respuesta.objects.all().count())

    def test_submitting_answers(self):
        test_url_name = 'captura:contestar_estudio'
        secciones = Seccion.objects.all().order_by('numero')
        subsecciones = Subseccion.objects.filter(seccion=secciones[0])
        preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)
        respuestas = Respuesta.objects.filter(pregunta__in=preguntas)

        self.browser.visit(
            self.live_server_url + reverse(
                test_url_name, 
                kwargs={'id_estudio': self.estudio.id, 'numero_seccion': secciones[0].numero}))

        for pregunta in preguntas:
            respuestas = Respuesta.objects.filter(pregunta=pregunta)
            
            for respuesta in respuestas:
                answer_input = self.browser.find_by_id('id_respuesta-' + str(respuesta.id) + '-respuesta').first
                answer_input.fill('sastres el desastres')

