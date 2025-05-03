from pathlib import Path

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env.test",
        env_ignore_empty=True,
    )

    # db settings
    TEST_POSTGRES_SERVER: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                username=self.TEST_POSTGRES_USER,
                password=self.TEST_POSTGRES_PASSWORD,
                host=self.TEST_POSTGRES_SERVER,
                port=self.TEST_POSTGRES_PORT,
                path=self.TEST_POSTGRES_DB,
            )
        )

    BASE_URL: str = "http://testserver"


test_settings = Settings()
