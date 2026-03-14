from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from typing import Any, cast

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


# --- ADMIN DASHBOARD TESTS ---
class AdminUserListTestCase(APITestCase):
    """Tests that only admin can list all users via /users/ endpoint."""
    client: APIClient

    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass",
            role="employer"
        )
        self.user = CustomUser.objects.create_user(
            email="user@example.com",
            username="user",
            password="userpass",
            role="seeker"
        )
        self.list_url = "/users/"

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin)
        response = cast(Any, self.client.get(self.list_url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", [])
        self.assertTrue(any(u["email"] == "user@example.com" for u in results))

    def test_non_admin_cannot_list_users(self):
        self.client.force_authenticate(user=self.user)
        response = cast(Any, self.client.get(self.list_url))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.login_url = "/token/"

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


