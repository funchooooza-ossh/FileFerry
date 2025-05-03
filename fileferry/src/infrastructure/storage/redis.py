import json
from typing import Optional

from redis.asyncio import Redis

from contracts.infrastructure import CacheStorageContract
from domain.models import FileMeta
from shared.exceptions.handlers.redis_handler import wrap_redis_failure
from shared.object_mapping.filemeta import DTOFileMeta, FileMetaMapper


class RedisCacheStorage(CacheStorageContract):
    def __init__(self, client: Redis, prefix: str) -> None:
        self._client = client
        self._prefix = prefix

    def key(self, file_id: str) -> str:
        return f"{self._prefix}:{file_id}"

    @wrap_redis_failure("get")
    async def get(self, file_id: str) -> Optional[FileMeta]:
        key = self.key(file_id)
        raw = await self._client.get(key)
        if raw:
            return self.deserialize_meta(raw)

    @wrap_redis_failure("set")
    async def set(self, meta: FileMeta, ttl: int) -> None:
        key = self.key(meta.get_id())
        value = self.serialize_meta(meta)
        await self._client.set(name=key, value=value, ex=ttl)

    @wrap_redis_failure("delete", raising=True)
    async def delete(self, file_id: str) -> None:
        key = self.key(file_id)
        await self._client.delete(key)

    @staticmethod
    def deserialize_meta(raw: bytes) -> FileMeta:
        serialized_meta = DTOFileMeta(**json.loads(raw.decode("utf-8")))
        return FileMetaMapper.deserialize_filemeta(serialized_meta)

    @staticmethod
    def serialize_meta(meta: FileMeta) -> str:
        return json.dumps(FileMetaMapper.serialize_filemeta(meta))
