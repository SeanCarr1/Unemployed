from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

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