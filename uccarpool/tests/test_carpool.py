from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CARPOOL_URL = reverse("ucusers:carpool-list")


class UnauthorizedModelTests(TestCase):
    """Test suite for public unauthorized requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Checking if the user is not authorized to make the request"""

        res = self.client.get(CARPOOL_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
