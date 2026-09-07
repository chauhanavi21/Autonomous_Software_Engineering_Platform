.PHONY: setup up down logs migrate migration test lint format typecheck ci

setup:
	@test -f .env || cp .env.example .env
	docker compose build

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose run --rm api alembic upgrade head

migration:
	docker compose run --rm api alembic revision --autogenerate -m "$(m)"

test:
	docker compose run --rm api pytest -q

lint:
	docker compose run --rm api ruff check .

dformat:
	docker compose run --rm api ruff format .

format:
	docker compose run --rm api ruff format .

typecheck:
	docker compose run --rm api mypy app

ci:
	docker compose run --rm api sh -c "ruff check . && mypy app && pytest -q"
