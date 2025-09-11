up:
	@cd src && uvicorn main:app --reload

dev:
	@PYTHONPATH=src fastapi dev src/main.py

test:
	@PYTHONPATH=src:tests pytest

format:
	@ruff check --select I,F401 --fix && ruff format

docker:
	@docker compose build && docker compose down && docker compose up -d

stop:
	@docker compose stop
