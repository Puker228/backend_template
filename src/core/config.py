from pathlib import Path
from typing import Optional

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_ignore_empty=True,
    )

    # init
    SUPERADMIN_EMAIL: str
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
    PROJECT_NAME: str
    DEBUG: bool

    # sentry
    SENTRY_DSN: Optional[str]
    SENTRY_ENVIRONMENT: Optional[str]

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
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str


settings = Settings()
