from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

import models  # noqa: F401
from api.v1.routers import api_v1_router
from core.config import settings
from core.database import clear_database
from core.middlewares import SQLAlchemySessionMiddleware
from scripts.init_data import init_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_superuser()
    yield


app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG, lifespan=lifespan)
app.include_router(api_v1_router)
app.add_middleware(SQLAlchemySessionMiddleware)


@app.post("/clear-db")
async def clear():
    await clear_database()
    return {"message": "db cleared"}


@app.get("/health-check")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False, workers=1)
