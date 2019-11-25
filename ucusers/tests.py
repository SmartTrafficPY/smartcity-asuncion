from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import UcarpoolingProfile


USER_URL = reverse('ucusers:user-list')


class ModelTests(TestCase):
    """ Model tests for ucusers app """

    def setUp(self):
        """ Creating an admin user for granting all privileges """

        self.client = APIClient()

        self.admin = User(username='user', is_staff=True)
        self.admin.set_password('passphrase')
        self.admin.save()

        self.client.force_authenticate(user=self.admin)

    def test_create_user_successful(self):
        """ Test if it can create a new Ucarpooling user successfully"""

        payload = {

            'email': 'test@mail.com',
            'password': '12345678',

            'first_name': 'Cachito',
            'last_name': 'Gonzalez',

            'UcarpoolingProfile': {
                'sex': UcarpoolingProfile.SEX_MALE,
                'smoker': False,
                'musicTaste': [
                    UcarpoolingProfile.MUSIC_GENRE_CUMBIA,
                    UcarpoolingProfile.MUSIC_GENRE_METAL,
                    UcarpoolingProfile.MUSIC_GENRE_RAP
                ]
            }
        }

        res = self.client.post(USER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
