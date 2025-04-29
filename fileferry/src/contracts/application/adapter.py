from collections.abc import AsyncIterator
from typing import Optional, Protocol

from domain.models import FileId, FileMeta, FileName, HealthReport
from shared.enums import Buckets


class ApplicationAdapterContract(Protocol):
    """Базовый адаптер для работы с приложением."""

    async def upload(
        self,
        *,
        name: FileName,
        stream: AsyncIterator[bytes],
        bucket: Buckets,
    ) -> FileMeta: ...

    async def retrieve(
        self,
        *,
        file_id: FileId,
        bucket: Buckets,
    ) -> tuple[FileMeta, AsyncIterator[bytes]]: ...

    async def delete(
        self,
        *,
        file_id: FileId,
        bucket: Buckets,
    ) -> None: ...

    async def update(
        self,
        *,
        bucket: Buckets,
        file_id: FileId,
        name: FileName,
        stream: Optional[AsyncIterator[bytes]] = None,
    ) -> FileMeta: ...

    async def healthcheck(self) -> HealthReport: ...
