import uuid
from datetime import datetime

from fastapi import Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.config import settings

async_engine = create_async_engine(url=settings.SQLALCHEMY_DATABASE_URI)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, primary_key=True, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)


def get_session(request: Request) -> AsyncSession:
    return request.state.db


async def clear_database():
    async with async_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(text(f"TRUNCATE {table.name} RESTART IDENTITY CASCADE"))
        await conn.commit()
