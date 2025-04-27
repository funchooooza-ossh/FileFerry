from collections.abc import AsyncIterator
from typing import Optional, Protocol

from domain.models import FileMeta
from shared.enums import Buckets


class ApplicationAdapterContract(Protocol):
    """Базовый адаптер для работы с приложением."""

    async def upload(
        self,
        *,
        name: str,
        stream: AsyncIterator[bytes],
        bucket: Buckets,
    ) -> FileMeta: ...

    async def retrieve(
        self,
        *,
        file_id: str,
        bucket: Buckets,
    ) -> AsyncIterator[bytes]: ...

    async def delete(
        self,
        *,
        file_id: str,
        bucket: Buckets,
    ) -> None: ...

    async def update(
        self,
        *,
        file_id: str,
        name: Optional[str] = None,
        stream: Optional[AsyncIterator[bytes]] = None,
    ) -> Optional[FileMeta]: ...

    # TODO return type healthcheck
    async def healthcheck(self) -> dict[str, str]: ...
