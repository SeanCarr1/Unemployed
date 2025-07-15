from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Job
from .serializers import JobSerializer
from .permissions import IsEmployer, IsJobOwnerOrReadOnly

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsEmployer()]
        
        if self.action in ['retrieve', 'list']:
            return[AllowAny()]
        
        if self.action in ['update', 'partial_update', 'destroy']:
            return[IsAuthenticated(), IsEmployer(), IsJobOwnerOrReadOnly()]
        

        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)
