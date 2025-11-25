up:
	if docker network ls --format "{{.Name}}" | grep backend_network; then \
		echo "Network 'backend_network' already exists"; \
	else \
		echo "Creating network 'backend_network'..."; \
		docker network create backend_network; \
	fi

	docker compose build
	docker compose down
	docker compose up -d

stop:
	docker compose stop

test:
	PYTHONPATH=src:tests pytest

format:
	uv run ruff check --select I,F401 --fix
	uv run ruff format

down:
	docker compose down
	docker volume prune -a -f

prune:
	make stop
	docker compose down
	docker system prune -a -f
	docker volume prune -a -f
