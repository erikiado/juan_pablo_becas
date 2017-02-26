from django.test import TestCase
from django.contrib.auth import get_user_model

from familias.models import Familia
from perfiles_usuario.models import Capturista
from .models import Estudio, Seccion, Pregunta, OpcionRespuesta, Respuesta


class EstudioTestCase(TestCase):
    """ Suite to Test things related to the Estudio Model.

    Attributes:
    -----------
    user : User
        A mock user to use as capturista.
    capturista : Capturista
        A mock capturista to use as the one who filled the study.
    familia : Familia
        The family of which the study is about.
    estudio : Estudio
        The actual study.
    """

    def setUp(self):
        """ Setup attributes.

        """
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
        """ Test whether the __str__ method works as expected.

        TODO: fill __str__ method of familia.
        """
        expected = '{familia} status: {status}'.format(
                                            familia=str(self.familia),
                                            status=self.estudio.status)
        self.assertEqual(str(self.estudio), expected)


class SeccionTestCase(TestCase):
    """ Suite to test things related to the Seccion Model.

    Attributes:
    -----------
    seccion : Seccion
        The object for seccion we want to test.
    """

    def setUp(self):
        """ Setup the sección.

        """
        self.seccion = Seccion.objects.create(
                                nombre='Situación Económica',
                                numero=1)

    def test_str(self):
        """ Test whether the __str__ method works as expected.
        """
        self.assertEqual(str(self.seccion), 'Sección Situación Económica número 1')


class PreguntaTestCase(TestCase):
    """ Suite to test things related to the Pregunta model.

    Attributes:
    -----------
    seccion : Seccion
        The section to which the question belongs.
    pregunta : Pregunta
        The question itself.
    """

    def setUp(self):
        """ Setup attributes.
        """
        self.seccion = Seccion.objects.create(
                                nombre='Situación Económica',
                                numero=1)
        self.pregunta = Pregunta.objects.create(
                                seccion=self.seccion,
                                texto='Medio de Transporte')

    def test_str(self):
        """ Test whether __str__ method works as expected.
        """
        self.assertEqual(str(self.pregunta), 'Medio de Transporte')


class OpcionRespuestaTestCase(TestCase):
    """ Suite to test things related to the OpcionRespuesta model.

    Attributes:
    -----------
    seccion : Seccion
        The section to which the question belongs.
    pregunta : Pregunta
        The question itself.
    opcion_respuesta : OpcionRespuesta
        An option for answer to the question.
    """

    def setUp(self):
        """ Setup the attributes.
        """
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
        """ Test whether __str__ method works as expected.
        """
        self.assertEqual(str(self.opcion_respuesta), 'Camión')


class RespuestaTestCase(TestCase):
    """ Suite to test things related to the Respuesta model.

    Attributes:
    -----------
    user : User
        A mock user to use as capturista.
    capturista : Capturista
        A mock capturista to use as the one who filled the study.
    familia : Familia
        The family of which the study is about.
    estudio : Estudio
        The study to which the answer belongs.
    seccion : Seccion
        The section to which the question belongs.
    pregunta : Pregunta
        The question itself.
    opcion_respuesta : OpcionRespuesta
        An option for answer to the question.
    """

    def setUp(self):
        """ Setup the attributes.
        """
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

    def test_str_respuesta_empty(self):
        """ Test the __str__ method.

        We test the __str__ method when the answer has no text
        or choices whatsoever.
        """
        respuesta = Respuesta.objects.create(
                                estudio=self.estudio,
                                pregunta=self.pregunta)
        self.assertEqual(str(respuesta), 'No tiene respuesta.')

    def test_str_respuesta(self):
        """ Test the __str__ method.

        We test the __str__ method when the answer is a text inside the
        answer (filling the attribute respuesta).
        """
        respuesta = Respuesta.objects.create(
                                estudio=self.estudio,
                                pregunta=self.pregunta,
                                respuesta='Autobus')
        self.assertEqual(str(respuesta), 'Autobus')

    def test_str_opcion_respuesta(self):
        """ Test the __str__ method.

        We test the __str__ method when the answer are two choices of
        OpcionRespuesta.
        """
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
