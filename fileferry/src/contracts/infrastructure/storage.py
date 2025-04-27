# contracts/infrastructure/storage_access.py
from collections.abc import AsyncIterator
from typing import Protocol

from domain.models import FileMeta
from shared.enums import Buckets


class StorageAccessContract(Protocol):
    """Контракт для работы с файловым хранилищем."""

    async def stage_upload(
        self, *, file_meta: FileMeta, stream: AsyncIterator[bytes], bucket: Buckets
    ) -> str:
        """Временно загружает файл в хранилище (без подтверждения)."""
        ...

    async def commit(
        self, *, staged_file_id: str, final_file_id: str, bucket: Buckets
    ) -> None:
        """Подтверждает загрузку временного файла, превращая его в окончательный."""
        ...

    async def rollback(self, *, staged_file_id: str, bucket: Buckets) -> None:
        """Откатывает загрузку временного файла."""
        ...

    async def retrieve(self, *, file_id: str, bucket: Buckets) -> AsyncIterator[bytes]:
        """Извлекает файл из хранилища."""
        ...

    async def delete(self, *, file_id: str, bucket: Buckets) -> None:
        """Удаляет файл из хранилища."""
        ...
