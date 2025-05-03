from contracts.infrastructure import (
    CacheInvalidatorContract,
    CacheStorageContract,
    DataAccessContract,
    FireAndForgetTasksContract,
)
from domain.models import FileMeta


class CachedFileMetaAccess(DataAccessContract):
    def __init__(
        self,
        invalidator: CacheInvalidatorContract,
        storage: CacheStorageContract,
        scheduler: FireAndForgetTasksContract,
        delegate: DataAccessContract,
        ttl: int = 300,
    ) -> None:
        self._delegate = delegate
        self._cache_ttl = ttl
        self._cache_invalidator = invalidator
        self._сache_storage = storage
        self._scheduler = scheduler

    async def save(self, file_meta: FileMeta) -> FileMeta:
        result = await self._delegate.save(file_meta)
        if result:
            self._scheduler.schedule(
                self._сache_storage.set(file_meta, ttl=self._cache_ttl)
            )
        return result

    async def get(self, file_id: str) -> FileMeta:
        cached = await self._сache_storage.get(file_id)
        if cached:
            return cached
        result = await self._delegate.get(file_id)
        if result:
            self._scheduler.schedule(
                self._сache_storage.set(result, ttl=self._cache_ttl)
            )

        return result

    async def update(self, meta: FileMeta) -> FileMeta:
        result = await self._delegate.update(meta)
        if result:
            await self._cache_invalidator.invalidate(
                meta.get_id(), max_retry_seconds=self._cache_ttl
            )

        return result

    async def delete(self, file_id: str) -> None:
        await self._delegate.delete(file_id)

        await self._cache_invalidator.invalidate(
            file_id, max_retry_seconds=self._cache_ttl
        )
