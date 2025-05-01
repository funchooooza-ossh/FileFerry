from contracts.infrastructure import (
    CacheInvalidatorContract,
    CacheStorageContract,
    DataAccessContract,
    TaskSchedulerContract,
)
from domain.models import FileMeta


class CachedFileMetaAccess(DataAccessContract):
    def __init__(
        self,
        invalidator: CacheInvalidatorContract,
        storage: CacheStorageContract,
        scheduler: TaskSchedulerContract,
        delegate: DataAccessContract,
        ttl: int = 300,
    ) -> None:
        self._delegate = delegate
        self._cache_ttl = ttl
        self._invalidator = invalidator
        self._storage = storage
        self._scheduler = scheduler

    async def save(self, file_meta: FileMeta) -> FileMeta:
        result = await self._delegate.save(file_meta)

        self._scheduler.schedule(self._storage.set(file_meta, ttl=self._cache_ttl))
        return result

    async def get(self, file_id: str) -> FileMeta:
        cached = await self._storage.get(file_id)
        if cached:
            return cached
        result = await self._delegate.get(file_id)

        self._scheduler.schedule(self._storage.set(result, ttl=self._cache_ttl))

        return result

    async def update(self, meta: FileMeta) -> FileMeta:
        result = await self._delegate.update(meta)

        await self._invalidator.invalidate(meta.get_id(), ttl=self._cache_ttl)

        return result

    async def delete(self, file_id: str) -> None:
        await self._delegate.delete(file_id)

        await self._invalidator.invalidate(file_id, ttl=self._cache_ttl)
