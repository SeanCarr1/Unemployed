from .models import CustomUser
from typing import Any

class TestUserFactory:
    # Factory method to create a CustomUser instance for testing
    def create_user(self, **kwargs: Any) -> CustomUser:
        defaults = {
            "email": "default@example.com",
            "username": "defaultuser",
            "password": "defaultpass",
            "role": "seeker",
        }
        defaults.update(kwargs)
        return CustomUser.objects.create_user(**defaults)