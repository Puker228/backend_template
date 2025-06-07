up:
	@cd src && uvicorn main:app --reload

dev:
	@PYTHONPATH=src fastapi dev src/main.py

test:
	@PYTHONPATH=src:tests pytest

format:
	@black . && isort .

docker:
	@docker-compose up -d

restart:
	@docker-compose stop && docker-compose build && docker-compose up -d

stop:
	@docker-compose stop