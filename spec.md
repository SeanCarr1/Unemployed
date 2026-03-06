# Unemployed Project — Feature Spec & Planning

## 1. Admin Features
**Admin Dashboard**
	- Backend: Create admin-only endpoints for user management (`users/views.py`, `users/serializers.py`).
	- Backend: Create admin-only endpoints for company management (`companies/views.py`, `companies/serializers.py`).
	- Frontend: Build dashboard UI for admins (`frontend/src/views/AdminDashboard.vue`) to display and manage users and companies.
	- Admin actions: promote/demote/deactivate users, manage companies (CRUD).
- **Company CRUD**
	- Backend: Add Company model, endpoints for create/read/update/delete (`companies/models.py`, `companies/views.py`).
	- Frontend: Company management UI for admins/employers (`frontend/src/components/CompanyForm.vue`).
- **User Role Management**
	- Backend: Endpoints to promote/demote/deactivate users (`users/views.py`).
	- Frontend: Role management UI, admin controls (`frontend/src/components/UserRoleManager.vue`).

## 2. File Uploads
- **Resume/Cover Letter Upload**
	- Backend: API for file upload, validation, storage (local or S3) (`applications/views.py`, `applications/models.py`).
	- Frontend: Upload UI in application form (`frontend/src/components/applications/ApplicationForm.vue`).
- **Validation & Security**
	- Backend: File type/size validation, virus scan (optional).
	- Infrastructure: Secure storage, access control.

## 3. Notifications & Feedback
- **Email Notifications**
	- Backend: Send emails for application status, job updates (`applications/views.py`, `jobs/views.py`).
	- Infrastructure: SMTP setup, email templates.
- **Frontend Toasts**
	- Frontend: Toast notifications for errors/success (Pinia/store, `frontend/src/components/Toast.vue`).

## 4. Job Application Status
- **Status Updates**
	- Backend: Employers can update application status (`applications/views.py`).
	- Frontend: UI for status change, seeker view of status (`frontend/src/components/applications/ApplicationList.vue`).

## 5. Profile Management
- **User Profile Edit**
	- Backend: Endpoints for profile update (name, email, password, resume) (`users/views.py`).
	- Frontend: Profile edit UI (`frontend/src/components/ProfileForm.vue`).
- **Employer/Company Profile**
	- Backend: Company info endpoints (`companies/views.py`).
	- Frontend: Company profile UI (`frontend/src/components/CompanyProfile.vue`).

## 6. Security & Permissions
- **Endpoint Protection**
	- Backend: JWT required for protected actions (DRF permissions, `permissions.py`).
- **Role-based Access**
	- Backend: Ensure only employers can edit their jobs (`jobs/permissions.py`).
- **Rate Limiting/Password Reset**
	- Backend: Add rate limiting, password reset endpoints (`users/views.py`).

## 7. Search & Filtering
- **Job Search**
	- Backend: Search/filter endpoints (keyword, location, type, salary) (`jobs/views.py`).

### Backend Integration Tests (format: jobs/tests)
- For each feature, create a test file in the relevant app's `tests/` folder (e.g., `applications/tests/applications_upload_test.py`).
- Use feature-based test classes (e.g., `ResumeUploadTestCase`).
- Use custom base classes and factories for setup (see jobs/tests).
- Use DRF APIClient for API requests.
- Each test method should cover a user story, permission, or edge case.
- Assert on status codes, response data, and DB state.

#### Example: Resume Upload
```python
class ResumeUploadTestCase(AuthenticatedAPITestCase):
	def setUp(self):
		self.seeker = TestUserFactory().create_user(role="seeker")
		self.client = APIClient()
		self.applications_url = "/applications/"

	def test_seeker_can_upload_resume(self):
		self.authenticate(self.seeker)
		with open("tests/files/sample_resume.pdf", "rb") as resume:
			data = {"resume": resume, "job": 1}
			response = self.client.post(self.applications_url, data, format="multipart")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn("resume", response.json())

	---

	# MVP Checklist

	- [ ] User registration & login (SimpleJWT, Djoser)
	- [ ] Job CRUD (employer can post/edit jobs)
	- [ ] Job search & listing (seeker can browse jobs)
	- [ ] Application submission (seeker can apply, upload resume)
	- [ ] Employer dashboard (view/manage applications)
	- [ ] Admin dashboard (manage users/companies)
	- [ ] Profile management (edit user info, resume)
	- [ ] Company CRUD (admin/employer)
	- [ ] Application status updates (employer changes status)
	- [ ] Email notifications (application/job status)
	- [ ] Permissions & role management (seeker/employer/admin)
	- [ ] Pagination for job listings
	- [ ] API documentation (DRF schema)
	- [ ] Frontend toasts for feedback
	- [ ] Automated backend tests (feature-based)
	- [ ] Automated frontend tests (Bun)
	- [ ] Production Docker Compose
	- [ ] CI/CD pipeline

	# Recommended Build Order (for fastest feedback)

	1. User registration & login (so you can log in and test flows)
	2. Job CRUD (employer can post jobs, see them listed)
	3. Job search & listing (seeker can browse jobs)
	4. Application submission (seeker applies, uploads resume)
	5. Employer dashboard (view/manage applications)
	6. Profile management (edit user info, resume)
	7. Application status updates (employer changes status)
	8. Permissions & role management (ensure correct access)
	9. Company CRUD (admin/employer)
	10. Admin dashboard (manage users/companies)
	11. Email notifications (application/job status)
	12. Pagination for job listings
	13. API documentation (DRF schema)
	14. Frontend toasts for feedback
	15. Automated backend tests (feature-based)
	16. Automated frontend tests (Bun)
	17. Production Docker Compose
	18. CI/CD pipeline


## 9. Additional Planning & Decisions

### Frontend Testing
- **Test Runner:** Use Bun for frontend unit/integration tests.
- **Location:** Place tests in `frontend/src/components/tests/` and feature folders.
- **Format:** Feature-based, covering user flows and API interactions.

### API Documentation
- **Backend:** Use DRF schema generation for auto-generated API docs.
- **Endpoint:** Expose `/api/schema/` for OpenAPI/Swagger docs.

### Monitoring & Logging
- **Status:** Not planned for MVP.

### Performance & Scalability
- **Pagination:** Use Django pagination for job listings and other large datasets.
- **Caching/Async:** Not planned for MVP.

### Data Migration & Seeding
- **Factories:** Use factory_boy and custom factory helpers for test data creation.
- **Reference:** See examples in `applications/factories.py` and related tests.

### Internationalization (i18n)
- **Status:** No multi-language support planned.

### Legal & Compliance
- **Status:** Not planned for MVP.

### User Analytics
- **Status:** Not planned for MVP.

### Feature Flags & Rollouts
- **Status:** Not planned for MVP.

### Backup & Disaster Recovery
- **Status:** Not planned for MVP.

	def test_invalid_file_type(self):
		with open("tests/files/invalid.txt", "rb") as resume:
			response = self.client.post(self.applications_url, data, format="multipart")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("resume", response.json())
```

#### For each feature, plan:
- [ ] Test file location (e.g., `applications/tests/applications_upload_test.py`)
- [ ] Test class name (e.g., `ResumeUploadTestCase`)
- [ ] User stories/permissions to cover
- [ ] Edge cases and error handling
- [ ] Use factories for setup
- [ ] Use APIClient for requests
- [ ] Assert on status codes, response, DB state

---

## 9. Styling & Accessibility
- **Tailwind & shadcn-vue**
	- Frontend: Integrate Tailwind, refactor UI (`frontend/src/assets/base.css`, `frontend/src/components/`).
- **Accessibility**
	- Frontend: Add a11y features (labels, keyboard nav, etc.).

## 10. Deployment & CI/CD
- **Production Docker Compose**
	- Infrastructure: Separate prod compose, env files (`docker-compose.prod.yml`).
- **CI/CD Pipeline**
	- Infrastructure: Automated tests, build, deploy (GitHub Actions, etc.).
