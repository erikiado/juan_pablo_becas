import os
import time
import string
import random

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group
from django.contrib.staticfiles.templatetags.staticfiles import static
from splinter import Browser

from django.conf import settings
# from jp2_online.settings.base import BASE_DIR
from administracion.models import Escuela
from estudios_socioeconomicos.models import Estudio, Seccion, Pregunta, Respuesta
from estudios_socioeconomicos.models import Subseccion, OpcionRespuesta, Foto
from familias.models import Familia, Integrante, Alumno, Tutor
from indicadores.models import Periodo
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
            status=Estudio.BORRADOR)

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
        """ Initialize the browser and create a user, before running the tests.
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
        # self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
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
        # self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        self.assertEqual(Estudio.objects.count(), 2)
        # Check that the following texts are present in the dashboard
        self.assertTrue(self.browser.is_text_present('Mis estudios socioeconómicos'))
        self.assertTrue(self.browser.is_text_present('Agregar estudio'))
        # Check that the following text isn't present if exists any socio-economic study
        self.assertFalse(self.browser.is_text_present('No hay registro'))
        # Check that the following texts are present if exists any socio-economic study
        self.assertTrue(self.browser.is_text_present('Editar'))
        self.assertTrue(self.browser.is_text_present('Ver Retroalimentación'))


class TestViewsFotos(StaticLiveServerTestCase):
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
        self.familia1 = Familia.objects.create(numero_hijos_diferentes_papas=numero_hijos_inicial,
                                               estado_civil=estado_civil_inicial,
                                               localidad=localidad_inicial)

        self.estudio1 = Estudio.objects.create(capturista=self.capturista,
                                               familia=self.familia1)

        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()

    def tearDown(self):
        """ At the end of tests, close the browser.
        """
        self.browser.driver.close()
        self.browser.quit()

    def test_upload_photo(self):
        """ This test checks that the view 'captura:upload_photo', allows
        the upload of a new family photo, and the photo is displayed.
        """
        url = reverse('captura:list_photos',
                      kwargs={'id_estudio': self.estudio1.pk})
        static_url = static('test_files/cocina.jpeg')[1:]
        test_image = os.path.join(settings.BASE_DIR, static_url)
        self.browser.visit(self.live_server_url + url)
        self.browser.find_by_id('btn_modal_upload_photo').click()
        time.sleep(1)
        self.browser.fill('file_name', 'prueba')
        self.browser.fill('upload', test_image)
        self.browser.find_by_id('btn_send_create_photo').click()
        time.sleep(1)
        self.assertTrue(self.browser.is_text_present('prueba'))
        image = Foto.objects.filter(estudio=self.estudio1).last()
        self.assertEqual('prueba', image.file_name)
        image_url = image.upload.url[1:]
        os.remove(os.path.join(os.path.dirname(settings.BASE_DIR), image_url))

    def test_check_error_messages(self):
        url = reverse('captura:list_photos',
                      kwargs={'id_estudio': self.estudio1.pk})
        number_of_images_before = Foto.objects.filter(estudio=self.estudio1).count()
        static_url = static('test_files/fake.jpeg')[1:]
        test_image = os.path.join(settings.BASE_DIR, static_url)
        self.browser.visit(self.live_server_url + url)
        self.browser.find_by_id('btn_modal_upload_photo').click()
        time.sleep(1)
        self.browser.fill('file_name', 'prueba')
        self.browser.fill('upload', test_image)
        self.browser.find_by_id('btn_send_create_photo').click()
        time.sleep(1)
        self.assertTrue(self.browser.is_text_present('Upload a valid image'))
        number_of_images_after = Foto.objects.filter(estudio=self.estudio1).count()
        self.assertEqual(number_of_images_before, number_of_images_after)


class TestViewsCapturaEstudioCompleto(StaticLiveServerTestCase):
    """
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

        self.periodicidad1 = Periodo.objects.create(periodicidad='Semanal',
                                                    factor='4',
                                                    multiplica=True)

        self.escuela = Escuela.objects.create(nombre='Juan Pablo')

        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()

    def tearDown(self):
        self.browser.driver.close()
        self.browser.quit()

    def create_transactions(self, monto, observacion):
        """
        """
        self.browser.find_by_id('btn_modal_create_user').click()
        time.sleep(.3)
        self.browser.find_by_id('id_monto').fill(monto)
        self.browser.find_by_id('id_observacion').fill(observacion)
        self.browser.select('periodicidad', '1')
        self.browser.find_by_id('id_fecha').first.click()
        time.sleep(.2)
        self.browser.find_by_css('.ui-datepicker-today').first.click()
        self.browser.select('tipo', 'comprobable')
        self.browser.find_by_id('btn_send_create_user').click()

    def test_captura_complete_study(self):
        """
        """
        self.browser.visit(self.live_server_url + reverse('captura:estudios'))
        self.browser.find_by_id('create_estudio').click()
        time.sleep(.1)

        """ Create Family and Study
        """
        self.browser.find_by_id('id_numero_hijos_diferentes_papas').fill(2)
        self.browser.find_by_id('id_nombre_familiar').fill('Pérez')
        self.browser.select('estado_civil', 'casado_iglesia')
        self.browser.select('localidad', 'poblado_jurica')
        self.browser.find_by_id('submit_familia').click()

        TestViewsFamiliaLive.send_create_integrante_form(
            self,
            nombres='Juan',
            apellidos='Perez',
            telefono='4424567899',
            correo='abc@abc.com')
        self.browser.find_by_css('.swal2-confirm').first.click()

        TestViewsFamiliaLive.send_create_integrante_form(
            self,
            nombres='Hector',
            apellidos='Perez',
            telefono='222222222',
            correo='efg@abc.com')
        self.browser.find_by_css('.swal2-confirm').first.click()

        TestViewsFamiliaLive.send_create_integrante_form(
            self,
            nombres='Laura',
            apellidos='Perez',
            telefono='4424567899',
            correo='hij@abc.com')
        self.browser.find_by_css('.swal2-confirm').first.click()

        self.browser.find_by_id('next_ingresos_egresos').click()
        time.sleep(.1)

        self.create_transactions(1000, 'Ninguna')
        self.browser.find_by_css('.swal2-confirm').first.click()
        self.browser.find_by_id('next_fotos').click()

        static_url = static('test_files/cocina.jpeg')[1:]
        test_image = os.path.join(settings.BASE_DIR, static_url)
        self.browser.find_by_id('btn_modal_upload_photo').click()
        time.sleep(1)
        self.browser.fill('file_name', 'prueba')
        self.browser.fill('upload', test_image)
        self.browser.find_by_id('btn_send_create_photo').click()
        time.sleep(1)
        self.assertTrue(self.browser.is_text_present('prueba'))
        image = Foto.objects.filter(estudio=Estudio.objects.all().first()).last()
        self.assertEqual('prueba', image.file_name)
        image_url = image.upload.url[1:]
        os.remove(os.path.join(os.path.dirname(settings.BASE_DIR), image_url))

        self.browser.find_by_id('next_preguntas').click()  # Preguntas

        secciones = Seccion.objects.all().order_by('numero')
        random_texts = {}

        for seccion in secciones:

            subsecciones = Subseccion.objects.filter(seccion=seccion)
            preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)

            for pregunta in preguntas:

                respuestas = Respuesta.objects.filter(pregunta=pregunta)

                for respuesta in respuestas:
                    num_opciones = OpcionRespuesta.objects.filter(pregunta=pregunta).count()

                    if num_opciones > 0:

                        answer_input = self.browser.find_by_id(
                            'id_respuesta-' + str(respuesta.id)
                            + '-eleccion_' + str(num_opciones-1))

                        answer_input.check()
                    else:
                        new_text = ''.join(
                            random.choice(string.ascii_uppercase) for _ in range(12))

                        answer_input = self.browser.find_by_id(
                            'id_respuesta-' + str(respuesta.id) + '-respuesta').first
                        answer_input.fill(new_text)

                        random_texts[respuesta.id] = new_text

            self.browser.find_by_id('next_section_button').first.click()

        time.sleep(.1)
        self.browser.find_by_id('previous_cuestionario').first.click()

        secciones = Seccion.objects.all().order_by('-numero')

        for seccion in secciones:

            subsecciones = Subseccion.objects.filter(seccion=seccion)
            preguntas = Pregunta.objects.filter(subseccion__in=subsecciones)

            for pregunta in preguntas:
                respuestas = Respuesta.objects.filter(pregunta=pregunta)

                for respuesta in respuestas:
                    num_opciones = OpcionRespuesta.objects.filter(pregunta=pregunta).count()

                    if num_opciones > 0:
                        answer_input = self.browser.find_by_id(
                            'id_respuesta-' + str(respuesta.id)
                            + '-eleccion_' + str(num_opciones-1))

                        self.assertTrue(answer_input.checked)
                    else:
                        answer_input = self.browser.find_by_id(
                            'id_respuesta-' + str(respuesta.id) + '-respuesta').first
                        self.assertEqual(answer_input.value, random_texts[respuesta.id])

            self.browser.find_by_id('previous_section_button').first.click()

        # Now we JUMPT Between sections and add more info before we upload.

        self.browser.find_by_id('navigation_familia').click()
        hijos_bast = self.browser.find_by_id('id_numero_hijos_diferentes_papas').first.value
        self.assertEqual(hijos_bast, '2')

        self.browser.find_by_id('id_numero_hijos_diferentes_papas').fill(4)
        self.browser.find_by_id('submit_familia').click()
        time.sleep(.1)

        self.browser.find_by_id('previous_familia').click()
        hijos_bast = self.browser.find_by_id('id_numero_hijos_diferentes_papas').first.value
        self.assertEqual(hijos_bast, '4')

        self.browser.find_by_id('navigation_integrantes').click()

        self.assertTrue(self.browser.is_text_present('Hector'))
        self.assertTrue(self.browser.is_text_present('Laura'))
        self.assertTrue(self.browser.is_text_present('Juan'))

        # CREATE FATHER
        self.browser.find_by_id('btn_modal_create_integrante').click()
        time.sleep(0.3)
        self.browser.find_by_id('id_nombres').first.fill('don')
        self.browser.find_by_id('id_apellidos').first.fill('martines')
        self.browser.find_by_id('id_telefono').first.fill('442343234234')
        self.browser.find_by_id('id_correo').first.fill('abs@losabelosabe.com')
        self.browser.select('nivel_estudios', '6_grado')
        self.browser.find_by_id('id_fecha_de_nacimiento').first.click()
        time.sleep(.2)
        self.browser.find_by_css('.ui-datepicker-today').first.click()
        self.browser.select('rol', 'tutor')
        self.browser.select('relacion', 'padre')

        self.browser.find_by_id('btn_send_create_user').click()
        time.sleep(.1)
        self.browser.find_by_css('.swal2-confirm').first.click()
        # END CREATE FATHER

        # CREATE MOTHER
        self.browser.find_by_id('btn_modal_create_integrante').click()
        time.sleep(0.3)
        self.browser.find_by_id('id_nombres').first.fill('dona')
        self.browser.find_by_id('id_apellidos').first.fill('martines')
        self.browser.find_by_id('id_telefono').first.fill('442343234234')
        self.browser.find_by_id('id_correo').first.fill('absb@losabelosabe.com')
        self.browser.select('nivel_estudios', '6_grado')
        self.browser.find_by_id('id_fecha_de_nacimiento').first.click()
        time.sleep(.2)
        self.browser.find_by_css('.ui-datepicker-today').first.click()
        self.browser.select('rol', 'tutor')
        self.browser.select('relacion', 'madre')
        self.browser.find_by_id('btn_send_create_user').click()
        time.sleep(.1)
        self.browser.find_by_css('.swal2-confirm').first.click()
        # END CREATE MOTHER

        # CREATE SON
        self.browser.find_by_id('btn_modal_create_integrante').click()
        time.sleep(0.3)
        self.browser.find_by_id('id_nombres').first.fill('junior')
        self.browser.find_by_id('id_apellidos').first.fill('martines')
        self.browser.find_by_id('id_telefono').first.fill('4423431234234')
        self.browser.find_by_id('id_correo').first.fill('abssb@losabelosabe.com')
        self.browser.select('nivel_estudios', '6_grado')
        self.browser.find_by_id('id_fecha_de_nacimiento').first.click()
        time.sleep(.2)
        self.browser.find_by_css('.ui-datepicker-today').first.click()
        self.browser.select('rol', 'alumno')
        self.browser.select('escuela', '1')
        self.browser.find_by_id('id_numero_sae').fill('123123')
        self.browser.find_by_id('btn_send_create_user').click()
        self.browser.find_by_css('.swal2-confirm').first.click()
        # END CREATE SON
        time.sleep(.1)

        self.assertTrue(self.browser.is_text_present('don'))
        self.assertTrue(self.browser.is_text_present('dona'))
        self.assertTrue(self.browser.is_text_present('junior'))

        self.browser.find_by_id('navigation_transacciones').click()
        time.sleep(.1)
        estudio = Estudio.objects.all().first()
        desired_url = self.live_server_url + reverse(
            'captura:list_transacciones',
            kwargs={'id_familia': estudio.familia.id})

        self.assertEqual(self.browser.url, desired_url)

        self.browser.find_by_id('navigation_fotos').click()
        desired_url = self.live_server_url + reverse(
            'captura:list_photos',
            kwargs={'id_estudio': estudio.id})

        self.assertEqual(self.browser.url, desired_url)

        self.browser.find_by_id('navigation_cuestionario').click()
        desired_url = self.live_server_url + reverse(
            'captura:contestar_estudio',
            kwargs={'id_estudio': estudio.id, 'numero_seccion': 1})

        self.assertEqual(self.browser.url, desired_url)

        self.browser.find_by_css('.fa-file-text').first.click()
        time.sleep(.1)

        self.assertTrue(self.browser.is_text_present('Editar'))
        self.browser.find_by_css('.glyphicon-pencil').first.click()
        time.sleep(.1)

        self.browser.find_by_id('navigation_subir').click()
        time.sleep(.1)

        self.browser.find_by_id('submit_estudio').click()
        time.sleep(.1)

        desired_url = self.live_server_url + reverse('captura:estudios')

        self.assertEqual(self.browser.url, desired_url)
        self.assertFalse(self.browser.is_text_present('Editar'))
        estudio = Estudio.objects.all().first()
        self.assertEqual(estudio.status, Estudio.REVISION)
