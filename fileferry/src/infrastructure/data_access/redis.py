import asyncio
import json
from collections.abc import Coroutine
from typing import Any, Optional

from loguru import logger
from redis.asyncio import Redis
from redis.exceptions import RedisError

from contracts.infrastructure import (
    DataAccessContract,
    ImportantTaskManagerContract,
    RedisDataAccessContract,
    TaskSchedulerContract,
)
from domain.models import ContentType, FileId, FileMeta, FileName, FileSize
from infrastructure.tasks.wrapper import wrap_with_event_timeout
from shared.exceptions.handlers.redis_handler import wrap_redis_failure


class RedisDataAccess(RedisDataAccessContract):
    def __init__(
        self,
        redis: Redis,
        scheduler: TaskSchedulerContract,
        manager: ImportantTaskManagerContract,
        ttl: int = 300,
        delegate: Optional[DataAccessContract] = None,
    ) -> None:
        self._delegate = delegate
        self._redis = redis
        self._scheduler = scheduler
        self._cache_ttl = ttl
        self._manager = manager

    async def get(self, file_id: str) -> FileMeta:
        key = self.key(file_id)
        cached = await self._try_get(key)
        if cached:
            return self.deserialize_meta(cached)

        result = await self.delegate.get(file_id=file_id)

        self._scheduler.schedule(
            self._try_set(key, value=self.serialize_meta(result), ex=self._cache_ttl)
        )

        return result

    async def save(self, file_meta: FileMeta) -> FileMeta:
        result = await self.delegate.save(file_meta)

        key = self.key(result.get_id())
        cache_value = self.serialize_meta(result)
        self._scheduler.schedule(
            self._try_set(key, value=cache_value, ex=self._cache_ttl)
        )

        return result

    async def update(self, meta: FileMeta) -> FileMeta:
        result = await self.delegate.update(meta)

        key = self.key(result.get_id())
        await self.invalidate_cache(key, ttl_seconds=self._cache_ttl)

        return result

    async def delete(self, file_id: str) -> None:
        await self.delegate.delete(file_id)

        key = self.key(file_id)
        await self.invalidate_cache(key, ttl_seconds=self._cache_ttl)

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
    async def _try_set(self, key: str, value: str, ex: int) -> None:
        await self._redis.set(name=key, value=value, ex=ex)

    async def invalidate_cache(self, key: str, ttl_seconds: int) -> None:
        event = asyncio.Event()
        logger.info(f"[REDIS][INVALIDATE] Scheduling task for key={key}")

        def task_factory() -> Coroutine[Any, Any, Any]:
            async def _task() -> None:
                deadline = asyncio.get_event_loop().time() + ttl_seconds
                while not event.is_set():
                    try:
                        logger.info(f"[REDIS][INVALIDATE] Trying for {key}")
                        await self._redis.delete(key)
                        logger.info(f"[REDIS][INVALIDATE] Finished for {key}")
                        return
                    except RedisError:
                        if asyncio.get_event_loop().time() >= deadline:
                            event.set()
                        else:
                            logger.info(f"[REDIS][INVALIDATE] Sleeping for {key}")
                            await asyncio.sleep(5)

            return wrap_with_event_timeout(_task(), event, ttl_seconds)

        await self._manager.schedule(key, task_factory, event)
