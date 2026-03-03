from . import AuthenticatedAPITestCase, TestUserFactory, APIClient, JobFactory, status

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
