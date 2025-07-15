# jobs/factories.py
import factory
from jobs.models import Job

class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    title = "Software Engineer"
    description = "Develop and maintain software."
    location = "Remote"
    salary_min = 10
    salary_max = 20
    job_type = "full-time"

    @classmethod
    def build_api_payload(cls, **kwargs):
        """Return a dict suitable for API POST payload."""
        data = {
            "title": kwargs.get("title", cls.title),
            "description": kwargs.get("description", cls.description),
            "location": kwargs.get("location", cls.location),
            "salary_min": kwargs.get("salary_min", cls.salary_min),
            "salary_max": kwargs.get("salary_max", cls.salary_max),
            "job_type": kwargs.get("job_type", cls.job_type),
        }
        return data