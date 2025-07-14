---
applyTo: '**'
---
# Coding Standards, Domain Knowledge, and Preferences

## 1. Python & Django
- Use OOP and dependency injection where it makes sense.
- Always use type annotations.
- All model changes must go through Django migrations.
- Use and leverage PostgreSQL features via Django ORM when possible.
- Separate business logic from views (use services or utils).
- Use MVT (Model-View-Template) pattern.
- Use JSON responses for backend errors that users should not see.

## 2. TypeScript & Vue
- Use TypeScript everywhere.
- Use the Composition API (`<script setup lang="ts">`).
- Use Pinia for state management.
- Vue components must be PascalCase.
- Use Tailwind CSS and shadcn-vue for UI (when ready).
- For now, use plain HTML for MVP, minimal CSS.
- Components can be page-specific for now.

## 3. API & Auth
- Use RESTful API design with kebab-case endpoints.
- Use SimpleJWT for authentication.
- Some endpoints will be protected in the future.
- No API versioning for now.

## 4. Error Handling & User Feedback
- Show errors as toast notifications on the frontend.
- Backend should return JSON error responses for user-facing errors.

## 5. Testing
- Use Django’s built-in testing framework.
- Test coverage should be by feature (expected input/output), not every function.

## 6. Documentation
- No need for extensive docs or docstrings.
- Maintain a README.

## 7. Git & Workflow
- Use feature branches (kebab-case).
- Self-review is fine (solo dev).
- Commit messages should be short and clear.

## 8. Deployment & Environments
- Use Docker Compose for development and deployment.
- Maintain separate settings for dev, testing, and production.
- All secrets must be loaded from environment variables.

## 9. Domain Knowledge
- User roles: job seekers, employers, admins (companies after MVP).
- Seekers can apply to open jobs.
- Employers can edit their own job postings.

## 10. Patterns & Practices
- Favor these patterns: MVT, Factory, Adapter, Decorator, Observer, Command, Strategy, Service Layer, Unit of Work, Dependency Injection, Builder.
- Comment every method/function/class with a one-line description.
- For each major code snippet, explain the main parts in the prompt for learning.
- Prefer explicit, modern code.

## 11. Other
- English only.
- Accessibility and a11y will be handled when shadcn-vue is added.

## 12. Replies to Prompts
- if the reply contains a step by step instruction, instead of replying the code for each step. explain the solution in a high level manner first instead of dumping out a lot of code that would probably be invalidated at the first step due to a library not being installed or a feature not yet implemented.
- do not make any changes until you have 95% confidence that you know what to build. ask me follow up questions until you have that confidence.
---

**If you are unsure about a requirement, ask for clarification before proceeding.**