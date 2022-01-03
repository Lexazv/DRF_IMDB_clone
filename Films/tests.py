from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from Films.models import Film
from Platforms.models import Platform
from utils.django_test_helpers import create_user, login_user_jwt, dump


class TestFilms(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user('test_user')
        login_user_jwt(self.client, self.user, '/account/login/')
        
        self.platform = Platform.objects.create(
            owner=self.user,
            name='test_platform',
            link="https://www.test.org/",
            description="test description"
        )

    def test_create_film(self):
        response = self.client.post('/films/list/',
            data={
                'title': 'test title',
                'director': 'test director',
                'released_on': '2020-12-12',
                'description': 'test description',
                'platform': self.platform.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
            {
                'id': response.data.get('id'),
                'reviews': [],
                'owner': self.user.id,
                'title': "test title",
                'director': "test director",
                'avg_rate': 0.0,
                'reviews_number': 0,
                'released_on': "2020-12-12",
                'description': "test description",
                'added_on': response.data.get('added_on'),
                'platform': self.platform.id
            }
        )

    def test_get_list(self):
        self.film = Film.objects.create(
            title='test title',
            director='test director',
            released_on='2020-12-12',
            description='test description',
            platform=self.platform,
            owner=self.user
        )
        response = self.client.get('/films/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
            [
                {
                    'id': response.data[0].get('id'),
                    'reviews': [],
                    'owner': self.user.id,
                    'title': "test title",
                    'director': "test director",
                    'avg_rate': 0.0,
                    'reviews_number': 0,
                    'released_on': "2020-12-12",
                    'description': "test description",
                    'added_on': response.data[0].get('added_on'),
                    'platform': self.platform.id
                }
            ]
        )

    def test_get_detail(self):
        self.film = Film.objects.create(
            title='test title',
            director='test director',
            released_on='2020-12-12',
            description='test description',
            platform=self.platform,
            owner=self.user
        )
        response = self.client.get(f'/films/{self.film.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
            {
                'id': response.data.get('id'),
                'reviews': [],
                'owner': self.user.id,
                'title': "test title",
                'director': "test director",
                'avg_rate': 0.0,
                'reviews_number': 0,
                'released_on': "2020-12-12",
                'description': "test description",
                'added_on': response.data.get('added_on'),
                'platform': self.platform.id
            }
        )


class TestUnAuthAccess(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_unauth_create_film(self):
        response = self.client.post('/films/list/',
            data={
                'title': 'test title',
                'director': 'test director',
                'released_on': '2020-12-12',
                'description': 'test description',
                'platform': 'self.platfom.id'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data,
            {
                'detail': "Authentication credentials were not provided."
            }
        )

    def test_unauth_get_list(self):
        response = self.client.get('/films/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data,
            {
                'detail': "Authentication credentials were not provided."
            }
        )

    def test_unauth_get_detail(self):
        response = self.client.get('/films/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data,
            {
                'detail': "Authentication credentials were not provided."
            }
        )
