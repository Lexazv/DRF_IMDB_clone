from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, \
    BlacklistedToken

from utils.django_test_helpers import create_user, login_user_jwt, dump


class TestUser(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        response = self.client.post('/account/register/',
            data={
                'username': 'test_user',
                'password': '123',
                'email': 'test_user@gmail.com',
                'confirmed_password': '123'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 
            {
                'username': "test_user",
                'email': "test_user@gmail.com"
            }
        )

    def test_login_user(self):
        self.user = create_user('test_user')
        response = self.client.post('/account/login/',
            data={'username': 'test_user', 'password': '123'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 
            {
                'refresh': response.data.get('refresh'),
                'access': response.data.get('access')
            } 
        )

    def test_refresh_token(self):
        self.user = create_user('test_user')
        login_response = self.client.post('/account/login/',
            data={
                'username': self.user.username, 'password': '123'
            }
        )
        self.refresh_token = login_response.data.get('refresh')
        self.access_token = login_response.data.get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.post('/account/refresh/',
            data={
                'refresh': self.refresh_token
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 
            {'access': response.data.get('access')}
        )

    def test_logout_user(self):
        self.user = create_user('test_user')
        login_user_jwt(self.client, self.user, '/account/login/')
        response = self.client.post('/account/logout/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 
            {
                'id': response.data.get('id'),
                'token': response.data.get('token'),
                'blacklisted_at': response.data.get('blacklisted_at')
            }
        )
