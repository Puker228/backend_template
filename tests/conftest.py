import asyncio

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from core.database import Base, get_session_without_transaction
from database import TestingSessionLocal
from main import app
from settings import test_settings


@pytest.fixture(autouse=True)
async def reset_db():
    async with TestingSessionLocal() as session:
        # таблицы, без которых нельзя жить
        exclude_tables = {
            "crowd_groups,",
            "roles",
            "cities",
            "regions",
            "districts",
            "support_settings",
            "site_settings",
        }

        # сбор всех таблиц
        table_names = [
            table_name
            for table_name, table in Base.metadata.tables.items()
            if table.schema is None and table_name not in exclude_tables
        ]

        # print("таблицы из схемы public:", ", ".join(table_names))

        tables_str = ", ".join(table_names)

        # очистка данных в таблицах
        if tables_str:
            truncate_stmt = f"TRUNCATE TABLE {tables_str} CASCADE;"
            await session.execute(text(truncate_stmt))
            await session.commit()
        else:
            print("нет таблиц для удаления из схемы public")

    yield


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_session():
    """сессия для тестов"""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def test_client(test_session):
    async def override_get_session():
        yield test_session

    app.dependency_overrides[get_session_without_transaction] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=test_settings.BASE_URL
    ) as client:
        yield client

    app.dependency_overrides.clear()
