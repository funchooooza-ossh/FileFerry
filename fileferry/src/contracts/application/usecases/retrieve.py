from collections.abc import AsyncIterator
from typing import Protocol

from domain.models import FileMeta
from shared.enums import Buckets


class RetrieveUseCaseContract(Protocol):
    async def execute(
        self, file_id: str, bucket: Buckets
    ) -> tuple[FileMeta, AsyncIterator[bytes]]: ...
