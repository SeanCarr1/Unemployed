from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.factories import TestUserFactory
from jobs.factories import JobFactory

# Create your tests here.
class AuthenticatedAPITestCase(APITestCase):
    """Base test case with authentication helper."""

    def authenticate(self, user):
        """Authenticate as the given user using JWT (Djoser endpoint)."""
        password = "employerpass" if user.role == "employer" else "seekerpass"
        response = self.client.post("/auth/jwt/create/", {"email": user.email, "password": password}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")