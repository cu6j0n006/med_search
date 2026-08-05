.PHONY: up test lint index

up:
	docker compose up -d --force-recreate

dev: 
	poetry run fastapi dev src/medsearch/api/main.py

test:
	poetry run pytest

lint:
	poetry run ruff check .
	poetry run mypy .

format: 
	poetry run ruff check --fix


