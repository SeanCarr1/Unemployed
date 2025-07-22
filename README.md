# Unemployed

A Django + Vue fullstack web application for job seekers and employers.

## Features
- Job seekers can register, browse jobs, and apply with resume/cover letter uploads
- Employers can post jobs, view applications, and manage their postings
- Admins (future) can manage users and companies
- RESTful API with JWT authentication (SimpleJWT)
- Frontend built with Vue 3, TypeScript, Pinia, and Vite
- Docker Compose for local development and deployment
- Automated tests for backend and frontend

## Tech Stack
- Backend: Django, Django REST Framework, PostgreSQL
- Frontend: Vue 3, TypeScript, Pinia, Vite
- Auth: SimpleJWT
- State: Pinia
- Styling: Tailwind CSS (planned), plain HTML/CSS for MVP
- Testing: Django TestCase, DRF APIClient, Vitest/Jest
- Factories: factory_boy for test data



## Project Structure
```
backend/
  applications/   # Job applications app
  jobs/           # Job postings app
  users/          # User management app
  manage.py
frontend/
  src/            # Vue app source
  public/
  ...
docker-compose.yml
README.md
```


## User Roles
- Job Seekers: apply to jobs
- Employers: post/edit jobs, view applications
- Admins: manage users/companies (future)

## License
MIT

---
For more details, see code comments and the MVP roadmap in `todo.txt`.
