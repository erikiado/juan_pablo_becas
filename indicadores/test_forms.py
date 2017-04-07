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
from familias.models import Familia, Integrante, Tutor
from perfiles_usuario.models import Capturista
from perfiles_usuario.utils import CAPTURISTA_GROUP
from .forms import IngresoForm


class TestFormsTransacciones(TestCase):
    """ Integration test suite for testing the forms in the app indicadores,
    that surround the creation and editing of the transaccion and ingreso model.

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
    familia2: Familia
        Used to make sure tutores don't leak when selecting one for an ingreso.
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

        self.familia2 = Familia.objects.create(numero_hijos_diferentes_papas=numero_hijos_inicial,
                                               estado_civil=estado_civil_inicial,
                                               localidad=localidad_inicial)

        self.estudio1 = Estudio.objects.create(capturista=self.capturista,
                                               familia=self.familia1)

        self.integrante1 = Integrante.objects.create(familia=self.familia1,
                                                     nombres='Rick',
                                                     apellidos='Astley',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.integrante2 = Integrante.objects.create(familia=self.familia2,
                                                     nombres='Bruce',
                                                     apellidos='Lee',
                                                     nivel_estudios='doctorado',
                                                     fecha_de_nacimiento='1996-02-26')

        self.tutor1 = Tutor.objects.create(integrante=self.integrante1,
                                           relacion='padre')

        self.tutor2 = Tutor.objects.create(integrante=self.integrante2,
                                           relacion='padre')

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


    def test_ingreso_queryset(self):
        """ Test that the select tutor option only includes tutores that are
        part of the family an ingreso is going to be added to.

        """
        form = IngresoForm(self.familia1.id)
        print(form)