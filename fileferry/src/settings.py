import os

from pydantic_settings import BaseSettings
from typing import Any
from loguru import logger

logger = logger.bind(logger_name="core")


class Settings(BaseSettings):
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_HOST: str = os.getenv("DB_HOST")

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: str = os.getenv("REDIS_PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DEBUG(self) -> bool:
        debug_env = os.getenv("APP_DEBUG", "False").lower() == "true"
        return debug_env

    def __repr__(self):
        return "<Settings [secure]>"


settings = Settings()
