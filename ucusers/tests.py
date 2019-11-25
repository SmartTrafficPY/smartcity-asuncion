from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import UcarpoolingProfile

USER_URL = reverse("ucusers:user-list")


def detail_url(user_id):
    """Return user detail URL"""
    return reverse("ucusers:user-detail", args=[user_id])


class UnauthorizedModelTests(TestCase):
    """Test suite for public unauthorized requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Checking if the user is not authorized to make the request"""

        res = self.client.get(USER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthorizedAppModelTests(TestCase):
    """Test suite for authorized requests via token key from the app"""

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

        """The user created successfully"""
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class AuthorizedUserAppModelTests(TestCase):
    """Test suite for authorized requests via token key from ucarpooling users"""

    def setUp(self):
        """ Creating a user for granting privileges of its own information"""

        self.client = APIClient()

        """A typical end user from the ucarpooling app"""
        self.regularAppUser = get_user_model().objects.create(
            username="John.Doe@mail.com", email="John.Doe@mail.com", first_name="John", last_name="Doe"
        )

        self.ucarpooling_regular_app_user = UcarpoolingProfile.objects.create(
            user=self.regularAppUser, sex=UcarpoolingProfile.SEX_MALE, smoker=False
        )

        """Generating the """
        ucarpoolingRegularAppUserToken = Token.objects.create(user=self.regularAppUser)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + ucarpoolingRegularAppUserToken.key)

    def test_patch_user(self):
        """Test if it can full update a user from Ucarpooling app"""

        """
        The user will be replaced with this payload when doing a PUT
        """
        payload = {
            "email": "another@mail.com",
            "ucarpoolingprofile": {"sex": UcarpoolingProfile.SEX_FEMALE, "smoker": True},
        }

        url = detail_url(self.regularAppUser.id)

        self.client.patch(url, payload, format="json")

        """
        Updating the recipe variable with what's in the DB
        """
        self.regularAppUser.refresh_from_db()
        self.ucarpooling_regular_app_user.refresh_from_db()

        self.assertEqual(self.regularAppUser.username, payload["email"])
        self.assertEqual(self.ucarpooling_regular_app_user.sex, payload["ucarpoolingprofile"]["sex"])

    def test_cannot_path_another_user(self):
        """Test it cannot patch another user's details"""

        """ Another user """
        anotherAppUser = get_user_model().objects.create(
            username="another.user@mail.com", email="another.user@mail.com", first_name="Another", last_name="User"
        )

        payload = {
            "email": "forbidden-another-mail@mail.com",
        }

        url = detail_url(anotherAppUser.id)

        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
