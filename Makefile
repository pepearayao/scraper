# Scraper Engine Makefile

.PHONY: help install test test-unit test-integration test-slow test-coverage clean lint format

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements-test.txt

test:  ## Run all tests
	cd engine && python -m pytest

test-unit:  ## Run fast unit tests only
	cd engine && DJANGO_SETTINGS_MODULE=settings.test python -m pytest -m unit

test-integration:  ## Run integration tests
	cd engine && python -m pytest -m integration

test-slow:  ## Run comprehensive/slow tests
	cd engine && python -m pytest -m slow

test-models:  ## Run model-specific tests
	cd engine && python -m pytest -m models

test-coverage:  ## Run tests with coverage report
	cd engine && python -m pytest --cov=. --cov-report=html --cov-report=term

test-parallel:  ## Run tests in parallel
	cd engine && python -m pytest -n auto

test-watch:  ## Watch for changes and run tests
	cd engine && python -m pytest --looponfail

clean:  ## Clean up test artifacts
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf engine/htmlcov
	rm -rf .pytest_cache

lint:  ## Run linting
	cd engine && flake8 .

format:  ## Format code
	cd engine && black .
	cd engine && isort .

migrate:  ## Run Django migrations
	cd engine && python manage.py migrate

makemigrations:  ## Create Django migrations
	cd engine && python manage.py makemigrations

shell:  ## Open Django shell
	cd engine && python manage.py shell

runserver:  ## Run Django development server
	cd engine && python manage.py runserver

create-superuser:  ## Create Django superuser
	cd engine && python manage.py createsuperuser