from collections.abc import AsyncIterator
from typing import Optional, Protocol

from domain.models import FileMeta
from shared.enums import Buckets


class UpdateUseCaseContract(Protocol):
    async def execute(
        self,
        file_id: str,
        name: str,
        stream: Optional[AsyncIterator[bytes]],
        bucket: Buckets,
    ) -> FileMeta: ...
