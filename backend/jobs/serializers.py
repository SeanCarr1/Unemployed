from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    employer_email = serializers.EmailField(source='employer.email', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'location',
            'salary_min', 'salary_max', 'job_type',
            'posted_at', 'employer', 'employer_email'
        ]
        read_only_fields = ['posted_at', 'employer']
