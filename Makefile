up:
	@cd src && uvicorn main:app --reload

redis:
	@redis-server

flushall:
	@redis-cli flushall