DC := docker compose
EXEC := docker exec -it
LOGS := docker logs
ENV := --env-file .env
APP_FILE := docker_compose/app.yaml


.PHONY: run
run:
	python -m src

.PHONY: install
install:
	poetry install --with dev,test,lint --no-root

.PHONY: lint
lint:
	just _py pre-commit run --all-files

.PHONY: up
up:
	${DC} up --build -d

