from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Capturista
from .utils import SERVICIOS_ESCOLARES_GROUP


class TokenCreationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='juliannieb', first_name='Julian',
            last_name='ElGandul', email='Julian69@gmail.com',
            password='vacalalonja')

        User.objects.create_user(
            username='erikiano', first_name='erik',
            last_name='yano', email='erikiano@gmail.com',
            password='vacalalo')

        self.servicios_group = Group.objects.get_or_create(name=SERVICIOS_ESCOLARES_GROUP)[0]
        self.user.groups.add(self.servicios_group)

        self.capturista = Capturista.objects.create(user=self.user)
        self.url = reverse('perfiles_usuario:obtain_auth_token')

    def test_return_authentication_token(self):
        """ Test that an existing user can authenticate through a rest endpoint.

            Test that a client can send a post request with a users credentials and
            the API will return the user Token for the client to use in further requests.
        """
        data = {'username': 'juliannieb', 'password': 'vacalalonja'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Token.objects.all()), 1)

    def test_incorrect_authentication_credentials(self):
        """ Test that an existing user can not authenticate with invalid credentials.

            Test that when a client tries to authenticate a user with invalid credentials
            he does not recieve a token ang get a 400 http response.
        """
        data = {'username': 'juliannieb', 'password': 'estanoesmicontrasena'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_group_authentication(self):
        """ Test only certain user groups can authenticate via API

            Test that other users who have valid credentials but are not
            part of the Administration of Capturing group can't obtain a Token.
        """
        data = {'username': 'erikiano', 'password': 'vacalalo'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
