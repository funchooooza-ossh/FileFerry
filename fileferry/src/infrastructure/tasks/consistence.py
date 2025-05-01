import asyncio
from collections.abc import Coroutine
from typing import Any

from loguru import logger
from redis.asyncio import RedisError

from contracts.infrastructure import (
    CacheInvalidatorContract,
    CacheStorageContract,
    ImportantTaskManagerContract,
)
from infrastructure.tasks.wrapper import wrap_with_event_timeout


class CacheInvalidator(CacheInvalidatorContract):
    def __init__(
        self, storage: CacheStorageContract, manager: ImportantTaskManagerContract
    ) -> None:
        self._storage = storage
        self._manager = manager

    async def invalidate(self, file_id: str, ttl: int) -> None:
        event = asyncio.Event()
        logger.info(f"[REDIS][INVALIDATE] Scheduling task for key={file_id}")

        def task_factory() -> Coroutine[Any, Any, Any]:
            async def _task() -> None:
                deadline = asyncio.get_event_loop().time() + ttl
                while not event.is_set():
                    try:
                        logger.info(f"[INVALIDATE] Trying for {file_id}")
                        await self._storage.delete(file_id)
                        logger.success(f"[INVALIDATE] Finished for {file_id}")
                        return
                    except RedisError:
                        if asyncio.get_event_loop().time() >= deadline:
                            event.set()
                        else:
                            logger.info(f"[INVALIDATE] Sleeping for {file_id}")
                            await asyncio.sleep(5)

            return wrap_with_event_timeout(_task(), event, ttl)

        await self._manager.schedule(file_id, task_factory, event)
