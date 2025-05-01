from typing import Protocol


class CacheInvalidatorContract(Protocol):
    async def invalidate(self, file_id: str, ttl: int) -> None: ...
