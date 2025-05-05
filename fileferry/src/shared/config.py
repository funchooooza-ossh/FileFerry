from typing import Any

from loguru import logger
from pydantic_settings import BaseSettings

logger = logger.bind(logger_name="core")


class Settings(BaseSettings):
    app_debug: bool
    configuration: str
    cache_enabled: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return "<Settings [secure]>"


settings = Settings()
