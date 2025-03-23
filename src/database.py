from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import settings

async_engine = create_async_engine(url=settings.SQLALCHEMY_DATABASE_URI)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


async def get_session_without_transaction():
    async with AsyncSessionLocal() as session:
        yield session
