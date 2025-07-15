from rest_framework.permissions import BasePermission
from users.models import CustomUser

class IsEmployer(BasePermission):
    """Allows access only to users with employer role."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated 
            and getattr(request.user, "role", None) == "employer"
        )