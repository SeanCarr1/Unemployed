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
        """Authenticate as the given user using JWT (Djoser endpoint)."""
        password = "employerpass" if user.role == "employer" else "seekerpass"
        response = self.client.post("/auth/jwt/create/", {"email": user.email, "password": password}, format="json")
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
        self.jobs_url = "/jobs/"
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
        self.jobs_url = "/jobs/"
        self.job = JobFactory.create_job(employer=self.employer)

    def assert_job_response_matches_instance(self, response_data, job):
        """Helper: Assert all relevant fields match between response and job instance."""
        self.assertEqual(response_data["id"], job.pk)
        self.assertEqual(response_data["title"], job.title)
        self.assertEqual(response_data["description"], job.description)
        self.assertEqual(response_data["location"], job.location)
        # Add more fields as needed


    def test_retrieve_job_by_id(self):
        """Anyone can retrieve a job by its ID."""
        url = f"{self.jobs_url}{self.job.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.job.pk)
        

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


class JobUpdateTestCase(AuthenticatedAPITestCase):
    """Feature tests for job edit (PATCH) endpoint."""

    def setUp(self) -> None:
        """Set up users and a job for update tests."""
        user_factory = TestUserFactory()
        self.employer = user_factory.create_user(password="employerpass", email="employer@gmail.com", role="employer")
        self.other_employer = user_factory.create_user(password="employerpass", email="otheremployer@gmail.com", role="employer")
        self.seeker = user_factory.create_user(password="seekerpass", email="seeker@gmail.com", role="seeker")
        self.jobs_url = "/jobs/"
        self.client = APIClient()
        self.job = JobFactory.create_job(employer=self.employer)


    def test_employer_can_patch_own_job(self):
        """Employer can PATCH their own job with valid data."""
        self.authenticate(self.employer)
        url = f"{self.jobs_url}{self.job.pk}/"
        patch_data = {"title": "Updated Title"}
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], patch_data["title"])


    def test_employer_cannot_patch_others_job(self):
        """Employer cannot PATCH a job they do not own."""
        self.authenticate(self.other_employer)
        url = f"{self.jobs_url}{self.job.pk}/"
        patch_data = {"title": "Hacked Title"}
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_seeker_cannot_patch_any_job(self):
        """Seeker cannot PATCH any job."""
        self.authenticate(self.seeker)
        url = f"{self.jobs_url}{self.job.pk}/"
        patch_data = {"title": "Seeker Edit"}
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_patch_invalid_data_returns_400(self):
        """PATCH with invalid data returns 400."""
        self.authenticate(self.employer)
        url = f"{self.jobs_url}{self.job.pk}/"
        patch_data = {"title": ""}  # Title cannot be empty
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.json())


    def test_patch_read_only_fields_are_ignored(self):
        """PATCHing read-only fields does not change them."""
        self.authenticate(self.employer)
        url = f"{self.jobs_url}{self.job.pk}/"
        patch_data = {
            "employer": self.other_employer.pk,
            "posted_at": "2000-01-01T00:00:00Z",
            "title": "Legit Update"
        }
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh from DB to check if employer/posted_at changed
        self.job.refresh_from_db()
        self.assertEqual(self.job.employer, self.employer)
        self.assertNotEqual(str(self.job.posted_at), "2000-01-01T00:00:00Z")
        self.assertEqual(self.job.title, "Legit Update")

    

class JobDeleteTestCase(AuthenticatedAPITestCase):
    def setUp(self) -> None:
        """Set up users and a job for update tests."""
        user_factory = TestUserFactory()
        self.client = APIClient()

        self.employer = user_factory.create_user(password="employerpass", email="employer@gmail.com", role="employer")
        self.other_employer = user_factory.create_user(password="employerpass", email="otheremployer@gmail.com", role="employer")
        
        self.seeker = user_factory.create_user(password="seekerpass", email="seeker@gmail.com", role="seeker")
        
        self.jobs_url = "/jobs/"
        self.job = JobFactory.create_job(employer=self.employer)
    
    def test_employer_can_delete_own_job(self):
        """Employer can delete their own job"""
        self.authenticate(self.employer)
        url = f"{self.jobs_url}{self.job.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # confirm job is deleted
        # Try to retrieve the deleted job to confirm it's gone
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)


    def test_employer_cannot_delete_another_employers_job(self):
        """Employer cannot delete a job they do not own"""
        self.authenticate(self.other_employer)
        url = f"{self.jobs_url}{self.job.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertTrue(JobFactory._meta.model.objects.filter(pk=self.job.pk).exists())

    def test_seeker_cannot_delete_any_job(self):
        """Seeker cannot DELETE any job."""
        self.authenticate(self.seeker)
        url = f"{self.jobs_url}{self.job.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Confirm job still exists
        self.assertTrue(JobFactory._meta.model.objects.filter(pk=self.job.pk).exists())

    def test_delete_non_existent_job_returns_404(self):
        """Deleting a non-existent job returns 404."""
        self.authenticate(self.employer)
        url = f"{self.jobs_url}999999/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
