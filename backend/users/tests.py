from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from rest_framework import status

class RegistrationTestCase(TestCase):
    """Tests user registration via Djoser with role field."""

    def test_user_registration_with_role(self):
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "securepassword123",
            "re_password": "securepassword123",
            "role": "seeker"
        }
        response = self.client.post("/auth/users/", data)
        if response.status_code != 201:
            print("Registration failed. Response:", response.content)
        self.assertEqual(response.status_code, 201, f"Expected 201, got {response.status_code}. Response: {response.content}")
        user = CustomUser.objects.get(email="testuser@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "seeker")

# --- LOGIN FLOW TESTS ---

class LoginFlowTestCase(TestCase):
    """Tests login flow for CustomUser using SimpleJWT."""

    def setUp(self):
        # Create a user with all required fields
        self.email = "loginuser@example.com"
        self.username = "loginuser"
        self.password = "testpass123"
        self.role = "employer"
        self.user = CustomUser.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password,
            role=self.role
        )
        self.login_url = "/api/token/"

    def test_login_success(self):
        """User can log in with valid email and password and receives tokens."""
        data = {"email": self.email, "password": self.password}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_login_invalid_password(self):
        """Login fails with invalid password."""
        data = {"email": self.email, "password": "wrongpass"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.json())

    def test_login_missing_email(self):
        """Login fails with missing email field."""
        data = {"password": self.password}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.json())


