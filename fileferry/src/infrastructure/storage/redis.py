import json
import time
from typing import Any, Optional

from redis.asyncio import Redis

from contracts.infrastructure import FileMetaCacheStorageContract
from domain.models import FileMeta
from infrastructure.exceptions.handlers.redis_handler import wrap_redis_failure
from infrastructure.types.health.component_health import ComponentStatus
from shared.object_mapping.filemeta import DTOFileMeta, FileMetaMapper


class RedisFileMetaCacheStorage(FileMetaCacheStorageContract):
    """
    Кэш-хранилище FileMeta в реализации через Redis.
    Инкапсулирует работу с Redis клиентом, реализует FileMetaCacheStorageContract.
    """

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

    async def healthcheck(self) -> ComponentStatus:
        start = time.perf_counter()
        try:
            pong: bool = await self._client.ping()  # type: ignore redis-py has not fully annotated
            latency = (time.perf_counter() - start) * 1000

            if not pong:
                return ComponentStatus(status="degraded", error="no pong from redis")
            info: dict[str, Any] = await self._client.info()  # type: ignore
            version_raw = info.get("redis_version", "unknown")

            status = "ok" if latency <= 20.0 else "degraded"

            return ComponentStatus(
                status=status,
                latency_ms=latency,
                details={"version_raw": f"Redis {version_raw}"},
            )

        except Exception as exc:
            return ComponentStatus(status="down", error=str(exc))
