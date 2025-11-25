from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from authx.exceptions import JWTDecodeError, MissingTokenError
from fastapi import FastAPI, HTTPException
from loguru import logger
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from starlette import status
from starlette.requests import Request

import models  # noqa: F401
import project_logs.logger_config  # noqa: F401
from api.v1.routers import api_v1_router
from core.config import settings
from core.database import clear_database
from scripts.init_data import init_buckets, init_superuser

if settings.SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        enable_logs=True,
        traces_sample_rate=1.0,
        profile_session_sample_rate=1.0,
        profile_lifecycle="trace",
        send_default_pii=True,
        environment=settings.SENTRY_ENVIRONMENT,
        integrations=[
            StarletteIntegration(
                transaction_style="endpoint",
                failed_request_status_codes={401, *range(500, 599)},
            ),
            FastApiIntegration(
                transaction_style="endpoint",
                failed_request_status_codes={401, *range(500, 599)},
            ),
        ],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_superuser()
    await init_buckets()
    yield


app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG, lifespan=lifespan)
app.include_router(api_v1_router)


@app.post("/clear-db")
async def clear():
    await clear_database()
    return {"message": "db cleared"}


@app.get("/health-check")
async def health_check():
    logger.info("Health check")
    return {"status": "ok"}


@app.get("/api/sentry-debug")
async def trigger_error():
    division_by_zero = 2 / 0


@app.exception_handler(MissingTokenError)
async def missing_token_handler(request: Request, exc: MissingTokenError):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=str(exc),
    )


@app.exception_handler(JWTDecodeError)
async def expired_token_handler(request: Request, exc: JWTDecodeError):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=str(exc),
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        workers=settings.WORKERS,
    )
