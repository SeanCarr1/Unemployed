from rest_framework.permissions import BasePermission

class IsSeeker(BasePermission):
    """Allows access only to users with role 'seeker'."""
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'seeker'
    
class IsSeekerOrEmployerOfJob(BasePermission):
    """Allow access only to the seeker or the employer of the job."""
    def has_object_permission(self, request, view, obj):
        return (
            obj.seeker == request.user or
            getattr(obj.job, 'employer', None) == request.user
        )
    
class IsEmployerOfJob(BasePermission):
    """Allow access only to the employer of the job"""
    def has_object_permission(self, request, view, obj):    
        return (
            getattr(obj.job, 'employer', None) == request.user
        )