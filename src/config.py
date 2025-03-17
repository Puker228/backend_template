from dataclasses import dataclass

from environs import Env


@dataclass
class Database:
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: int
    echo: bool
    db_url: str

@dataclass
class AppSettings:
    title: str
    debug: bool


@dataclass
class Config:
    app_settings: AppSettings
    database: Database


# функция, которая считывает данные с .env
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        app_settings=AppSettings(
            title=env("SWAGGER_TITLE"),
            debug=env("DEBUG"),
        ),
        database=Database(
            db_name=env("DB_NAME"),
            db_user=env("DB_USER"),
            db_port=env("DB_PORT"),
            db_pass=env("DB_PASS"),
            db_host=env("DB_HOST"),
            echo=env("ECHO"),
            db_url=f"postgresql+asyncpg://{env.str('DB_USER')}:{env.str('DB_PASS')}@{env.str('DB_HOST')}:{env.str('DB_PORT')}/{env.str('DB_NAME')}",
        ),
    )


settings = load_config()
