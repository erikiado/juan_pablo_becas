import os
import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.test import TestCase
from django.test import Client

from django.conf import settings
# from jp2_online.settings.base import BASE_DIR
from administracion.models import Escuela
from estudios_socioeconomicos.models import Estudio, Foto
from indicadores.models import Periodo, Transaccion, Ingreso
from familias.models import Familia, Integrante, Tutor
from perfiles_usuario.models import Capturista


class TestViewsTransacciones(TestCase):
    """ Test suite for testing the views in the app: captura.

    Test the urls for 'captura' that make up the CRUD of transactions

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
        self.tutor1 = Tutor.objects.create(integrante=self.integrante1,
                                           relacion='padre')

        self.periodicidad1 = Periodo.objects.create(periodicidad='Semanal',
                                                    factor='4',
                                                    multiplica=True)
        self.transaccion1 = Transaccion.objects.create(familia=self.familia1,
                                                       monto=30,
                                                       periodicidad=self.periodicidad1,
                                                       observacion='Cultivo',
                                                       es_ingreso=False)

        self.transaccion2 = Transaccion.objects.create(familia=self.familia1,
                                                       monto=30,
                                                       periodicidad=self.periodicidad1,
                                                       observacion='Cultivo',
                                                       es_ingreso=True)

        self.ingreso1 = Ingreso.objects.create(transaccion=self.transaccion2,
                                               fecha='2016-02-02',
                                               tipo='comprobable',
                                               tutor=self.tutor1)

        self.transaccion_constructor_dictionary = {'monto': 40,
                                                   'periodicidad': self.periodicidad1.id,
                                                   'observacion': 'Distribucion',
                                                   'es_ingreso': False,
                                                   'familia': self.familia1.id}
        self.ingreso_constructor_dictionary = {'fecha': '2016-02-02',
                                               'tipo': 'comprobable'}

        self.client.login(username=test_username, password=test_password)

    def test_create_egreso(self):
        """ Test that an egreso can be created if the correct information
        if provided to the create_transaccion url.
        """

        r = self.client.post(reverse('captura:create_transaccion',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.transaccion_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['msg'], 'Egreso guardado con éxito')
        self.assertEqual(r.status_code, 200)

    def test_create_egreso_with_comma(self):
        """ Test that validate that the amount of an egreso can be contains
        commas and if the other information is correctly provided it will to
        create successfuly the transaction.
        """
        self.transaccion_constructor_dictionary['monto'] = '2,500.00'
        r = self.client.post(reverse('captura:create_transaccion',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.transaccion_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['msg'], 'Egreso guardado con éxito')
        self.assertEqual(r.status_code, 200)

        transaccion = Transaccion.objects.filter(familia=self.familia1).last()
        self.assertEqual(transaccion.monto, 2500)

    def test_create_egreso_incomplete(self):
        """ Test that an egreso won't be created if required information is
        incomplete.

        """
        self.transaccion_constructor_dictionary['monto'] = ''
        r = self.client.post(reverse('captura:create_transaccion',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.transaccion_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['monto'][0]['message'],
                         'This field is required.')
        self.assertEqual(r.status_code, 400)

    def test_create_ingreso(self):
        """ Test that an ingreso can be created if we provide all the required information
        to the create_transaccion url. Checks for the confirmation message.

        """
        self.transaccion_constructor_dictionary['es_ingreso'] = True
        self.ingreso_constructor_dictionary.update(self.transaccion_constructor_dictionary)
        r = self.client.post(reverse('captura:create_transaccion',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.ingreso_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['msg'], 'Ingreso guardado con éxito')
        self.assertEqual(r.status_code, 200)

    def test_create_ingreso_with_comma(self):
        """ Test that validate that the amount of an ingreso can be contains
        commas and if the other information is correctly provided it will to
        create successfuly the transaction.
        """
        self.transaccion_constructor_dictionary['es_ingreso'] = True
        self.transaccion_constructor_dictionary['monto'] = '2,500.00'
        self.ingreso_constructor_dictionary.update(self.transaccion_constructor_dictionary)

        r = self.client.post(reverse('captura:create_transaccion',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.ingreso_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['msg'], 'Ingreso guardado con éxito')
        self.assertEqual(r.status_code, 200)

        transaccion = Transaccion.objects.filter(familia=self.familia1).last()
        self.assertEqual(transaccion.monto, 2500)

    def test_create_ingreso_incomplete(self):
        """ Test that an ingreso won't be created if the required information is
        incomplete. Checks that an error status is returned, as well as an error
        message.
        """
        self.transaccion_constructor_dictionary['es_ingreso'] = True
        self.ingreso_constructor_dictionary.update(self.transaccion_constructor_dictionary)
        self.ingreso_constructor_dictionary['fecha'] = ''
        r = self.client.post(reverse('captura:create_transaccion',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.ingreso_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['fecha'][0]['message'],
                         'This field is required.')
        self.assertEqual(r.status_code, 400)

    def test_update_egreso(self):
        """ Test that an egreso can be updated if it's id is passed in the form for
        creating a transaccion, as long of all the required information.

        Checks for the acutal change in the egreso, the confirmation message, and the
        success code.
        """
        self.transaccion_constructor_dictionary['id_transaccion'] = self.transaccion1.id
        r = self.client.post(reverse('captura:create_transaccion',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.transaccion_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['msg'], 'Egreso guardado con éxito')
        self.assertEqual(r.status_code, 200)
        transaccion = Transaccion.objects.get(pk=self.transaccion1.id)
        self.assertEqual('-$160.00 mensuales', str(transaccion))

    def test_update_egreso_incomplete(self):
        """ This tests that a form won't be updated in case the complete information
        is passed to the create transaccion view.

        Checks for the error message, as well as the error code.
        """
        self.transaccion_constructor_dictionary['id_transaccion'] = self.transaccion1.id
        self.transaccion_constructor_dictionary['monto'] = ''
        r = self.client.post(reverse('captura:create_transaccion',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.transaccion_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['monto'][0]['message'],
                         'This field is required.')
        self.assertEqual(r.status_code, 400)

    def test_update_ingreso(self):
        """ Check that an ingreso can be updated if the id of the transaccion is passed
        to the update_create_transaccion view.

        This checks for the success code and message.
        """
        self.transaccion_constructor_dictionary['id_transaccion'] = self.transaccion1.id
        self.transaccion_constructor_dictionary['es_ingreso'] = True
        self.ingreso_constructor_dictionary.update(self.transaccion_constructor_dictionary)
        r = self.client.post(reverse('captura:create_transaccion',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.ingreso_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['msg'], 'Ingreso guardado con éxito')
        self.assertEqual(r.status_code, 200)

    def test_update_ingreso_incomplete(self):
        """ Test that an ingrewo can't be updated if the required information is incomplete.

        Checks for the error code, as well as the error message.
        """
        self.transaccion_constructor_dictionary['es_ingreso'] = True
        self.ingreso_constructor_dictionary.update(self.transaccion_constructor_dictionary)
        self.ingreso_constructor_dictionary['fecha'] = ''
        r = self.client.post(reverse('captura:create_transaccion',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.ingreso_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['fecha'][0]['message'],
                         'This field is required.')
        self.assertEqual(r.status_code, 400)

    def test_delete_transaccion(self):
        """ Test that we get redirected after deleting the transaccion.
        """
        response = self.client.post(reverse('captura:delete_transaccion',
                                            kwargs={'id_transaccion': self.transaccion1.pk}),
                                    {'id_transaccion': self.transaccion1.pk})
        self.assertRedirects(response, reverse('captura:list_transacciones',
                                               kwargs={'id_familia': self.familia1.pk}))
        transaccion = Transaccion.objects.get(pk=self.transaccion1.pk)
        self.assertFalse(transaccion.activo)

    def test_delete_transaccion_bad_request(self):
        """ Test that the view that sends the form
        for rendering the modal returns 400 if the request is not ajax.
        """
        url = reverse('captura:form_delete_transaccion',
                      kwargs={'id_transaccion': self.transaccion1.pk})
        response = self.client.post(url)
        self.assertEqual(400, response.status_code)
        response = self.client.get(url)
        self.assertEqual(400, response.status_code)

    def test_get_modal_delete_transaccion(self):
        """ Test that the view that sends the form via ajax
        returns the form needed to delete a transaccion.
        """
        response = self.client.get(reverse('captura:form_delete_transaccion',
                                           kwargs={'id_transaccion': self.transaccion1.pk}),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertTrue(b'seguro que desea borrar la transacci' in response.content)


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
                                               localidad=localidad_inicial,
                                               nombre_familiar='Pérez')

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
                                                  'rol': 'ninguno',
                                                  'oficio': '1'}

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
                                     'localidad': 'salitre',
                                     'nombre_familiar': 'Pérez'})
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
                                         localidad=localidad_inicial,
                                         nombre_familiar='Pérez')

        Estudio.objects.create(
          capturista=self.capturista,
          familia=familia)

        response = self.client.post(reverse('captura:familia', kwargs={'id_familia': familia.id}),
                                    {'numero_hijos_diferentes_papas': numero_hijos_final,
                                     'estado_civil': estado_civil_final,
                                     'localidad': localidad_final,
                                     'nombre_familiar': 'Pérez'})
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
        self.integrante_constructor_dictionary['plantel'] = self.escuela.id
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
        self.integrante_constructor_dictionary['plantel'] = self.escuela.id
        r = self.client.post(reverse('captura:create_integrante',
                                     kwargs={'id_familia': self.familia1.id}),
                             data=self.integrante_constructor_dictionary,
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # ajax request
        content = json.loads(r.content.decode('utf-8'))
        self.assertEqual(content['__all__'][0]['message'],
                         'El estudiante necesita el número sae y el plantel')
        self.assertEqual(r.status_code, 400)

    def test_create_integrante_with_rol_alumno_incomplete2(self):
        """ Test that an alumno can't be created if we don't provide
        escuela (plantel).
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
                         'El estudiante necesita el número sae y el plantel')
        self.assertEqual(r.status_code, 400)

    def test_create_integrante_with_rol_alumno_incomplete3(self):
        """ Test that an alumno can't be created if we provide
        a relation.
        """
        self.integrante_constructor_dictionary['id_integrante'] = ''
        self.integrante_constructor_dictionary['rol'] = 'alumno'
        self.integrante_constructor_dictionary['numero_sae'] = '123'
        self.integrante_constructor_dictionary['relacion'] = 'padre'
        self.integrante_constructor_dictionary['plantel'] = self.escuela.id
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
                         'El tutor no tiene número sae ni plantel')
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

    def test_delete_integrante(self):
        """ Test that we get redirected after deleting the integrante.

        """
        response = self.client.post(reverse('captura:delete_integrante',
                                            kwargs={'id_integrante': self.integrante1.pk}),
                                    {'id_integrante': self.integrante1.pk})
        self.assertRedirects(response, reverse('captura:list_integrantes',
                                               kwargs={'id_familia': self.familia1.pk}))
        integrante = Integrante.objects.get(pk=self.integrante1.pk)
        self.assertFalse(integrante.activo)

    def test_delete_integrante_bad_request(self):
        """ Test that the view that sends the form
        for rendering the modal returns 404 if the request is not ajax.
        """
        url = reverse('captura:form_delete_integrante',
                      kwargs={'id_integrante': self.integrante1.pk})
        response = self.client.post(url)
        self.assertEqual(400, response.status_code)
        response = self.client.get(url)
        self.assertEqual(400, response.status_code)

    def test_get_modal_delete_integrante(self):
        """ Test that the view that sends the form via ajax
        returns the form we want.
        """
        response = self.client.get(reverse('captura:form_delete_integrante',
                                           kwargs={'id_integrante': self.integrante1.pk}),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertTrue(b'seguro que desea borrar al integrante' in response.content)

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


class TestViewsRecuperaEstudio(TestCase):
    """ Unit tests for the views related to
    recovering studies.

    """

    def setUp(self):
        """ Create studies for a capturista.

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
        self.client.login(username=test_username, password=test_password)

        self.capturista = Capturista.objects.create(user=elerik)

        self.familia1 = Familia.objects.create(numero_hijos_diferentes_papas=3,
                                               estado_civil='soltero',
                                               localidad='salitre')

        self.estudio1 = Estudio.objects.create(capturista=self.capturista,
                                               familia=self.familia1,
                                               status=Estudio.ELIMINADO_CAPTURISTA)

        self.familia2 = Familia.objects.create(numero_hijos_diferentes_papas=2,
                                               estado_civil='soltero',
                                               localidad='salitre')

        self.estudio2 = Estudio.objects.create(capturista=self.capturista,
                                               familia=self.familia2,
                                               status=Estudio.ELIMINADO_CAPTURISTA)

    def test_url_view_recover(self):
        """ Test that we can access the view for recovering studies.

        """
        response = self.client.get(reverse('captura:recover_studies'))
        self.assertEqual(response.status_code, 200)

    def test_template_view_recover(self):
        """ Test that the template being used is the expected.

        """
        response = self.client.get(reverse('captura:recover_studies'))
        self.assertTemplateUsed(response, 'captura/recuperar_estudios.html')

    def test_recover_study(self):
        """ Test that we get redirected after recovering a study.

        """
        response = self.client.post(reverse('captura:estudio_recover'),
                                    {'id_estudio': self.estudio1.pk})
        self.assertRedirects(response, reverse('captura:recover_studies'))
        estudio = Estudio.objects.get(pk=self.estudio1.pk)
        self.assertEqual(estudio.status, Estudio.BORRADOR)

    def test_modal_recover_bad_request(self):
        """ Test that the view that sends the form
        for rendering the modal returns 404 if the request is not ajax.
        """
        url = reverse('captura:estudio_recover_modal',
                      kwargs={'id_estudio': self.estudio1.pk})
        response = self.client.post(url)
        self.assertEqual(400, response.status_code)
        response = self.client.get(url)
        self.assertEqual(400, response.status_code)

    def test_get_modal_delete_integrante(self):
        """ Test that the view that sends the form via ajax
        returns the form we want.
        """
        response = self.client.get(reverse('captura:estudio_recover_modal',
                                           kwargs={'id_estudio': self.estudio1.pk}),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertTrue(b'seguro que desea recuperar el estudio?' in response.content)

    def test_estudio_recover_bad_request(self):
        """ This test checks that the view 'captura:estudio_recover'
        raises a HttpResponseBadRequest when accessed via a non POST method
        """
        url = reverse('captura:estudio_recover')
        response = self.client.get(url)
        self.assertEqual(400, response.status_code)


class TestViewsFotos(TestCase):
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

        self.client.login(username=test_username, password=test_password)

    def test_upload_photo(self):
        """ This test checks that the view 'captura:upload_photo', allows
        the upload of a new family photo.
        """
        url = reverse('captura:upload_photo',
                      kwargs={'id_estudio': self.estudio1.pk})
        test_image = settings.BASE_DIR + static('test_files/cocina.jpeg')
        with open(test_image, 'r+b') as testing:
            form = {'estudio': self.estudio1.pk,
                    'file_name': 'prueba',
                    'upload': testing}
            response = self.client.post(url, form)
            self.assertEqual(302, response.status_code)
            image = Foto.objects.filter(estudio=self.estudio1).last()
            self.assertEqual('prueba', image.file_name)
            image_url = image.upload.url[1:]
            os.remove(os.path.join(os.path.dirname(settings.BASE_DIR), image_url))

    def test_upload_photo_bad_request(self):
        """ This test checks that the view 'captura:upload_photo',
        raises a HttpResponseBadRequest when accessed via a non POST
        method
        """
        url = reverse('captura:upload_photo',
                      kwargs={'id_estudio': self.estudio1.pk})
        response = self.client.get(url)
        self.assertEqual(400, response.status_code)

    def test_delete_modal_photo(self):
        """ This test checks that the view 'captura:upload_photo', allows
        the upload of a new family photo.
        """
        url = reverse('captura:upload_photo',
                      kwargs={'id_estudio': self.estudio1.pk})
        test_image = settings.BASE_DIR + static('test_files/borrosa.jpeg')
        with open(test_image, 'r+b') as testing:
            form = {'estudio': self.estudio1.pk,
                    'file_name': 'prueba',
                    'upload': testing}
            response = self.client.post(url, form)
            self.assertEqual(302, response.status_code)
            image = Foto.objects.filter(estudio=self.estudio1).last()

            # Check that the object and file exist
            response = self.client.get(reverse('captura:form_delete_foto',
                                               kwargs={'id_foto': image.pk}),
                                       HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(200, response.status_code)
            self.assertTrue(b'seguro que desea borrar esta foto' in response.content)

            response = self.client.post(reverse('captura:delete_foto',
                                                kwargs={'id_foto': image.pk}),
                                        {'id_foto': image.pk})
            self.assertRedirects(response, reverse('captura:list_photos',
                                                   kwargs={'id_estudio': image.estudio.pk}))

    def test_upload_and_delete_photo(self):
        """ This test checks that the view 'captura:upload_photo', allows
        the upload of a new family photo.
        """
        url = reverse('captura:upload_photo',
                      kwargs={'id_estudio': self.estudio1.pk})
        test_image = settings.BASE_DIR + static('test_files/borrosa.jpeg')
        with open(test_image, 'r+b') as testing:
            form = {'estudio': self.estudio1.pk,
                    'file_name': 'prueba',
                    'upload': testing}
            response = self.client.post(url, form)
            self.assertEqual(302, response.status_code)
            image = Foto.objects.filter(estudio=self.estudio1).last()

            # Check that the object and file exist
            self.assertTrue(os.path.isfile(image.upload.path))
            self.assertTrue(Foto.objects.filter(pk=image.pk).exists())

            response = self.client.post(reverse('captura:delete_foto',
                                                kwargs={'id_foto': image.pk}),
                                        {'id_foto': image.pk})
            self.assertRedirects(response, reverse('captura:list_photos',
                                                   kwargs={'id_estudio': image.estudio.pk}))

            # Check that the object and file exist
            self.assertFalse(os.path.isfile(image.upload.path))
            self.assertFalse(Foto.objects.filter(pk=image.pk).exists())
