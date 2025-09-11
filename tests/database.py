from settings import test_settings
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

test_engine = create_async_engine(
    url=test_settings.SQLALCHEMY_DATABASE_URI, poolclass=NullPool
)
TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
)
