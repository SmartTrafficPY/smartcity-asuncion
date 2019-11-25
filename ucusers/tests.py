from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import UcarpoolingProfile

USER_URL = reverse("ucusers:user-list")


class UnauthorizedModelTests(TestCase):
    """Test suite for public unauthorized requests """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Checking if the user is not authorized to make the request"""

        res = self.client.get(USER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthorizedModelTests(TestCase):
    """Test suite for authorized requests """

    def setUp(self):
        """ Creating an admin user for granting all privileges """

        self.client = APIClient()

        """The 'user' for the Ucarpooling app"""
        ucarpoolingAppUser = get_user_model().objects.create(username="Ucarpooling")

        """Adding to the ucarpooling app specific group"""
        ucarpoolingAppGroup = Group.objects.create(name="ucarpooling apps")
        ucarpoolingAppGroup.user_set.add(ucarpoolingAppUser)

        """Generating the """
        ucarpoolingAppToken = Token.objects.create(user=ucarpoolingAppUser)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + ucarpoolingAppToken.key)

    def test_create_user_successful(self):
        """Test if it can create a new Ucarpooling user successfully"""

        payload = {
            "email": "test@mail.com",
            "password": "12345678",
            "first_name": "Cachito",
            "last_name": "Gonzalez",
            "UcarpoolingProfile": {
                "sex": UcarpoolingProfile.SEX_MALE,
                "smoker": False,
                "musicTaste": [
                    UcarpoolingProfile.MUSIC_GENRE_CUMBIA,
                    UcarpoolingProfile.MUSIC_GENRE_METAL,
                    UcarpoolingProfile.MUSIC_GENRE_RAP,
                ],
            },
        }

        res = self.client.post(USER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
