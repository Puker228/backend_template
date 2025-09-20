up:
	docker compose build
	docker compose down
	docker compose up -d

test:
	@PYTHONPATH=src:tests pytest

format:
	ruff check --select I,F401 --fix
	ruff format

stop:
	@docker compose stop

prune:
	make stop
	docker compose down
	docker system prune -a -f
	docker volume prune -a -f
