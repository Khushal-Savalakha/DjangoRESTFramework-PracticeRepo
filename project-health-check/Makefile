APP_NAME=project-health-check

.PHONY: build up down restart logs

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down
	docker compose up -d 

logs:
	docker compose logs -f

shell:
	docker compose exec project-health-check sh

