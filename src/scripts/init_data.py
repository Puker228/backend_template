from loguru import logger
from sqlalchemy import select

from auth.utils import hash_password
from core.config import settings
from core.database import AsyncSessionLocal
from user.models import User


async def init_superuser():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == settings.SUPERADMIN_EMAIL)
        )
        user = result.scalar_one_or_none()

        if user:
            logger.info("Superadmin is exist")
            return

        new_superuser = User(
            email=settings.SUPERADMIN_EMAIL,
            password=hash_password(settings.SUPERADMIN_PASSWORD),
            login="Admin",
            is_superuser=True,
        )
        session.add(new_superuser)
        await session.commit()
        logger.info("Superadmin is created")
