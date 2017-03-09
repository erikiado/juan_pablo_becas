from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group

from splinter import Browser

from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP
from estudios_socioeconomicos.models import Estudio
from familias.models import Familia
from perfiles_usuario.models import Capturista


class StudiesDashboardAdministratorTest(StaticLiveServerTestCase):
    """ Integration test suite for testing the views in the app: administracion.
        Test if the socio-economic studies are present.

        Attributes
        ----------
        browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """ Initialize the browser and create a user admin,
            before running the tests.
        """
        self.browser = Browser('chrome')
        test_username = 'thelma'
        test_password = 'junipero'
        thelma = User.objects.create_user(
            username=test_username, email='juan@pablo.com', password=test_password,
            first_name='Thelma', last_name='Thelmapellido')
        administrators = Group.objects.get_or_create(name=ADMINISTRADOR_GROUP)[0]
        administrators.user_set.add(thelma)
        administrators.save()

        estebes = User.objects.create_user(
            username='estebes', email='juan@example.com', password='contrasena',
            first_name='Estebes', last_name='glez')
        capturista = Group.objects.get_or_create(name=CAPTURISTA_GROUP)[0]
        capturista.user_set.add(estebes)
        capturista.save()
        self.capturista = Capturista.objects.create(user=estebes)

        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', test_username)
        self.browser.fill('password', test_password)
        self.browser.find_by_id('login-submit').click()


    def tearDown(self):
        """ At the end of tests, close the browser.
        """
        self.browser.quit()

    def test_if_not_exist_any_studies_rejected(self):
        """ Test for url 'administracion:main_estudios' with the 'rechazado' argument.

            Visit the url of name 'administracion:main_estudios' and check if loads the
            empty page with the rigth message.
        """
        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name, args=['rechazado']))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
        self.assertEqual(Estudio.objects.count(), 0)
        # Check that the following text is present in the dashboard
        self.assertTrue(self.browser.is_text_present('No existen registros de este tipo de estudios para mostrar'))
        # Check that the following texts aren't present in the dashboard
        self.assertFalse(self.browser.is_text_present('Numero de Estudio Socioeconómico'))
        self.assertFalse(self.browser.is_text_present('Id Familia'))
        self.assertFalse(self.browser.is_text_present('Nombre del Capturista'))
        self.assertFalse(self.browser.is_text_present('Ver'))

    def test_studies_rejected_appears_for_user_admin(self):
        """ Test for url 'administracion:main_estudios' with the 'rechazado' argument.

            Visit the url of name 'administracion:main_estudios' and check it loads the
            content of the socio-economic studies rejected in the dashboard panel.
        """
        # Get the capturist and creates families
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
                     status=Estudio.RECHAZADO, numero_sae=2)
        e2.save()

        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name, args=['rechazado']))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
        self.assertEqual(Estudio.objects.count(), 2)
        # Check that the following texts aren't present in the dashboard
        self.assertFalse(self.browser.is_text_present('No existen registros de este tipo de estudios para mostrar'))
        self.assertFalse(self.browser.is_text_present('aprobado'))
        self.assertFalse(self.browser.is_text_present('borrador'))
        self.assertFalse(self.browser.is_text_present('Pendiente'))
        self.assertFalse(self.browser.is_text_present('eliminado'))
        # Check that the following texts are present in the dashboard
        self.assertTrue(self.browser.is_text_present('Numero de Estudio Socioeconómico'))
        self.assertTrue(self.browser.is_text_present('Id Familia'))
        self.assertTrue(self.browser.is_text_present('Nombre del Capturista'))
        self.assertTrue(self.browser.is_text_present('Ver'))
        self.assertTrue(self.browser.is_text_present('En revisión'))

    def test_if_not_exist_any_studies_as_pending(self):
        """ Test for url 'administracion:main_estudios' with the 'revision' parameter.

            Visit the url of name 'administracion:main_estudios' and check if loads the
            empty page with the rigth message.
        """
        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name, args=['revision']))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
        self.assertEqual(Estudio.objects.count(), 0)
        # Check that the following text is present in the dashboard
        self.assertTrue(self.browser.is_text_present('No existen registros de este tipo de estudios para mostrar'))
        # Check that the following texts aren't present in the dashboard
        self.assertFalse(self.browser.is_text_present('Numero de Estudio Socioeconómico'))
        self.assertFalse(self.browser.is_text_present('Id Familia'))
        self.assertFalse(self.browser.is_text_present('Nombre del Capturista'))
        self.assertFalse(self.browser.is_text_present('Ver'))

    def test_studies_as_pending_appears_for_admin(self):
        """ Test for url 'administracion:main_estudios' with the 'revision' parameter.

            Visit the url of name 'administracion:main_estudios' and check it loads the
            content of the socio-economic studies as pending in the dashboard panel.
        """
        # Get the capturist and creates families
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
                     status=Estudio.REVISION, numero_sae=1)
        e1.save()
        e2 = Estudio(capturista_id=capturist.id, familia_id=f2.id,
                     status=Estudio.REVISION, numero_sae=2)
        e2.save()

        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name, args=['revision']))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
        self.assertEqual(Estudio.objects.count(), 2)
        # Check that the following texts aren't present in the dashboard
        self.assertFalse(self.browser.is_text_present('No existen registros de este tipo de estudios para mostrar'))
        self.assertFalse(self.browser.is_text_present('aprobado'))
        self.assertFalse(self.browser.is_text_present('borrador'))
        self.assertFalse(self.browser.is_text_present('En revisión'))
        self.assertFalse(self.browser.is_text_present('eliminado'))
        # Check that the following texts aren present in the dashboard
        self.assertTrue(self.browser.is_text_present('Numero de Estudio Socioeconómico'))
        self.assertTrue(self.browser.is_text_present('Id Familia'))
        self.assertTrue(self.browser.is_text_present('Nombre del Capturista'))
        self.assertTrue(self.browser.is_text_present('Ver'))
        self.assertTrue(self.browser.is_text_present('Pendiente'))


    def test_if_not_exist_any_studies_approved(self):
        """ Test for url 'administracion:main_estudios' with the 'aprobado' parameter.

            Visit the url of name 'administracion:main_estudios' and check if loads the
            empty page with the rigth message.
        """
        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name, args=['aprobado']))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
        self.assertEqual(Estudio.objects.count(), 0)
        # Check that the following text is present in the dashboard
        self.assertTrue(self.browser.is_text_present('No existen registros de este tipo de estudios para mostrar'))
        # Check that the following texts aren't present in the dashboard
        self.assertFalse(self.browser.is_text_present('Numero de Estudio Socioeconómico'))
        self.assertFalse(self.browser.is_text_present('Id Familia'))
        self.assertFalse(self.browser.is_text_present('Nombre del Capturista'))
        self.assertFalse(self.browser.is_text_present('Ver'))

    def test_studies_approved_appears_for_admin(self):
        """ Test for url 'administracion:main_estudios' with the 'aprobado' parameter.

            Visit the url of name 'administracion:main_estudios' and check it loads the
            content of the socio-economic studies approved in the dashboard panel.
        """
        # Get the capturist and creates families
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
                     status=Estudio.APROBADO, numero_sae=1)
        e1.save()
        e2 = Estudio(capturista_id=capturist.id, familia_id=f2.id,
                     status=Estudio.APROBADO, numero_sae=2)
        e2.save()

        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name, args=['aprobado']))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
        self.assertEqual(Estudio.objects.count(), 2)
        # Check that the following texts aren't present in the dashboard
        self.assertFalse(self.browser.is_text_present('No existen registros de este tipo de estudios para mostrar'))
        self.assertFalse(self.browser.is_text_present('Pendiente'))
        self.assertFalse(self.browser.is_text_present('borrador'))
        self.assertFalse(self.browser.is_text_present('En revisión'))
        self.assertFalse(self.browser.is_text_present('eliminado'))
        # Check that the following texts are present in the dashboard
        self.assertTrue(self.browser.is_text_present('Numero de Estudio Socioeconómico'))
        self.assertTrue(self.browser.is_text_present('Id Familia'))
        self.assertTrue(self.browser.is_text_present('Nombre del Capturista'))
        self.assertTrue(self.browser.is_text_present('Ver'))
        self.assertTrue(self.browser.is_text_present('aprobado'))

    def test_if_not_exist_any_draft_studies(self):
        """ Test for url 'administracion:main_estudios' with the 'borrador' parameter.

            Visit the url of name 'administracion:main_estudios' and check if loads the
            empty page with the rigth message.
        """
        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name, args=['borrador']))

        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
        self.assertEqual(Estudio.objects.count(), 0)
        # Check that the following text is present in the dashboard
        self.assertTrue(self.browser.is_text_present('No existen registros de este tipo de estudios para mostrar'))
        # Check that the following texts aren't present in the dashboard
        self.assertFalse(self.browser.is_text_present('Numero de Estudio Socioeconómico'))
        self.assertFalse(self.browser.is_text_present('Id Familia'))
        self.assertFalse(self.browser.is_text_present('Nombre del Capturista'))
        self.assertFalse(self.browser.is_text_present('Ver'))

    def test_draft_studies_appears_for_admin(self):
        """ Test for url 'administracion:main_estudios' with the 'borrador' parameter.

            Visit the url of name 'administracion:main_estudios' and check it loads the
            content of the draft socio-economic studies in the dashboard panel.
        """
        # Get the capturist and creates families
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
                     status=Estudio.BORRADOR, numero_sae=1)
        e1.save()
        e2 = Estudio(capturista_id=capturist.id, familia_id=f2.id,
                     status=Estudio.BORRADOR, numero_sae=2)
        e2.save()

        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name, args=['borrador']))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
        self.assertEqual(Estudio.objects.count(), 2)
        # Check that the following texts aren't present in the dashboard
        self.assertFalse(self.browser.is_text_present('No existen registros de este tipo de estudios para mostrar'))
        self.assertFalse(self.browser.is_text_present('Pendiente'))
        self.assertFalse(self.browser.is_text_present('aprobado'))
        self.assertFalse(self.browser.is_text_present('En revisión'))
        self.assertFalse(self.browser.is_text_present('eliminado'))
        # Check that the following texts are present in the dashboard
        self.assertTrue(self.browser.is_text_present('Numero de Estudio Socioeconómico'))
        self.assertTrue(self.browser.is_text_present('Id Familia'))
        self.assertTrue(self.browser.is_text_present('Nombre del Capturista'))
        self.assertTrue(self.browser.is_text_present('Ver'))
        self.assertTrue(self.browser.is_text_present('borrador'))

    def test_if_not_exist_any_studies_deleted(self):
        """ Test for url 'administracion:main_estudios' with the 'eliminado' parameter.

            Visit the url of name 'administracion:main_estudios' and check if loads the
            empty page with the rigth message.
        """
        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name, args=['eliminado']))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
        self.assertEqual(Estudio.objects.count(), 0)
        # Check that the following text is present in the dashboard
        self.assertTrue(self.browser.is_text_present('No existen registros de este tipo de estudios para mostrar'))
        # Check that the following texts aren't present in the dashboard
        self.assertFalse(self.browser.is_text_present('Numero de Estudio Socioeconómico'))
        self.assertFalse(self.browser.is_text_present('Id Familia'))
        self.assertFalse(self.browser.is_text_present('Nombre del Capturista'))
        self.assertFalse(self.browser.is_text_present('Ver'))

    def test_studies_deleted_appears_for_admin(self):
        """ Test for url 'administracion:main_estudios' with the 'eliminado' parameter.

            Visit the url of name 'administracion:main_estudios' and check it loads the
            content of the socio-economic studies deleted in the dashboard panel.
        """
        # Get the capturist and creates families
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
                     status=Estudio.ELIMINADO, numero_sae=1)
        e1.save()
        e2 = Estudio(capturista_id=capturist.id, familia_id=f2.id,
                     status=Estudio.ELIMINADO, numero_sae=2)
        e2.save()

        test_url_name = 'administracion:main_estudios'

        self.browser.visit(self.live_server_url + reverse(test_url_name, args=['eliminado']))
        # Check for nav_bar partial
        self.assertTrue(self.browser.is_text_present('Instituto Juan Pablo'))
        # Check for side_nav partial
        self.assertTrue(self.browser.is_text_present('Estudios Socioeconómicos'))
        self.assertEqual(Estudio.objects.count(), 2)
        # Check that the following texts aren't present in the dashboard
        self.assertFalse(self.browser.is_text_present('No existen registros de este tipo de estudios para mostrar'))
        self.assertFalse(self.browser.is_text_present('Pendiente'))
        self.assertFalse(self.browser.is_text_present('aprobado'))
        self.assertFalse(self.browser.is_text_present('En revisión'))
        self.assertFalse(self.browser.is_text_present('borrador'))
        # Check that the following texts are present in the dashboard
        self.assertTrue(self.browser.is_text_present('Numero de Estudio Socioeconómico'))
        self.assertTrue(self.browser.is_text_present('Id Familia'))
        self.assertTrue(self.browser.is_text_present('Nombre del Capturista'))
        self.assertTrue(self.browser.is_text_present('Ver'))
        self.assertTrue(self.browser.is_text_present('eliminado'))
