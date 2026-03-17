from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    employer_email = serializers.EmailField(source='employer.email', read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'salary_min', 'salary_max', 'job_type',
          'employer', 'employer_email', 'posted_at']
        read_only_fields = ['posted_at', 'employer']

    def create(self, validated_data):
        validated_data['employer'] = self.context['request'].user
        return super().create(validated_data)

        
