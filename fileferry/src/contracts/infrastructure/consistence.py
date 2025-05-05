import asyncio
from typing import Protocol


class CacheInvalidatorContract(Protocol):
    """Контракт инвалидатора кэша."""

    async def invalidate(
        self, file_id: str, max_retry_seconds: int
    ) -> asyncio.Event: ...
