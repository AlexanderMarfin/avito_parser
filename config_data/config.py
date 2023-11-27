from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:  # Токен для доступа к телеграм-боту
    token: str


@dataclass
class DbConfig:  # Параметры БД
    host: str
    port: str
    database: str
    user: str
    password: str


@dataclass
class WebDriverConfig:  # Параметры Selenium
    host: str
    port: str


@dataclass
class Config:
    tg_bot: TgBot
    db_config: DbConfig
    webdriver_config: WebDriverConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")),
        db_config=DbConfig(
            host=env("HOST"),
            port=env("PORT"),
            database=env("DATABASE"),
            user=env("USER"),
            password=env("PASSWORD"),
        ),
        webdriver_config=WebDriverConfig(
            host=env("WEBDRIVER_HOST"), port=env("WEBDRIVER_PORT")
        ),
    )
