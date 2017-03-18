from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from estudios_socioeconomicos.models import Pregunta, Subseccion, Seccion
from perfiles_usuario.models import Capturista
from estudios_socioeconomicos.load import load_data

from .views import APIQuestionsInformation


class TestAPIStudyMetaInformationRetrieval(APITestCase):
    """ Test Case for the API endpoint that will list information
        about questions, sections and subsections for the offline
        application.
    """
    def setUp(self):
        """ Setup start values and load data from script
        """
        test_username = 'erikiano'
        test_password = 'vacalalo'

        self.user = User.objects.create_user(
            username=test_username,
            email='latelma@junipero.sas',
            password=test_password,
            first_name='telma',
            last_name='suapellido')

        self.capturista = Capturista.objects.create(user=self.user)
        self.capturista.save()

        load_data()

        self.test_url_name = 'captura:api_obtener_informacion_preguntas'

    def test_retrieval_study_meta_information(self):
        """ Test that an authenticated user can retrieve information
            through the API.
        """
        data = {'username': 'erikiano', 'password': 'vacalalo'}

        response = self.client.post(
            reverse('perfiles_usuario:obtain_auth_token'),
            data, format='json')
        token = response.data['token']
        factory = APIRequestFactory()

        view = APIQuestionsInformation.as_view()

        request = factory.get(reverse(self.test_url_name))
        force_authenticate(request, user=self.user, token=token)

        response = view(request)

        num_preguntas = 0
        num_subsecciones = 0
        num_secciones = 0

        for seccion in response.data:
            for subseccion in seccion['subsecciones']:
                for pregunta in subseccion['preguntas']:
                    num_preguntas += 1
                num_subsecciones += 1
            num_secciones += 1

        self.assertEqual(num_preguntas, Pregunta.objects.all().count())
        self.assertEqual(num_subsecciones, Subseccion.objects.all().count())
        self.assertEqual(num_secciones, Seccion.objects.all().count())
