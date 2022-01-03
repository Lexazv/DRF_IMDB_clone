from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from Platforms.models import Platform
from utils.django_test_helpers import create_user, login_user_jwt, dump


class TestPlatforms(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user('test_user')
        login_user_jwt(self.client, self.user, '/account/login/')

    def test_create_platform(self):
        response = self.client.post(
            '/platforms/list/',
            data = {
                'name': 'test_platform',
                'link': 'https://www.test.org/',
                'description': 'test description'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 
            {
                'id': response.data.get('id'),
                'films': [],
                'owner': self.user.id,
                'name': "test_platform",
                'link': "https://www.test.org/",
                'description': "test description",
                'added_on': response.data.get('added_on')
            }
        )

    def test_get_list(self):
        Platform.objects.create(
            owner=self.user,
            name='test_platform',
            link="https://www.test.org/",
            description="test description"
        )
        response = self.client.get('/platforms/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
            [
                {
                    'id': response.data[0].get('id'),
                    'films': [],
                    'owner': self.user.id,
                    'name': "test_platform",
                    'link': "https://www.test.org/",
                    'description': "test description",
                    'added_on': response.data[0].get('added_on')
                }
            ]
        )

    def test_get_detail(self):
        self.platform = Platform.objects.create(
            owner=self.user,
            name='test_platform',
            link="https://www.test.org/",
            description="test description"
        )
        response = self.client.get(f'/platforms/{self.platform.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 
            {
                'id': response.data.get('id'),
                'films': [],
                'owner': self.user.id,
                'name': "test_platform",
                'link': "https://www.test.org/",
                'description': "test description",
                'added_on': response.data.get('added_on')
            }
        )


class TestUnAuthAccess(TestCase):
    
    def setUp(self):
        self.client = APIClient()

    def test_unauth_create_platform(self):
        response = self.client.post(
            '/platforms/list/',
            data = {
                'name': 'test_platform',
                'link': 'https://www.test.org/',
                'description': 'test description'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, 
            {
                'detail': "Authentication credentials were not provided."
            }
        )

    def test_unauth_get_list(self):
        response = self.client.get('/platforms/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, 
            {
                'detail': "Authentication credentials were not provided."
            }
        )

    def test_unauth_get_detail(self):
        self.user = create_user('test_user')
        self.platform = Platform.objects.create(
            owner=self.user,
            name='test_platform',
            link="https://www.test.org/",
            description="test description"
        )
        response = self.client.get(f'/platforms/{self.platform.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, 
            {
                'detail': "Authentication credentials were not provided."
            }
        )
