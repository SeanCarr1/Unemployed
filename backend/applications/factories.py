import factory
from .models import Application
from jobs.factories import JobFactory
from users.factories import TestUserFactory
from typing import Any

from django.core.files.uploadedfile import SimpleUploadedFile

class ApplicationFactory(factory.django.DjangoModelFactory):
    """Factory for creating Application instances for tests."""
    class Meta:
        model = Application

    job = factory.SubFactory(JobFactory)
    seeker = factory.LazyFunction(lambda: TestUserFactory().create_user(role="seeker"))
    resume = factory.LazyAttribute(lambda _: SimpleUploadedFile(
        "resume.pdf", b"dummy pdf file", content_type="application/pdf"
    ))
    cover_letter = factory.LazyAttribute(lambda _: SimpleUploadedFile(
        "cover_letter.pdf", b"dummy cover letter", content_type="application/pdf"
    ))
    status = "pending"

    @classmethod
    def build_api_payload(cls, **kwargs: Any) -> dict:
        """Return a dict suitable for API POST payload (for application creation)."""
        job_id = kwargs.get("job") or JobFactory.create_job().pk
        # Remove seeker and status from payload, as seeker is set by the view and status is read-only
        resume = kwargs.get("resume") or SimpleUploadedFile("resume.pdf", b"dummy pdf file", content_type="application/pdf")
        cover_letter = kwargs.get("cover_letter") or SimpleUploadedFile("cover_letter.pdf", b"dummy cover letter", content_type="application/pdf")
        data = {
            "job": job_id,
            "resume": resume,
            "cover_letter": cover_letter,
        }
        # Only include extra fields that are valid for creation
        for key in ["job", "resume", "cover_letter"]:
            if key in kwargs:
                data[key] = kwargs[key]
        return data

    @classmethod
    def create_application(cls, **kwargs: Any) -> Application:
        """Create and return an Application instance using factory_boy with optional overrides."""
        return cls.create(**kwargs)
