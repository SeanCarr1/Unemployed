from . import AuthenticatedAPITestCase, TestUserFactory, APIClient, JobFactory, status

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
