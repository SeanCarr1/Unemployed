from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import CustomUser

class IsEmployer(BasePermission):
    """Allows access only to users with employer role."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated 
            and getattr(request.user, "role", None) == "employer"
        )
    

class IsJobOwnerOrReadOnly(BasePermission):
    """Allow only the employer who owns the job to edit it."""

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are always allowed (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Only the employer who owns the job can edit
        return obj.employer == request.user