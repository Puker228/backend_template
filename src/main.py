from fastapi import FastAPI

from config import settings

app = FastAPI(
    title=settings.app_settings.title,
    debug=settings.app_settings.debug,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
