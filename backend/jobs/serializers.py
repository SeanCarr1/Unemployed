from rest_framework import serializers
from rest_framework.request import Request
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    employer_email = serializers.EmailField(source='employer.email', read_only=True)

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ['posted_at', 'employer']

    def create(self, validated_data):
        request = self.context.get("request")
        if not isinstance(request, Request):
            raise serializers.ValidationError({"detail": "Request context is required."})
        validated_data['employer'] = request.user
        return super().create(validated_data)
        
