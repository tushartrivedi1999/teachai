# Rivinity Learning

Rivinity Learning is a full-stack AI learning platform blueprint for learners from Class 6 to PhD researchers.
It provides dynamic course generation, module-wise practical learning, proctored quizzes, and learner-focused recommendations.

## Tech Stack

- **Frontend:** React + TypeScript + Vite
- **Backend:** FastAPI + SQLModel + JWT auth
- **SDK:** Python client (`sdk/python`)

## Core Features Implemented

- Authentication (register/login with JWT)
- Profile retrieval/update
- Dynamic course generation endpoint
- Personalized suggestion endpoint
- Quiz submission with anti-cheating penalty logic
- React landing page + dashboard layout (sidebar, content area, reminder/calendar panel)
- Popup-based course creation flow with resilient UI error handling
- Python SDK starter for programmatic use

## Project Structure

```text
backend/
  app/
    api/
    core/
    services/
  tests/
frontend/
sdk/python/
docs/
```

## Run Locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE` if backend is not running at `http://localhost:8000/api/v1`.

### SDK

```bash
cd sdk/python
pip install -e .
```

## API Overview

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/users/me`
- `PATCH /api/v1/users/me`
- `POST /api/v1/courses`
- `GET /api/v1/courses`
- `POST /api/v1/quizzes/submit`
- `GET /api/v1/suggestions`

## Notes on Production Hardening

- Move secrets to environment variables.
- Add refresh tokens and secure cookie auth path.
- Add Redis/Celery (or equivalent) for reminders and async generation.
- Add persistent proctoring audit trails.
- Add CI pipelines for lint/test/build/deploy.
