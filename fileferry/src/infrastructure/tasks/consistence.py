import asyncio

from loguru import logger
from redis.asyncio import RedisError

from contracts.infrastructure import (
    CacheInvalidatorContract,
    FileMetaCacheStorageContract,
    ImportantTaskManagerContract,
)


class CacheInvalidator(CacheInvalidatorContract):
    """
    Самый сомнительный, но и наверное самый интересный в реализации класс.
    Инвалидирует кэш любой ценой для избежания нарушения согласованности
    данных в базе и кэше.
    Я признаю, что это решение спорное, но мне оно понравилось и я решил его реализовать.
    """

    def __init__(
        self,
        cache_storage: FileMetaCacheStorageContract,
        task_manager: ImportantTaskManagerContract,
        retry_interval: float = 5.0,
    ) -> None:
        self._storage = cache_storage
        self._manager = task_manager
        self._retry_interval = retry_interval

    async def invalidate(
        self, file_id: str, max_retry_seconds: int | float
    ) -> asyncio.Event:
        done = asyncio.Event()
        deadline = asyncio.get_running_loop().time() + max_retry_seconds

        async def task() -> None:
            try:
                while True:
                    try:
                        await self._storage.delete(file_id)
                        return
                    except RedisError:
                        if asyncio.get_running_loop().time() >= deadline:
                            logger.info(
                                f"[INAVLIDATE] Finished for {file_id} due to timeout"
                            )
                            return
                        await asyncio.sleep(self._retry_interval)
            finally:
                logger.info(f"[INAVLIDATE] Finished for {file_id}")
                done.set()

        await self._manager.schedule(file_id, lambda: task())
        return done
