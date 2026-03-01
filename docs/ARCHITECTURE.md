# Rivinity Learning Architecture

## High-level Components

1. **Web App (React):** Landing, auth entry, dashboard, course creation, suggestions.
2. **API (FastAPI):** Auth, profile, courses, quizzes, suggestions.
3. **Data Layer (SQLModel):** Users, courses, quiz attempts.
4. **AI Services:** Course outline generation service (extensible to Mistral API).
5. **SDK:** Python client for external integrations.

## Dynamic Flow

- User signs up/logs in and receives JWT.
- User updates interests/track in profile.
- User requests course generation by field/title/objectives.
- Backend builds module-wise outline with practical + assessment plan.
- Dashboard fetches personalized suggestions from profile interests.
- Quiz submissions include suspicious action traces and score adjustment.

## Security and Integrity

- Password hashing with bcrypt.
- Bearer token authentication.
- Anti-cheating signal ingestion (`copy`, `paste`, `tab-switch`, `camera-off`).

## Extension Roadmap

- Mistral-powered adaptive curriculum and hint generation.
- NCERT ingestion service.
- Certificate generation and verification endpoint.
- Tool-directory harvester from GitHub datasets.
