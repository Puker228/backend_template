from pathlib import Path
from typing import Optional

from pydantic import EmailStr, HttpUrl, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # init
    SUPERADMIN_EMAIL: EmailStr
    SUPERADMIN_PASSWORD: str

    # db settings
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )

    # app settings
    PROJECT_NAME: str = "Name"
    DEBUG: bool = True
    WORKERS: int = 1
    JWT_SECRET_KEY: str

    # sentry
    SENTRY_DSN: Optional[HttpUrl] = None
    SENTRY_ENVIRONMENT: Optional[str] = None

    # redis settings
    REDIS_HOST: str
    REDIS_PORT: int

    # s3_media
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_BUCKET: str
    MINIO_URL: str
    MINIO_SEND_URL: str

    # pgadmin web
    PGADMIN_DEFAULT_EMAIL: EmailStr
    PGADMIN_DEFAULT_PASSWORD: str

    RABBIT_USER: str
    RABBIT_PASS: str


settings = Settings()  # type: ignore
