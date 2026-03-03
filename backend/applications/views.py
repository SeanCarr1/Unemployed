from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == 'seeker':
            return Application.objects.filter(seeker=user).order_by('-applied_at')
        elif role == 'employer':
            return Application.objects.filter(job__employer=user).order_by('-applied_at')
        return Application.objects.none()
    queryset = Application.objects.all().order_by('-applied_at')
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        from .permissions import IsSeeker, IsSeekerOrEmployerOfJob, IsEmployerOfJob
        # Only seekers can create applications, others can read/list
        if self.action == 'create':
            return [IsAuthenticated(), IsSeeker()]
        
        if self.action in ['retrieve', 'list']:
            return[IsAuthenticated(), IsSeekerOrEmployerOfJob()]
        
        if self.action in ['update', 'partial_update']:
            return[IsAuthenticated(), IsEmployerOfJob()]

        return [IsAuthenticated()]
    
        

    def perform_create(self, serializer):
        serializer.save(seeker=self.request.user)
