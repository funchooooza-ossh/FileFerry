from miniopy_async import Minio
from redis.asyncio import Redis
from redis.backoff import NoBackoff
from redis.retry import Retry
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from infrastructure.config.minio import MinioConfig
from infrastructure.config.redis import RedisConfig


def redis_client_factory(config: RedisConfig, with_cache: bool) -> Redis | None:
    if not with_cache:
        return None
    return Redis(
        host=config.host,
        port=config.port,
        socket_connect_timeout=config.socket_connect_timeout,
        socket_timeout=config.socket_timeout,
        retry=Retry(NoBackoff(), retries=0),  # type: ignore
    )


def create_db_engine(url: str, echo: bool = False) -> AsyncEngine:
    return create_async_engine(url=url, echo=echo)


def db_sessionmaker(
    engine: AsyncEngine, autoflush: bool, expire_on_commit: bool = False
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        autoflush=autoflush,
        expire_on_commit=expire_on_commit,
        autocommit=False,
    )


def db_session_factory(sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncSession:
    return sessionmaker()


def minio_client_factory(config: MinioConfig) -> Minio:
    return Minio(
        endpoint=config.endpoint,
        access_key=config.access,
        secret_key=config.secret,
        secure=config.secure,
    )
