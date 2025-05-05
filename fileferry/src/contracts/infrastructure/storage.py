# contracts/infrastructure/storage_access.py
from collections.abc import AsyncIterator
from typing import Any, Protocol

from domain.models import FileMeta
from shared.enums import Buckets
from shared.types.component_health import ComponentStatus


class StorageAccessContract(Protocol):
    """Контракт для работы с файловым хранилищем."""

    async def upload(
        self, *, file_meta: FileMeta, stream: AsyncIterator[bytes], bucket: Buckets
    ) -> None:
        """Загружает файл в хранилище."""
        ...

    async def retrieve(self, *, file_id: str, bucket: Buckets) -> AsyncIterator[bytes]:
        """Извлекает файл из хранилища."""
        ...

    async def delete(self, *, file_id: str, bucket: Buckets) -> None:
        """Удаляет файл из хранилища."""
        ...

    async def healthcheck(self) -> ComponentStatus:
        """Проверка состояния."""
        ...


class CacheStorageContract(Protocol):
    async def get(self, *args: Any, **kwargs: Any) -> Any:
        """Получить кэш."""
        ...

    async def set(self, *args: Any, **kwargs: Any) -> Any:
        """Установить кэш."""
        ...

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        """Удалить кэш."""
        ...

    async def healthcheck(self, *args: Any, **kwargs: Any) -> ComponentStatus:
        """Проверка состояния."""
        ...


class FileMetaCacheStorageContract(CacheStorageContract, Protocol):
    """Конракт для работы с FileMeta кэш-хранилищем."""

    async def get(self, file_id: str) -> FileMeta | None:
        """Получить FileMeta кэш по ID"""
        ...

    async def set(self, meta: FileMeta, ttl: int) -> None:
        """Установить FileMeta в кэш"""
        ...

    async def delete(self, file_id: str) -> None:
        """Удалить кэш FileMeta по ID"""
        ...
