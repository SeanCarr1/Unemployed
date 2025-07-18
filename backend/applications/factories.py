import factory
from .models import Application
from jobs.factories import JobFactory
from users.factories import TestUserFactory
from typing import Any

class ApplicationFactory(factory.django.DjangoModelFactory):
    """Factory for creating Application instances for tests."""
    class Meta:
        model = Application

    job = factory.SubFactory(JobFactory)
    seeker = factory.LazyFunction(lambda: TestUserFactory().create_user(role="seeker"))
    resume = factory.django.FileField(filename="resume.pdf")
    cover_letter = factory.django.FileField(filename="cover_letter.pdf")
    status = "pending"

    @classmethod
    def build_api_payload(cls, **kwargs: Any) -> dict:
        """Return a dict suitable for API POST payload."""
        job = kwargs.get("job") or JobFactory.create_job()
        seeker = kwargs.get("seeker") or TestUserFactory().create_user(role="seeker")
        data = {
            "job": job.pk,
            "seeker": seeker.pk,
            # For API, you may need to mock file uploads or use simple strings for resume/cover_letter
            "resume": "resume.pdf",
            "cover_letter": "cover_letter.pdf",
            "status": kwargs.get("status", "pending"),
        }
        data.update(kwargs)
        return data

    @classmethod
    def create_application(cls, **kwargs: Any) -> Application:
        """Create and return an Application instance using factory_boy with optional overrides."""
        return cls.create(**kwargs)
