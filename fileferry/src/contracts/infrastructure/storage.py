# contracts/infrastructure/storage_access.py
from collections.abc import AsyncIterator
from typing import Protocol

from domain.models import FileMeta
from shared.enums import Buckets
from shared.types.component_health import ComponentStatus


class StorageAccessContract(Protocol):
    """Контракт для работы с файловым хранилищем."""

    async def upload(
        self, *, file_meta: FileMeta, stream: AsyncIterator[bytes], bucket: Buckets
    ) -> None:
        """Временно загружает файл в хранилище (без подтверждения)."""
        ...

    async def retrieve(self, *, file_id: str, bucket: Buckets) -> AsyncIterator[bytes]:
        """Извлекает файл из хранилища."""
        ...

    async def delete(self, *, file_id: str, bucket: Buckets) -> None:
        """Удаляет файл из хранилища."""
        ...

    async def healthcheck(self) -> ComponentStatus: ...


class CacheStorageContract(Protocol):
    async def get(self, file_id: str) -> FileMeta | None: ...
    async def set(self, meta: FileMeta, ttl: int) -> None: ...
    async def delete(self, file_id: str) -> None: ...
    async def healthcheck(self) -> ComponentStatus: ...
