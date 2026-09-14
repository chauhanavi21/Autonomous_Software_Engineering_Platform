# ForgeOS — Phase 2

Autonomous software-engineering platform foundation with identity, RBAC, organizations, workspaces, and tenant-aware projects.

## Stack
Next.js, TypeScript, FastAPI, PostgreSQL, Redis, SQLAlchemy, Alembic, Docker Compose, Argon2, JWT, pytest, Ruff, mypy.

## Run
1. `cp .env.example .env` (PowerShell: `Copy-Item .env.example .env`)
2. Change `JWT_SECRET` in `.env` to a long random value.
3. `docker compose up --build -d`
4. `docker compose exec api alembic upgrade head`
5. Open `http://localhost:3000/register` and `http://localhost:8000/docs`.

## Authentication flow
Register -> login -> short-lived access JWT + HttpOnly refresh cookie -> protected `/auth/me` -> refresh rotation.

## Phase 2 APIs
- `/api/v1/auth/register`, `/login`, `/refresh`, `/logout`, `/me`
- `/api/v1/organizations`
- `/api/v1/organizations/{id}/members`
- `/api/v1/organizations/{id}/workspaces`
- `/api/v1/workspaces/{id}/projects`
- `/api/v1/projects/{id}`

## Production note
The localhost refresh cookie uses `secure=false`. Set secure cookies under HTTPS before a real deployment. OAuth provider configuration is represented by environment fields and architecture hooks but external OAuth callbacks are intentionally not enabled until real provider credentials are supplied.
