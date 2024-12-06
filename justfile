DC := "docker compose"
EXEC := "docker exec -it"
LOGS := "docker logs"
ENV := "--env-file .env"
APP_FILE := "docker_compose/app.yaml"
package_dir := "src"

# Show help message
help:
    just -l

# Fastapi run
run:
  python -m src

# Install package with dependencies
install:
	poetry install --with dev,test,lint --no-root

# Run pre-commit
lint:
	just _py pre-commit run --all-files

# Up container
up:
  docker compose up --build -d

# Run tests
test *args:
  just _py pytest {{args}}

_py *args:
  poetry run {{args}}
