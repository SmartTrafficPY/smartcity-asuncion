import datetime

import pytz
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from uccarpool.models import Carpool, CarpoolItinerary, RequestCarpool, UserItinerary
from ucusers.models import UcarpoolingProfile

REQUEST_CARPOOL_URL = reverse("ucusers:requestcarpool-list")


def detail_url(carpool_id):
    """Return carpool detail URL"""
    return reverse("ucusers:requestcarpool-detail", args=[carpool_id])


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
        "timeOfArrival": datetime.datetime(2019, 5, 17, 15, 0, 0, tzinfo=pytz.UTC),
    }

    """
    Override any field of the defaults dictionary.
    """
    defaults.update(params)

    return UserItinerary.objects.create(ucarpoolingProfile=user, **defaults)


def create_sample_carpool(driver, poolers, itinerary):

    carpoolItinerary = CarpoolItinerary.objects.create(itinerary=itinerary)

    carpool_object = Carpool.objects.create(driver=driver, carpoolItinerary=carpoolItinerary)

    for pooler in poolers:
        carpool_object.poolers.add(pooler)

    return carpool_object


class UnauthorizedModelTests(TestCase):
    """Test suite for public unauthorized requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Checking if the user is not authorized to make the request"""

        res = self.client.get(REQUEST_CARPOOL_URL)

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

    def test_create_carpool_request_successful(self):
        """Test if a user can create a new carpool request"""

        """Creating another user with his itinerary"""
        another_user1 = create_sample_carpooling_user(username="another_user1")
        another_user1_itinerary = create_sample_user_itinerary(another_user1)

        """Creating another pooler"""
        another_user2 = create_sample_carpooling_user(username="another_user2")

        """Creating a carpool where the user is not participating"""
        other_carpool = create_sample_carpool(
            driver=another_user1, poolers=[another_user2], itinerary=another_user1_itinerary
        )

        payload = {"recipient": another_user1.id, "subject": other_carpool.id}

        res = self.client.post(REQUEST_CARPOOL_URL, payload, format="json")

        """The user created successfully"""
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        """Assert that the sender of the created carpool request is the user that made the POST"""
        request_carpool_created = RequestCarpool.objects.get(id=res.data["id"])

        self.assertEqual(request_carpool_created.sender, self.ucarpooling_profile_regular_app_user)

    def test_retrieve_carpool_requests_successful(self):
        """Test that a user retrieves his carpool requests AND ONLY HIS"""

        """Create an itinerary for the user"""
        user_itinerary1 = create_sample_user_itinerary(self.ucarpooling_profile_regular_app_user)

        """Creating another user with his itinerary"""
        another_user1 = create_sample_carpooling_user(username="another_user1")

        """Creating another pooler"""
        another_user2 = create_sample_carpooling_user(username="another_user2")

        """Creating another pooler"""
        another_user3 = create_sample_carpooling_user(username="another_user3")
        another_user3_itinerary = create_sample_user_itinerary(another_user3)

        """Creating carpools where the user is the driver"""
        carpool1 = create_sample_carpool(
            driver=self.ucarpooling_profile_regular_app_user,
            poolers=[another_user1, another_user2],
            itinerary=user_itinerary1,
        )

        """Creating a carpool where the user is not participating"""
        carpool3 = create_sample_carpool(
            driver=another_user3, poolers=[another_user1, another_user2], itinerary=another_user3_itinerary
        )

        """
        Creating the requests the user made for participate in the first 2 carpools
        """

        # Requesting a pooler to participate in a carpool where the user is the driver"""
        RequestCarpool.objects.create(
            sender=self.ucarpooling_profile_regular_app_user, recipient=another_user3, subject=carpool1
        )
        # Requesting to participate in a carpool where the user desires to be a pooler"""
        RequestCarpool.objects.create(
            sender=self.ucarpooling_profile_regular_app_user, recipient=another_user3, subject=carpool3
        )

        res = self.client.get(REQUEST_CARPOOL_URL)

        """Asserting that only 2 request listed"""
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_cannot_retrieve_other_users_requests(self):
        """Test that users can't retrieve other users carpools requqest by id"""

        """Creating another user with his itinerary"""
        another_user1 = create_sample_carpooling_user(username="another_user1")
        another_user1_itinerary = create_sample_user_itinerary(another_user1)

        """Creating another pooler"""
        another_user2 = create_sample_carpooling_user(username="another_user2")

        """Creating a carpool where the user is not participating"""
        other_carpool = create_sample_carpool(
            driver=another_user1, poolers=[another_user2], itinerary=another_user1_itinerary
        )

        """Creating a request that the user did not make"""
        other_carpool_request = RequestCarpool.objects.create(
            sender=another_user2, recipient=another_user1, subject=other_carpool
        )

        res = self.client.get(detail_url(other_carpool_request.id))

        self.assertNotEqual(res.status_code, status.HTTP_200_OK)
