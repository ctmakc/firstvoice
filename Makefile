.PHONY: up down logs migrate test lint typecheck

up:
	cd infra && docker compose up -d

down:
	cd infra && docker compose down

logs:
	cd infra && docker compose logs -f

migrate:
	cd apps/api && alembic upgrade head

makemigrations:
	cd apps/api && alembic revision --autogenerate -m "$(msg)"

test-api:
	cd apps/api && pytest -v

test-web:
	cd apps/web && npm run test

lint-api:
	cd apps/api && ruff check .

lint-web:
	cd apps/web && npm run lint

typecheck-web:
	cd apps/web && npm run typecheck

fmt-api:
	cd apps/api && ruff format .

seed:
	@echo "TODO: seed communities + demo recordings"

shell-api:
	cd infra && docker compose exec api bash

shell-db:
	cd infra && docker compose exec postgres psql -U fv -d firstvoice
