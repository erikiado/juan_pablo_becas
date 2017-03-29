from django.test import TestCase
from django.contrib.auth import get_user_model

from familias.models import Familia
from perfiles_usuario.models import Capturista
from estudios_socioeconomicos.models import Estudio
from .models import Retroalimentacion


class RetroalimentacionTestCase(TestCase):
    """ Suite to Test things related to the Retroalimentacion Model.

    Attributes:
    -----------
    user : User
        The user who's filling the comment.
    estudio : Estudio
        The study to which the retroalimentación is referring to.
    retroalimentacion : Retroalimentacion
        The actual retro that the user is filling.
    """

    def setUp(self):
        """ Setup attributes.

        """
        self.user = get_user_model().objects.create_user(
                                    username='some_user',
                                    email='temporary@gmail.com',
                                    password='some_pass')
        capturista = Capturista.objects.create(user=self.user)
        familia = Familia.objects.create(
                                numero_hijos_diferentes_papas=2,
                                explicacion_solvencia='aaa',
                                estado_civil='soltero',
                                localidad='otro')
        self.estudio = Estudio.objects.create(
                                capturista=capturista,
                                familia=familia,
                                status=Estudio.REVISION)
        self.retroalimentacion = Retroalimentacion(
                                estudio=self.estudio,
                                usuario=self.user,
                                descripcion='Escribiste el campo x mal.')

    def test_estudio_str(self):
        """ Test whether the __str__ method works as expected.

        """
        expected = 'some_user - {fecha}: Escribiste el campo x mal.'.format(
                                                fecha=str(self.retroalimentacion.fecha))
        self.assertEqual(str(self.retroalimentacion), expected)
