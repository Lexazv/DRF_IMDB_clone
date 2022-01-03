from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from Platforms.models import Platform
from Films.models import Film
from Reviews.models import Review, Like
from utils.django_test_helpers import create_user, login_user_jwt, dump


class TestReview(TestCase):

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
        self.film = Film.objects.create(
            title='test title',
            director='test director',
            released_on='2020-12-12',
            description='test description',
            platform=self.platform,
            owner=self.user
        )

    def test_create_review(self):
        response = self.client.post('/reviews/list/',
            data={
                'film': self.film.id,
                'rate': '5',
                'description': 'test description'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
            {
                'id': response.data.get('id'),
                'owner': response.data.get('owner'),
                'added_on': response.data.get('added_on'),
                'rate': 5,
                'updated_on': response.data.get('updated_on'),
                'likes_amount': 0,
                'description': "test description",
                'film': response.data.get('film')
            }
        )

    def test_get_review_list(self):
        self.review = Review.objects.create(
            owner=self.user,
            rate=5,
            description='test description',
            film=self.film
        )
        response = self.client.get('/reviews/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
            [
                {
                    'id': response.data[0].get('id'),
                    'owner': response.data[0].get('owner'),
                    'added_on': response.data[0].get('added_on'),
                    'rate': 5,
                    'updated_on': response.data[0].get('updated_on'),
                    'likes_amount': 0,
                    'description': "test description",
                    'film': response.data[0].get('film')
                }
            ]
        )

    def test_get_review_detail(self):
        self.review = Review.objects.create(
            owner=self.user,
            rate=5,
            description='test description',
            film=self.film
        )
        response = self.client.get(f'/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
            {
                'id': response.data.get('id'),
                'owner': response.data.get('owner'),
                'added_on': response.data.get('added_on'),
                'rate': 5,
                'updated_on': response.data.get('updated_on'),
                'likes_amount': 0,
                'description': "test description",
                'film': response.data.get('film')
            }
        )

    def test_create_like(self):
        self.review = Review.objects.create(
            owner=self.user,
            rate=5,
            description='test description',
            film=self.film
        )
        response = self.client.post(f'/reviews/{self.review.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 
            {
                'id': response.data.get('id'),
                'owner': response.data.get('owner'),
                'review': response.data.get('review'),
                'added_on': response.data.get('added_on')
            }
        )

    def test_delete_like(self):
        self.review = Review.objects.create(
            owner=self.user,
            rate=5,
            description='test description',
            film=self.film
        )
        self.like = Like.objects.create(
            owner=self.user,
            review=self.review
        )
        response = self.client.delete(f'/reviews/{self.review.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)


class TestUnAuthAccess(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_unauth_create_review(self):
        response = self.client.post('/reviews/list/',
            data={
                'film': 'self.film.id',
                'rate': '5',
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
        response = self.client.get('/reviews/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data,
            {
                'detail': "Authentication credentials were not provided."
            }
        )

    def test_unauth_get_detail(self):
        response = self.client.get('/reviews/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data,
            {
                'detail': "Authentication credentials were not provided."
            }
        )
