from minio import Minio

from core.config import settings


def create_minio_client():
    return Minio(
        endpoint=settings.MINIO_URL,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        secure=False,
    )
