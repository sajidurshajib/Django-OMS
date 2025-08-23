# Docker build command
build:
	docker build -t oms .

# Docker compose run command
run:
	docker compose up -d

# Docker restart command
restart:
	docker compose restart
	
# Docker backend logs
logs:
	docker compose logs --since=1h api

rebuild:
	docker compose down --volumes --remove-orphans
	docker compose build --no-cache
	docker compose up -d

# Run container shell
shell:
	docker compose exec api bash

# Docker compose stop command
stop:
	docker compose down

# For Formatting and linting tasks
ruff-check:
	ruff check .

ruff-check-fix:
	ruff check . --fix

ruff-check-import-fix:
	ruff check . --select I --fix

ruff-format:
	ruff format .

ruff-all:
	ruff check . --fix
	ruff check . --select I --fix
	ruff format .