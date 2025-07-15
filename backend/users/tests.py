from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

class RegistrationTestCase(TestCase):
    """Tests user registration via Djoser with role field."""

    def test_user_registration_with_role(self):
        # Arrange: Prepare registration data
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "securepassword123",
            "role": "seeker"
        }
        # Act: Send POST request to Djoser registration endpoint
        response = self.client.post("/auth/users/", data)
        # Assert: Check for successful creation
        self.assertEqual(response.status_code, 201)
        user = CustomUser.objects.get(email="testuser@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "seeker")