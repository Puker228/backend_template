from fastapi import FastAPI

from config import settings

app = FastAPI(
    title=settings.app_settings.title,
    debug=settings.app_settings.debug,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
