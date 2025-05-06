from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    """
    Redis конфиг
    """

    host: str
    port: int
    socket_timeout: int = (
        1  # сколько времени даем на операцию(1 секунды с головой для микросервиса)
    )
    socket_connect_timeout: int = (
        1  # сколько времени даем на попытку подключение(опять же 1 секунда более чем)
    )
    cache_prefix: str  # по этому префикс будет лежать кэш
    cache_ttl: int  # ttl кэша в секундах

    class Config:
        env_prefix = "REDIS_"
        env_file = "redis.env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __repr__(self) -> str:
        return "<RedisConfig [secure]>"
