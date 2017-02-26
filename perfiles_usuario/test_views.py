from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token


class TokenCreationTest(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='juliannieb', first_name='Julian',
            last_name='ElGandul', email='Julian69@gmail.com',
            password='vacalalonja')

        self.url = reverse('perfiles_usuario:api_login')

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
