import json

from loguru import logger
from minio import Minio
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


async def init_buckets():
    client = Minio(
        endpoint=settings.MINIO_URL,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        secure=False,
    )

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                "Resource": f"arn:aws:s3:::{settings.MINIO_BUCKET}",
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{settings.MINIO_BUCKET}/*",
            },
        ],
    }

    if not client.bucket_exists(settings.MINIO_BUCKET):
        client.make_bucket(settings.MINIO_BUCKET)
        client.set_bucket_policy(settings.MINIO_BUCKET, json.dumps(policy))
        logger.info("новый бакет инициализирован")
    else:
        logger.info("бакет уже был создан")
