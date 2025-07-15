from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.factories import TestUserFactory
from .factories import JobFactory

# Create your tests here.
class AuthenticatedAPITestCase(APITestCase):
    """Base test case with authentication helper."""

    def authenticate(self, user):
        """Authenticate as the given user using JWT."""
        password = "employerpass" if user.role == "employer" else "seekerpass"
        response = self.client.post("/api/token/", {"email": user.email, "password": password}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

class JobCreationTestCase(AuthenticatedAPITestCase):
    """Feature tests for job creation endpoint."""

    def setUp(self):
        # Create employer and seeker users
        user_factory = TestUserFactory()
        self.employer = user_factory.create_user(password="employerpass", email="employer@gmail.com", role="employer")
        self.seeker = user_factory.create_user(password="seekerpass", email="seeker@gmail.com", role="seeker")
        self.jobs_url = "/api/jobs/"
        self.client = APIClient()


    def test_employer_can_create_job(self):
        """Employer can create a job with valid data."""
        self.authenticate(self.employer)
        data = JobFactory.build_api_payload()
        response = self.client.post(self.jobs_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["title"], data["title"])


    def test_seeker_cannot_create_job(self):
        """Seeker cannot create a job (should be forbidden)."""
        self.authenticate(self.seeker)
        data = JobFactory.build_api_payload()
        response = self.client.post(self.jobs_url, data, format="json")
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])


    def test_invalid_job_data(self):
        """Employer cannot create a job with invalid data (missing title)."""
        self.authenticate(self.employer)
        data = {
            # "title" is missing
            "description": "No title provided.",
            "location": "Remote",
            "salary": 50000
        }
        response = self.client.post(self.jobs_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.json())


class JobRetrieveTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        # Create employer and seeker users
        user_factory = TestUserFactory()
        self.client = APIClient()
        self.employer = user_factory.create_user(email="employer@gmail.com", role="employer")
        self.seeker = user_factory.create_user(email="seeker@gmail.com", role="seeker")
        self.jobs_url = "/api/jobs/"
        self.job = JobFactory.create_job(employer=self.employer)

    def assert_job_response_matches_instance(self, response_data, job):
        """Helper: Assert all relevant fields match between response and job instance."""
        self.assertEqual(response_data["id"], job.id)
        self.assertEqual(response_data["title"], job.title)
        self.assertEqual(response_data["description"], job.description)
        self.assertEqual(response_data["location"], job.location)
        # Add more fields as needed


    def test_retrieve_job_by_id(self):
        """Anyone can retrieve a job by its ID."""
        url = f"{self.jobs_url}{self.job.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.job.id)
        

    def test_retrieve_non_existent_job(self):
        """Retrieving a non-existent job returns 404."""
        url = f"{self.jobs_url}999999/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_response_matches_job_instance(self):
        """API response matches the job instance fields."""
        url = f"{self.jobs_url}{self.job.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_job_response_matches_instance(response.json(), self.job)

