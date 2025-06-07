import asyncio
import logging
import os

import pytest
from alembic import command
from alembic.config import Config

from core.database import get_session
from database import TestingSessionLocal
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from settings import test_settings

logger = logging.getLogger(__name__)


@pytest.fixture
def override_db_url(monkeypatch):
    """Замена урла бд для миграций"""
    monkeypatch.setattr(
        "application.db.session.SQLALCHEMY_DATABASE_URL",
        test_settings.SQLALCHEMY_DATABASE_URI,
    )


@pytest.fixture
async def apply_migrations(override_db_url):
    """Применяет миграции к тестовой базе асинхронно"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
    alembic_ini_path = os.path.join(base_dir, "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)
    migrations_path = os.path.join(base_dir, "migrations")
    alembic_cfg.set_main_option("script_location", migrations_path)
    alembic_cfg.set_main_option("sqlalchemy.url", test_settings.SQLALCHEMY_DATABASE_URI)
    logger.info(
        f"Alembic applying migrations to: {alembic_cfg.get_main_option('sqlalchemy.url')}"
    )

    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")


@pytest.fixture(autouse=True)
async def apply_init_data(apply_migrations, test_session: AsyncSession):
    """
    Фикстура, которая после применения миграций выполняет SQL-скрипт для инициализации данных.
    Скрипт находится по пути tests/files/init_data_v3.sql.
    """
    script_path = os.path.join(os.path.dirname(__file__), "files", "init_data_v3.sql")

    with open(script_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    # разбиваем скрипт на отдельные выражения по `;`, фильтруем пустые строки
    commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]

    # выполняем каждую команду отдельно
    for cmd in commands:
        await test_session.execute(text(cmd))

    await test_session.commit()

    yield

    await test_session.execute(text("DROP SCHEMA IF EXISTS analytics CASCADE;"))
    await test_session.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
    await test_session.execute(text("CREATE SCHEMA public;"))

    await test_session.commit()


@pytest.fixture
async def test_session():
    """сессия для тестов"""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest.fixture
async def test_client(test_session: AsyncSession):
    """
    Подменяет get_session из основного приложения и вызывает lifespan
    Args:
        test_session: сессия для работы с бд
    """

    async def override_get_session():
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    async with app.router.lifespan_context(app):
        async with AsyncClient(app=app, base_url=test_settings.BASE_URL) as client:
            yield client

    app.dependency_overrides.clear()
