# Makefile

.PHONY: setup install up down seed run test clean

setup:
	python -m venv venv
	@echo "Virtual environment created. Activate with '.\venv\Scripts\activate'"

install:
	pip install poetry
	poetry install

up:
	docker-compose -f deployment/docker/docker-compose.yml up -d
	@echo "Infrastructure is up (Qdrant, Redis, Prometheus, Grafana)"

down:
	docker-compose -f deployment/docker/docker-compose.yml down

seed:
	poetry run python scripts/seed_data.py

run:
	poetry run python src/main.py

test:
	poetry run pytest tests/

lint:
	poetry run flake8 src/
	poetry run black src/ --check
