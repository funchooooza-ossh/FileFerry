import json
from typing import Optional

from redis.asyncio import Redis

from contracts.infrastructure import DataAccessContract, RedisDataAccessContract
from domain.models import ContentType, FileId, FileMeta, FileName, FileSize
from shared.exceptions.handlers.redis_handler import wrap_redis_failure


class RedisDataAccess(RedisDataAccessContract):
    def __init__(
        self, redis: Redis, delegate: Optional[DataAccessContract] = None
    ) -> None:
        self._delegate = delegate
        self._redis = redis

    async def get(self, file_id: str) -> FileMeta:
        key = self.key(file_id)
        cached = await self._try_get(key)
        if cached:
            return self.deserialize_meta(cached)

        result = await self.delegate.get(file_id=file_id)

        await self._try_set(key, self.serialize_meta(result), 3600)

        return result

    async def save(self, file_meta: FileMeta) -> FileMeta:
        result = await self.delegate.save(file_meta)

        key = self.key(result.get_id())
        cache_value = self.serialize_meta(result)
        await self._try_set(key, cache_value, 3600)

        return result

    async def update(self, meta: FileMeta) -> FileMeta:
        result = await self.delegate.update(meta)

        key = self.key(result.get_id())
        cache_value = self.serialize_meta(result)
        await self._try_set(key, cache_value, 3600)

        return result

    async def delete(self, file_id: str) -> None:
        await self.delegate.delete(file_id)

        key = self.key(file_id)
        await self._try_delete(key)

    @staticmethod
    def deserialize_meta(raw: bytes) -> FileMeta:
        data = json.loads(raw.decode("utf-8"))
        return FileMeta(
            FileId(data["id"]),
            FileName(data["name"]),
            ContentType(data["content_type"]),
            FileSize(data["size"]),
        )

    @staticmethod
    def serialize_meta(meta: FileMeta) -> str:
        return json.dumps(
            {
                "id": meta.get_id(),
                "name": meta.get_name(),
                "content_type": meta.get_content_type(),
                "size": meta.get_size(),
            }
        )

    @staticmethod
    def key(file_id: str) -> str:
        return f"file:meta:{file_id}"

    @property
    def delegate(self) -> DataAccessContract:
        if not self._delegate:
            raise RuntimeError("Bind delegate before accessing it")
        return self._delegate

    def bind_delegate(self, delegate: DataAccessContract) -> None:
        if self._delegate:
            raise RuntimeError("Delegate already bind")
        self._delegate = delegate

    @wrap_redis_failure("get")
    async def _try_get(self, key: str) -> bytes | None:
        return await self._redis.get(key)

    @wrap_redis_failure("set")
    async def _try_set(self, key: str, value: str, ex: int = 3600) -> None:
        await self._redis.set(name=key, value=value, ex=ex)

    @wrap_redis_failure("delete")
    async def _try_delete(self, key: str) -> None:
        await self._redis.delete(key)
