# ForgeOS — Phase 1

Phase 1 establishes the production-grade foundation for ForgeOS, an autonomous software engineering platform.

## Included

- Next.js + TypeScript frontend
- FastAPI async backend
- PostgreSQL + SQLAlchemy 2.0
- Redis
- Alembic migrations
- Repository + service layers
- UUID primary keys and timestamped models
- Request correlation IDs
- Structured JSON logging
- Centralized exception handling
- API versioning
- Liveness and readiness probes
- Docker / Docker Compose
- Ruff, mypy, pytest, pre-commit
- GitHub Actions CI
- Architecture decision records

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

In another terminal:

```bash
docker compose exec api alembic upgrade head
```

Open:

- Web: http://localhost:3000
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Liveness: http://localhost:8000/api/v1/health/live
- Readiness: http://localhost:8000/api/v1/health/ready

## Tests

```bash
docker compose run --rm api pytest -q
```

## Quality checks

```bash
docker compose run --rm api ruff check .
docker compose run --rm api mypy app
```
