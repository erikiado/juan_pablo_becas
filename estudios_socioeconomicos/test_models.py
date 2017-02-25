from django.test import TestCase
from django.contrib.auth import get_user_model

from familias.models import Familia
from perfiles_usuario.models import Capturista
from .models import Estudio, Seccion, Pregunta, OpcionRespuesta, Respuesta


class FamiliaTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                                    username='some_user',
                                    email='temporary@gmail.com',
                                    password='some_pass')
        self.capturista = Capturista.objects.create(user=self.user)
        self.familia = Familia.objects.create(
                                explicacion_solvencia='aaa',
                                estado_civil='soltero',
                                localidad='otro')
        self.estudio = Estudio.objects.create(
                                capturista=self.capturista,
                                familia=self.familia,
                                status=Estudio.APROBADO)

    def test_estudio_str(self):
        self.assertEqual(str(self.estudio), str(self.familia))


class SeccionTestCase(TestCase):

    def setUp(self):
        self.seccion = Seccion.objects.create(
                                nombre='Situación Económica',
                                numero=1)

    def test_str(self):
        self.assertEqual(str(self.seccion), 'Sección Situación Económica número 1')


class PreguntaTestCase(TestCase):

    def setUp(self):
        self.seccion = Seccion.objects.create(
                                nombre='Situación Económica',
                                numero=1)
        self.pregunta = Pregunta.objects.create(
                                seccion=self.seccion,
                                texto='Medio de Transporte')

    def test_str(self):
        self.assertEqual(str(self.pregunta), 'Medio de Transporte')


class OpcionRespuestaTestCase(TestCase):

    def setUp(self):
        self.seccion = Seccion.objects.create(
                                nombre='Situación Económica',
                                numero=1)
        self.pregunta = Pregunta.objects.create(
                                seccion=self.seccion,
                                texto='Medio de Transporte')
        self.opcion_respuesta = OpcionRespuesta.objects.create(
                                pregunta=self.pregunta,
                                texto='Camión')

    def test_str(self):
        self.assertEqual(str(self.opcion_respuesta), 'Camión')


class RespuestaTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                                    username='some_user',
                                    email='temporary@gmail.com',
                                    password='some_pass')
        self.capturista = Capturista.objects.create(user=self.user)
        self.familia = Familia.objects.create(
                                explicacion_solvencia='aaa',
                                estado_civil='soltero',
                                localidad='otro')
        self.estudio = Estudio.objects.create(
                                capturista=self.capturista,
                                familia=self.familia,
                                status=Estudio.APROBADO)
        self.seccion = Seccion.objects.create(
                                nombre='Situación Económica',
                                numero=1)
        self.pregunta = Pregunta.objects.create(
                                seccion=self.seccion,
                                texto='Medio de Transporte')

    def test_str_respuesta(self):
        respuesta = Respuesta.objects.create(
                                estudio=self.estudio,
                                pregunta=self.pregunta,
                                respuesta='Autobus')
        self.assertEqual(str(respuesta), 'Autobus')

    def test_str_opcion_respuesta(self):
        opcion_respuesta_camion = OpcionRespuesta.objects.create(
                                pregunta=self.pregunta,
                                texto='Camión')
        opcion_respuesta_bicicleta = OpcionRespuesta.objects.create(
                                pregunta=self.pregunta,
                                texto='Bicicleta')
        respuesta = Respuesta.objects.create(
                                estudio=self.estudio,
                                pregunta=self.pregunta)
        respuesta.elecciones.add(opcion_respuesta_camion)
        respuesta.elecciones.add(opcion_respuesta_bicicleta)
        self.assertEqual(str(respuesta), 'Bicicleta, Camión')
