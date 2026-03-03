from . import AuthenticatedAPITestCase, TestUserFactory, APIClient, JobFactory, status


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
