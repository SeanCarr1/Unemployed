from .models import CustomUser


class TestUserFactory:
    # Factory method to create a CustomUser instance for testing
    def create_user(self, **kwargs: dict) -> CustomUser:
        defaults = {
            "email": "default@example.com",
            "username": "defaultuser",
            "password": "defaultpass",
            "role": "seeker",
        }
        defaults.update(kwargs)
        return CustomUser.objects.create_user(**defaults)