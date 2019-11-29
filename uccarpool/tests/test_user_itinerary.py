from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from uccarpool.models import UserItinerary
from ucusers.models import UcarpoolingProfile

USERITINERARY_URL = reverse("ucusers:useritinerary-list")

# Test that it updates itinerary


def detail_url(itinerary_id):
    """Return useritinerary detail URL"""
    return reverse("ucusers:useritinerary-detail", args=[itinerary_id])


def create_sample_carpooling_user(username="username"):
    """Create a sample user of the Ucarpooling app"""

    regularAppUser = get_user_model().objects.create(
        username=username, email=username, first_name=username, last_name=username
    )

    ucarpooling_profile_regular_app_user = UcarpoolingProfile.objects.create(
        user=regularAppUser, sex=UcarpoolingProfile.SEX_MALE, smoker=False
    )

    """Generating the token key for the user"""
    Token.objects.create(user=regularAppUser)

    return ucarpooling_profile_regular_app_user


def create_sample_user_itinerary(user, **params):
    """ Helper function for creating user itineraries """

    defaults = {
        "isDriver": False,
        "origin": Point(float(-25.0), float(-50.0)),
        "destination": Point(float(-25.0), float(-50.0)),
        "timeOfArrival": "2019-11-29T14:24:08Z",
    }

    """
    Override any field of the defaults dictionary.
    """
    defaults.update(params)

    return UserItinerary.objects.create(ucarpoolingProfile=user, **defaults)


class UnauthorizedModelTests(TestCase):
    """Test suite for public unauthorized requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Checking if the user is not authorized to make the request"""

        res = self.client.get(USERITINERARY_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthorizedUserAppModelTests(TestCase):
    """Test suite for authorized requests via token key from ucarpooling users"""

    def setUp(self):
        """ Creating a user for granting privileges of its own information"""

        self.client = APIClient()

        """A typical end user from the ucarpooling app"""
        self.regularAppUser = get_user_model().objects.create(
            username="John.Doe@mail.com", email="John.Doe@mail.com", first_name="John", last_name="Doe"
        )

        self.ucarpooling_profile_regular_app_user = UcarpoolingProfile.objects.create(
            user=self.regularAppUser, sex=UcarpoolingProfile.SEX_MALE, smoker=False
        )

        """Generating the token key for the user"""
        ucarpoolingRegularAppUserToken = Token.objects.create(user=self.regularAppUser)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + ucarpoolingRegularAppUserToken.key)

    def test_create_userItinerary_successful(self):
        """Test if it can create a new user itinerary successfully"""

        payload = {
            "isDriver": False,
            "origin": "-25.351206,-57.60576",
            "destination": "-25.3388541,-57.57132190000001",
            "timeOfArrival": "2019-11-29T14:24:08Z",
            "timeOfDeparture": "2020-11-29T14:24:08Z",
        }

        res = self.client.post(USERITINERARY_URL, payload, format="json")

        """The user created successfully"""
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        """Assert that the created user itinerary belongs to the user that it created"""
        user_itinerary_created = UserItinerary.objects.get(id=res.data["id"])

        self.assertEqual(user_itinerary_created.ucarpoolingProfile, self.ucarpooling_profile_regular_app_user)

    def test_retrieve_userItinerary_successful(self):
        """Test that a user retrieves his itineraries AND ONLY HIS"""

        create_sample_user_itinerary(self.ucarpooling_profile_regular_app_user)
        create_sample_user_itinerary(self.ucarpooling_profile_regular_app_user)

        another_user = create_sample_carpooling_user("Another user")
        create_sample_user_itinerary(user=another_user)

        res = self.client.get(USERITINERARY_URL)

        """Asserting that only 2 itineraries listed"""
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_cannot_retrieve_other_users_itinerary(self):
        """Test that users can't retrieve other users itinerary by id"""

        another_user = create_sample_carpooling_user("Another user")
        other_itinerary = create_sample_user_itinerary(user=another_user)

        res = self.client.get(detail_url(other_itinerary.id))

        self.assertNotEqual(res.status_code, status.HTTP_200_OK)

    def test_partial_update_recipe(self):
        """Test updating a user itinerary with a PATCH"""

        itinerary = create_sample_user_itinerary(self.ucarpooling_profile_regular_app_user)

        self.assertEqual(itinerary.isDriver, False)

        payload = {"isDriver": True}

        url = detail_url(itinerary.id)

        self.client.patch(url, payload)

        """
        Updating the itinerary variable with what's in the DB
        """
        itinerary.refresh_from_db()

        self.assertEqual(itinerary.isDriver, payload["isDriver"])

    def test_full_update_recipe(self):
        """ Testing a PUT request for a user itinerary """

        itinerary = create_sample_user_itinerary(self.ucarpooling_profile_regular_app_user)

        self.assertEqual(itinerary.isDriver, False)

        """
        The object will be replaced with this payload when doing a PUT
        """
        payload = {
            "isDriver": False,
            "origin": "-25.351206,-57.60576",
            "destination": "-25.3388541,-57.57132190000001",
            "timeOfArrival": "2019-11-29T14:24:08Z",
            "timeOfDeparture": "2020-11-29T14:24:08Z",
        }

        url = detail_url(itinerary.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        """
        Updating the recipe variable with what's in the DB
        """
        itinerary.refresh_from_db()

        self.assertEqual(itinerary.isDriver, payload["isDriver"])
