from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

# Import factories for users, jobs, and applications
from users.factories import TestUserFactory
from jobs.factories import JobFactory
# from .factories import ApplicationFactory  # To be implemented

# Base test case with authentication helper (copied from jobs/tests.py)
class AuthenticatedAPITestCase(APITestCase):
    """Base test case with authentication helper."""

    def authenticate(self, user):
        """Authenticate as the given user using JWT."""
        password = "employerpass" if user.role == "employer" else "seekerpass"
        response = self.client.post("/auth/jwt/create/", {"email": user.email, "password": password}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

# Feature tests for Application creation endpoint
class ApplicationCreationTestCase(AuthenticatedAPITestCase):
    """Feature tests for application creation endpoint."""

    def setUp(self):
        # Create users and job
        user_factory = TestUserFactory()
        self.seeker = user_factory.create_user(password="seekerpass", email="seeker@gmail.com", role="seeker")
        self.employer = user_factory.create_user(password="employerpass", email="employer@gmail.com", role="employer")
        self.job = JobFactory.create_job(employer=self.employer)
        self.applications_url = "/applications/"
        self.client = APIClient()

    def test_seeker_can_apply_to_job(self):
        """Seeker can create an application for a job."""
        # TODO: Use ApplicationFactory.build_api_payload()
        self.authenticate(self.seeker)
        data = {"job": self.job.pk}
        response = self.client.post(self.applications_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.json())

    def test_employer_cannot_apply_to_job(self):
        """Employer cannot create an application (should be forbidden)."""
        self.authenticate(self.employer)
        data = {"job": self.job.pk}
        response = self.client.post(self.applications_url, data, format="json")
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])

    def test_duplicate_application(self):
        """Seeker cannot apply to the same job twice."""
        self.authenticate(self.seeker)
        data = {"job": self.job.pk}
        # First application
        self.client.post(self.applications_url, data, format="json")
        # Duplicate application
        response = self.client.post(self.applications_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_application_data(self):
        """Application creation with invalid data returns 400."""
        self.authenticate(self.seeker)
        data = {"job": None}  # Invalid job
        response = self.client.post(self.applications_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Feature tests for Application listing endpoint
class ApplicationListTestCase(AuthenticatedAPITestCase):
    """Feature tests for application listing endpoint."""

    def setUp(self):
        # Create users, job, and applications
        user_factory = TestUserFactory()
        self.seeker = user_factory.create_user(password="seekerpass", email="seeker@gmail.com", role="seeker")
        self.employer = user_factory.create_user(password="employerpass", email="employer@gmail.com", role="employer")
        self.job = JobFactory.create_job(employer=self.employer)
        self.applications_url = "/applications/"
        self.client = APIClient()
        # TODO: Create applications using ApplicationFactory

    def test_seeker_can_list_own_applications(self):
        """Seeker can list their own applications."""
        self.authenticate(self.seeker)
        response = self.client.get(self.applications_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: Assert applications returned belong to seeker

    def test_employer_can_list_applications_for_their_jobs(self):
        """Employer can list applications for their jobs."""
        self.authenticate(self.employer)
        response = self.client.get(self.applications_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: Assert applications returned are for employer's jobs

# Feature tests for Application retrieve endpoint
class ApplicationRetrieveTestCase(AuthenticatedAPITestCase):
    """Feature tests for application retrieve endpoint."""

    def setUp(self):
        user_factory = TestUserFactory()
        self.seeker = user_factory.create_user(password="seekerpass", email="seeker@gmail.com", role="seeker")
        self.employer = user_factory.create_user(password="employerpass", email="employer@gmail.com", role="employer")
        self.job = JobFactory.create_job(employer=self.employer)
        self.client = APIClient()
        # TODO: Create application using ApplicationFactory
        self.application_id = 1  # Placeholder

    def test_seeker_can_retrieve_own_application(self):
        """Seeker can retrieve their own application."""
        self.authenticate(self.seeker)
        url = f"/applications/{self.application_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employer_can_retrieve_application_for_their_job(self):
        """Employer can retrieve application for their job."""
        self.authenticate(self.employer)
        url = f"/applications/{self.application_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_cannot_retrieve_application(self):
        """Other users cannot retrieve applications they don't own/manage."""
        other_user = TestUserFactory().create_user(password="otherpass", email="other@gmail.com", role="seeker")
        self.authenticate(other_user)
        url = f"/applications/{self.application_id}/"
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

# Feature tests for Application update endpoint
class ApplicationUpdateTestCase(AuthenticatedAPITestCase):
    """Feature tests for application update endpoint."""

    def setUp(self):
        user_factory = TestUserFactory()
        self.seeker = user_factory.create_user(password="seekerpass", email="seeker@gmail.com", role="seeker")
        self.employer = user_factory.create_user(password="employerpass", email="employer@gmail.com", role="employer")
        self.job = JobFactory.create_job(employer=self.employer)
        self.client = APIClient()
        # TODO: Create application using ApplicationFactory
        self.application_id = 1  # Placeholder

    def test_employer_can_update_application_status(self):
        """Employer can update application status (e.g., accept/reject)."""
        self.authenticate(self.employer)
        url = f"/applications/{self.application_id}/"
        patch_data = {"status": "accepted"}
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], "accepted")

    def test_seeker_cannot_update_application_status(self):
        """Seeker cannot update application status."""
        self.authenticate(self.seeker)
        url = f"/applications/{self.application_id}/"
        patch_data = {"status": "accepted"}
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_invalid_data_returns_400(self):
        """PATCH with invalid data returns 400."""
        self.authenticate(self.employer)
        url = f"/applications/{self.application_id}/"
        patch_data = {"status": ""}  # Status cannot be empty
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Feature tests for Application delete endpoint
class ApplicationDeleteTestCase(AuthenticatedAPITestCase):
    """Feature tests for application delete endpoint."""

    def setUp(self):
        user_factory = TestUserFactory()
        self.seeker = user_factory.create_user(password="seekerpass", email="seeker@gmail.com", role="seeker")
        self.employer = user_factory.create_user(password="employerpass", email="employer@gmail.com", role="employer")
        self.job = JobFactory.create_job(employer=self.employer)
        self.client = APIClient()
        # TODO: Create application using ApplicationFactory
        self.application_id = 1  # Placeholder

    def test_seeker_can_withdraw_own_application(self):
        """Seeker can delete (withdraw) their own application."""
        self.authenticate(self.seeker)
        url = f"/applications/{self.application_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_employer_can_delete_application_for_their_job(self):
        """Employer can delete application for their job."""
        self.authenticate(self.employer)
        url = f"/applications/{self.application_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_user_cannot_delete_application(self):
        """Other users cannot delete applications they don't own/manage."""
        other_user = TestUserFactory().create_user(password="otherpass", email="other@gmail.com", role="seeker")
        self.authenticate(other_user)
        url = f"/applications/{self.application_id}/"
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
