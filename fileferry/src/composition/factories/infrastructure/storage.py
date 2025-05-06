from miniopy_async import Minio
from redis.asyncio import Redis

from infrastructure.storage.minio import MiniOStorage
from infrastructure.storage.redis import RedisFileMetaCacheStorage


def minio_storage_factory(client: Minio) -> MiniOStorage:
    return MiniOStorage(client=client)


def redis_cache_storage_factory(
    with_cache: bool, client: Redis, prefix: str = "file:meta:"
) -> RedisFileMetaCacheStorage | None:
    if not with_cache:
        return None
    return RedisFileMetaCacheStorage(client=client, prefix=prefix)
