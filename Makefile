up:
	@cd src && uvicorn main:app --reload

dev:
	@PYTHONPATH=src fastapi dev src/main.py

test:
	@PYTHONPATH=src:tests pytest

format:
	@black . && isort .
