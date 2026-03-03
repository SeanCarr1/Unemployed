from . import AuthenticatedAPITestCase, TestUserFactory, APIClient, JobFactory, status

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
