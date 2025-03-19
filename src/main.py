import uvicorn
from fastapi import FastAPI

from config import settings

app = FastAPI(
    title=settings.app_settings.title,
    debug=settings.app_settings.debug,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
