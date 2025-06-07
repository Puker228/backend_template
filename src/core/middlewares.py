import time

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from core.database import AsyncSessionLocal


class SQLAlchemySessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with AsyncSessionLocal() as session:
            request.state.db = session
            start_time = time.time()
            try:
                response = await call_next(request)
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.exception("DB error during request")
                raise e
            finally:
                process_time = time.time() - start_time
                logger.info(
                    f"{request.method} {request.url.path} completed in {process_time:.2f}s"
                )
                await session.close()
        return response
