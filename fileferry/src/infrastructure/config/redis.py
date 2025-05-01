from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    host: str
    port: int

    class Config:
        env_prefix = "REDIS_"
        env_file = "redis.env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __repr__(self) -> str:
        return "<RedisConfig [secure]>"
