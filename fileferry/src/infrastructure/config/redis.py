from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    host: str
    port: str

    class Config:
        env_file = "redis.env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __repr__(self) -> str:
        return "<RedisSettings [secure]>"
