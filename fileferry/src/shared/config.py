from typing import Any

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_debug: bool
    cache_enabled: bool
    main_route: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return "<Settings [secure]>"


settings = Settings()
