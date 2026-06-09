.PHONY: setup logs logs-api logs-worker up down logs rebuild test clean deep-clean

setup:
	cp .env.sample .env
	cp .env.sample .env.test

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f api worker

logs-api:
	docker-compose logs -f api

logs-worker:
	docker-compose logs -f worker

rebuild:
	docker-compose up -d --build

test:
	docker-compose run --rm test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache

deep-clean: clean down
	docker-compose down -v --remove-orphans
