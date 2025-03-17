from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel

from config import settings

async_engine = create_async_engine(url=settings.database.db_url, echo=settings.database.echo)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def get_session_without_transaction():
    async with AsyncSessionLocal() as session:
        yield session
